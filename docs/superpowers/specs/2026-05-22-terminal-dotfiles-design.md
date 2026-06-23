---
title: "Spec — Galho 5 da trilha Terminal (Dotfiles)"
date: 2026-05-22
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 5 da trilha Terminal (Dotfiles)

## 1. Contexto e motivação

Este é o **quinto galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`; galhos 1-4 já entregues). Pressupõe leitura do roadmap.

O usuário tem **adoção zero** em dotfiles — não conhece o conceito, não usa stow/chezmoi/bare repo. Esta é a primeira exposição. A trilha precisa ser pedagógica de verdade: começa do "o que é um arquivo dotfile" e termina em workflows operacionais avançados (secrets, bootstrap, sync entre máquinas).

Por isso a trilha master previa 6 notas, mas o galho real vai ter **9 notas** (3+3+3). Iniciado é expandido (3 notas em vez de 2) pra dar fundamento: princípios + anatomia + cross-OS. Adepto cobre as 3 ferramentas principais (stow, chezmoi, bare repo) em profundidade equivalente — formato **catálogo comparativo**, deixando o usuário escolher informadamente. Magus traz operacional avançado (secrets, bootstrap, sync) que vale a pena entender mesmo antes de adotar.

**Todos os exemplos** das notas são neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos (`# hipotético: ...`). Sem fabricação de uso pessoal — o usuário ainda não tem dotfiles versionados.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **9 notas atômicas + 1 MOC do galho + expansão do Dicionário do Terminal** em `03-Dominios/Tecnologia/Terminal/Dotfiles/` e `03-Dominios/Tecnologia/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (3 Iniciado + 3 Adepto + 3 Magus).

A trilha precisa ser:

- **Pedagógica** — leitor sem conhecimento prévio entende o que são dotfiles ao final da nota 01, conhece XDG ao final de 02, sabe escolher entre stow/chezmoi/bare ao final de Adepto.
- **Honesta** — comandos testáveis, comparações justas entre ferramentas, sem hype. Quando uma ferramenta é melhor, dizer; quando depende do caso, listar critérios.
- **Atômica** — cada nota cobre um tópico bem-delimitado; cross-references ricos.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Terminal/Dotfiles/`)

Pasta nova, flat. 9 notas + 1 MOC:

#### Iniciado (3 notas — fundamentos)

| # | Nota |
|---|------|
| 01 | Princípios: o que são dotfiles e por que versionar |
| 02 | Anatomia: estrutura típica + XDG Base Directory spec |
| 03 | Cross-OS: Linux vs macOS vs WSL |

#### Adepto (3 notas — ferramentas equivalentes, catálogo comparativo)

| # | Nota |
|---|------|
| 04 | GNU stow: symlinks declarativos |
| 05 | chezmoi: manager completo com templates |
| 06 | Bare git repo: abordagem minimalista |

#### Magus (3 notas — operacional avançado)

| # | Nota |
|---|------|
| 07 | Secrets em dotfiles: git-crypt, age, sops |
| 08 | Bootstrap: máquina nova zero-to-ready |
| 09 | Sync entre máquinas heterogêneas |

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Terminal/Dotfiles/index.md`:
- `type: moc`, `status: growing`, `progresso: andamento`
- Frontmatter padrão (`title: "Dotfiles"`, tags `terminal/dotfiles/moc`, aliases `Dotfiles`)
- Conteúdo agrupado em 3 H3 (Iniciado/Adepto/Magus)
- 3-4 rotas alternativas:
  - **Mínimo viável (entender + 1 ferramenta)**: `01` → `02` → `04` (stow é o mais simples pra começar)
  - **Comparativo das ferramentas**: `01` → `02` → `04` → `05` → `06` (entende as 3 antes de escolher)
  - **Maestria operacional**: `04` (ou `05`) → `07` → `08` → `09`
  - **Cross-OS first**: `01` → `02` → `03` → `05` (chezmoi é melhor pra cross-OS)
- Bloco "Versões assumidas" com stow/chezmoi/git/OS capturados no pré-flight
- Bloco "Como escolher" com tabela de decisão (3 ferramentas × critérios)

### 3.3. Expansão do Dicionário do Terminal

`03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` ganha **novo bloco** `## Dotfiles` (após `## TUIs de Dev / Lazygit / Lazydocker`), com 16 verbetes em ordem alfabética case-insensitive:

| Verbete | Resumo |
|---|---|
| age | Ferramenta de encryption moderna, ssh-key based |
| Bare repo (dotfiles) | `git --git-dir=$HOME/.dotfiles --work-tree=$HOME` |
| Bootstrap | Script idempotente que provisiona máquina nova zero-to-ready |
| chezmoi | Manager de dotfiles em Go (templates, secrets, cross-OS) |
| Dotfile | Arquivo de configuração começando com `.` |
| git-crypt | Encryption transparente no git baseada em GPG via `.gitattributes` |
| Idempotente | Operação que produz o mesmo resultado se executada N vezes |
| Provisioning | Automação de setup inicial de máquina |
| Secret (dotfiles) | Credencial em dotfiles (API key, SSH key, GPG key) |
| sops | Secrets OPerationS (Mozilla), encryption YAML/JSON-aware |
| Stow | GNU stow, gerenciador de symlinks declarativos |
| Symlink | Link simbólico no filesystem |
| Template (dotfiles) | Arquivo com placeholders renderizados em apply-time |
| Whitelist (.gitignore) | `*` + `!arquivo` pra incluir só explícito (usado em bare repo) |
| WSL | Windows Subsystem for Linux |
| XDG Base Directory | Spec freedesktop.org de paths `$XDG_*_HOME` |

Cada verbete tem `Veja também:` apontando pra nota canônica.

### 3.4. Tronco — ativar wikilink

`03-Dominios/Tecnologia/Terminal/index.md`: trocar `- Dotfiles — galho 5 (planejado): gerenciamento de configs e sync` por `- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|Dotfiles]] — galho 5: princípios, ferramentas (stow/chezmoi/bare), secrets, bootstrap, sync`.

## 4. Convenções por nota

Mesmo padrão consolidado nos galhos 2-4:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - terminal
  - dotfiles
  - <fase>
  - <tags específicas>
aliases:
  - <aliases>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout)
- `## O que é / Como funciona` — H3s conforme tópico
- `## Na prática` — exemplos runnable, configs reais
- `## Armadilhas` — **≥5**, cada uma com 4 labels (Causa / Sintoma / Como detectar / Solução)
- `## Em inglês` — bullets bilíngues `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
- `## Veja também` — wikilinks SEM backticks; sempre inclui:
  - Notas relacionadas do galho
  - `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
  - `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
  - Wikilinks pros verbetes do Dicionário
- `## Referências` — docs oficiais + posts canônicos

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos. NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de comandos/flags. Cada flag/opção verificável via doc oficial.
3. **Sem `Co-Authored-By: Claude`**. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em "Veja também".
6. **Tronco wikilink obrigatório** em "Veja também".
7. **MOC wikilink** em "Veja também".
8. **Code fences corretos:** ` ```bash ` pra shell genérico, ` ```yaml ` pra YAML, ` ```toml ` pra TOML, ` ```text ` pra ASCII/diagrams.
9. **Defaults documentados** quando relevante.
10. **Comparações justas** entre ferramentas — sem hype, sem desmerecimento.
11. **Tom pedagógico** — assume zero conhecimento prévio em Iniciado; sobe gradualmente.

## 5. Conteúdo por nota (síntese)

### Iniciado

**01 — Princípios: o que são dotfiles e por que versionar**
- Definição: arquivos de config começando com `.` (ocultos no `ls`); origem do nome em Unix.
- Por que ocultos: convenção de não-poluir `ls` com configs.
- Por que versionar: setup repetível, sync entre máquinas, history de mudanças, dotfiles públicos como CV.
- Exemplos comuns: `~/.zshrc`, `~/.gitconfig`, `~/.config/nvim/init.lua`, `~/.ssh/config`.
- Histórico cultural: github.com/<usuario>/dotfiles como item de portfólio.
- Quando NÃO versionar: secrets sem encryption, paths absolutos hardcoded por usuário, configs geradas por wizards (P10k generated, OAuth tokens).

**02 — Anatomia: estrutura típica + XDG Base Directory spec**
- Layout legacy (anos 90/00): tudo direto em `$HOME` (`~/.bashrc`, `~/.vimrc`, `~/.gitconfig`).
- Layout XDG (moderno, padrão freedesktop.org):
  - `$XDG_CONFIG_HOME` = `~/.config/` — configs
  - `$XDG_DATA_HOME` = `~/.local/share/` — dados de usuário
  - `$XDG_CACHE_HOME` = `~/.cache/` — cache (descartável)
  - `$XDG_STATE_HOME` = `~/.local/state/` — estado runtime
  - `~/.local/bin/` — binários do usuário (não-XDG mas convenção)
- Por que XDG existe: separa config/data/cache (backup só config; clean cache facilmente; não polui home).
- Apps que respeitam: Neovim, Zellij, Lazygit, Lazydocker, fish, atuin, etc. (todos os apps modernos do stack).
- Apps que ignoram: bash (`.bashrc`), git (`.gitconfig`), ssh (`.ssh/`), gpg (`.gnupg/`) — legados.
- Como forçar XDG em app que ignora: env vars (`HISTFILE`, `INPUTRC`) ou flags (`git -C` etc.).

**03 — Cross-OS: Linux vs macOS vs WSL**
- Diferenças de paths: `/home/<user>` (Linux) vs `/Users/<user>` (macOS); WSL tem `/home/<user>` mas vê `/mnt/c/`.
- Shell default: Linux geralmente bash; macOS desde Catalina (2019) usa zsh; WSL depende da distro.
- Package manager: apt/dnf (Linux), brew (macOS, opcional Linux), pacman (Arch), winget/scoop (Windows via WSL).
- GNU vs BSD utils: `sed -i` no Linux funciona sem arg; `sed -i ''` no macOS exige string vazia (BSD `sed`). `grep -P` (Perl regex) só GNU. `realpath` ausente em macOS por default (`brew install coreutils` → `grealpath`).
- Quando dotfile precisa branch: env var `OSTYPE` (`linux-gnu` vs `darwin` vs ...) no shell; `chezmoi` tem `.chezmoi.os`; stow não tem (precisa script externo).
- WSL específico: interop com Windows (`wsl.exe`, `cmd.exe /c`), VS Code remote, clipboard (`clip.exe`).

### Adepto

**04 — GNU stow: symlinks declarativos**
- Filosofia: cada "package" (pasta) no repo representa um app; stow cria symlinks no home com a mesma estrutura.
- Estrutura repo:
  ```
  ~/dotfiles/
  ├── zsh/.zshrc
  ├── nvim/.config/nvim/init.lua
  └── git/.gitconfig
  ```
- Comandos: `stow zsh` (symlink `~/.zshrc` → `~/dotfiles/zsh/.zshrc`); `stow -D zsh` (unstow); `stow -R zsh` (restow); `stow --adopt zsh` (adota files existentes pro repo, raro).
- Flag `-v` (verbose), `-n` (dry-run).
- Vantagens: simples, sem state file, Unix-nativo, fácil debuggar (`ls -la` mostra symlinks).
- Desvantagens: sem templates (não pode rodar lógica em apply), sem cross-OS automático (precisa pastas separadas), sem secrets nativos.
- Workflow típico:
  ```bash
  cd ~/dotfiles && stow zsh nvim git tmux
  ```

**05 — chezmoi: manager completo com templates**
- Filosofia: state machine declarativo — `chezmoi apply` aplica diff entre source e target.
- Source: `~/.local/share/chezmoi/` (configurável).
- Naming convention: `dot_zshrc` → `~/.zshrc`; `dot_config/nvim/init.lua` → `~/.config/nvim/init.lua`.
- Features:
  - **Templates** (Go template syntax): `{{ .chezmoi.os }}`, `{{ .email }}`, `{{ if eq .chezmoi.hostname "work" }}...{{ end }}`
  - **Encrypted files** nativo (age, gpg)
  - **Scripts** (`run_once_<name>.sh`, `run_onchange_<name>.sh`) — bootstrap inline
  - **Data customizada** em `~/.config/chezmoi/chezmoi.toml`
- Workflow:
  ```bash
  chezmoi init https://github.com/<user>/dotfiles.git  # clona + apply
  chezmoi edit ~/.zshrc                                  # edita source
  chezmoi diff                                           # preview
  chezmoi apply                                          # aplica
  chezmoi cd                                             # cd na source
  chezmoi update                                         # pull + apply
  ```
- Vantagens: cross-OS automático via templates, secrets nativos, scripts integrados.
- Desvantagens: curva de aprendizado, "magic" do Go template, state file (`chezmoi-state.boltdb`).

**06 — Bare git repo: abordagem minimalista**
- Filosofia: zero ferramentas — só git. `git --git-dir=$HOME/.dotfiles --work-tree=$HOME`.
- Setup:
  ```bash
  git init --bare $HOME/.dotfiles
  alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
  dotfiles config status.showUntrackedFiles no
  ```
- `.gitignore` whitelist (todos os files ignorados por default; `!` libera específicos):
  ```
  *
  !.zshrc
  !.gitconfig
  !.config/
  !.config/nvim/
  !.config/nvim/init.lua
  ```
- Workflow:
  ```bash
  dotfiles add ~/.zshrc
  dotfiles commit -m "tweak prompt"
  dotfiles push
  ```
- Vantagens: nada pra instalar, máxima portabilidade, fácil cross-machine (clone + checkout).
- Desvantagens: sem templates, sem secrets, sem cross-OS automático; setup inicial mais fricção (whitelist explícita).
- Workflow nova máquina:
  ```bash
  git clone --bare <repo> $HOME/.dotfiles
  alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
  dotfiles checkout            # falha se há conflito com files existentes
  # Resolver: backup conflitos + checkout -f
  dotfiles config status.showUntrackedFiles no
  ```

### Magus

**07 — Secrets em dotfiles: git-crypt, age, sops**
- Problema: secrets em dotfiles (API tokens, SSH/GPG keys, OAuth refresh, DB credentials).
- 3 abordagens canônicas:

  **git-crypt:**
  - GPG-based encryption transparente
  - Setup: `git-crypt init`, `git-crypt add-gpg-user <key>`, marca files em `.gitattributes` (`secrets/* filter=git-crypt diff=git-crypt`)
  - Files encriptados em rest no repo; transparente quando `git-crypt unlock`
  - Pro: integra com workflow git normal; Con: GPG é complicado pra muitos

  **age:**
  - Modern (2019+), ssh-key based ou X25519 keys
  - Setup: `age-keygen -o key.txt`, `age -e -r <recipient> arquivo` → arquivo encrypted
  - Não integra automaticamente com git — você encripta files manualmente ou usa chezmoi
  - Pro: simples, sem GPG; Con: precisa wrap pra fluxo git-aware

  **sops (Mozilla):**
  - YAML/JSON aware — pode encriptar partial (só chaves específicas)
  - Backends: age, GPG, AWS KMS, GCP KMS, Azure Key Vault
  - `sops -e file.yaml > file.enc.yaml`
  - Pro: estrutura preservada, multi-backend; Con: mais complexo de setup

- Comparativo (tabela): git-crypt vs age vs sops por:
  - Curva de aprendizado
  - Granularidade (file todo vs partial)
  - Backend (GPG / age / KMS)
  - Integração nativa com chezmoi/stow/bare

- Quando cada um vence:
  - git-crypt: time já usa GPG, quer transparência git
  - age: quer simples, key-based puro
  - sops: secrets estruturados (YAML/JSON), cloud KMS, equipe DevOps

**08 — Bootstrap: máquina nova zero-to-ready**
- Goal: script único `bootstrap.sh` que leva máquina nova de zero até dev-ready em 1 comando.
- Etapas típicas:
  1. Detectar OS (`uname -s`, `/etc/os-release`)
  2. Instalar package manager se faltar (homebrew em macOS)
  3. Instalar dependências (`brew bundle`, `apt install`, `pacman -S`)
  4. Clonar dotfiles
  5. Aplicar dotfiles (stow/chezmoi/bare checkout)
  6. Configs pós-apply (shell default, git user.email, ssh keys)
- Propriedades importantes:
  - **Idempotente** (rodar 2x não quebra)
  - **Modular** (skip etapa já completa)
  - **Logged** (`set -x`, `tee bootstrap.log`)
  - **Falha rápida** (`set -euo pipefail`)
- Exemplo end-to-end:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail

  # 1. Detectar OS
  os=$(uname -s | tr '[:upper:]' '[:lower:]')

  # 2. Homebrew (idempotente)
  if ! command -v brew >/dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi

  # 3. Deps
  brew bundle --file=~/dotfiles/Brewfile

  # 4. Dotfiles
  [[ -d ~/dotfiles ]] || git clone https://github.com/alice/dotfiles ~/dotfiles
  cd ~/dotfiles && stow zsh nvim git

  # 5. Shell default
  [[ "$SHELL" != *zsh ]] && chsh -s "$(which zsh)"
  ```
- Alternativas: Ansible (overkill pra single-machine), justfile (recipe-based), Makefile (declarativo simples).

**09 — Sync entre máquinas heterogêneas**
- Cenário comum: laptop pessoal + work + servidor cloud, cada um com requisitos diferentes (work tem secrets corp, server não tem GUI, etc.).
- Estratégias:

  **Branches per-host:**
  - Master = baseline; branch `work` = overrides do trabalho.
  - Manter sync via `merge master`.
  - Pro: clean separation; Con: 2x manutenção.

  **Conditional includes (no shell config):**
  - `if hostname == "work-laptop"; source ~/.zshrc.work; fi`
  - Pro: single branch; Con: arquivos extras locais.

  **chezmoi data por host:**
  - `~/.config/chezmoi/chezmoi.toml` define data específica por hostname
  - Templates usam `{{ if eq .chezmoi.hostname "work" }}...{{ end }}`
  - Pro: idiomático em chezmoi; Con: só com chezmoi.

  **Stow com pastas host-specific:**
  - `dotfiles/zsh-work/.zshrc` vs `dotfiles/zsh/.zshrc`
  - Script: `stow zsh-work` ou `stow zsh` conforme host.
  - Pro: flexível; Con: manutenção manual.

- Quando branchar vs quando condicionar:
  - Branches: diferenças grandes/estruturais (work usa Linux + nix, pessoal usa macOS + brew)
  - Condicionais: diferenças pequenas/dinâmicas (alias por host, theme por host)
- Tradeoff: manutenibilidade (branches) vs flexibilidade (condicionais).

## 6. Pesquisa por nota (âncoras)

Cada nota começa com **Step 1: Pesquisa-âncora** — WebFetch em paralelo de docs oficiais.

- **01:** https://wiki.archlinux.org/title/Dotfiles, https://dotfiles.github.io/
- **02:** https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html, https://wiki.archlinux.org/title/XDG_Base_Directory
- **03:** https://learn.microsoft.com/en-us/windows/wsl/, https://apple.stackexchange.com/questions/72515/ (BSD vs GNU sed)
- **04:** https://www.gnu.org/software/stow/manual/stow.html
- **05:** https://www.chezmoi.io/, https://github.com/twpayne/chezmoi
- **06:** https://www.atlassian.com/git/tutorials/dotfiles, https://news.ycombinator.com/item?id=11070797 (origem do bare repo approach)
- **07:** https://github.com/AGWA/git-crypt, https://github.com/FiloSottile/age, https://github.com/getsops/sops
- **08:** https://github.com/Homebrew/homebrew-bundle, https://docs.ansible.com/ (referência)
- **09:** chezmoi templates + ssh config Match patterns

## 7. Plano de execução (preview — detalhado no execution.md)

**Pré-flight (Task 0):** capturar `stow --version`, `chezmoi --version`, `git --version`, info OS.

**Esqueletos (Tasks 1-2):**
- Task 1: `Dotfiles/index.md` (MOC com placeholders)
- Task 2: Bloco `## Dotfiles` vazio no Dicionário

**Notas (Tasks 3-11):** uma task por nota, ordem fase-progressiva. Cada task:
- Implementer subagent (Sonnet) com spec completo + restrições
- Reviewer combinado (Sonnet)
- Fix subagent (Sonnet) se Critical/Important
- Mark complete

**Passes finais (Tasks 12-15):**
- Task 12: Pass final MOC (versões reais)
- Task 13: Pass final Dicionário (alfabético + Veja também)
- Task 14: Tronco wikilink
- Task 15: Validação final (`verificar-wikilinks`)

## 8. Critério de pronto

- 10 arquivos em `03-Dominios/Tecnologia/Terminal/Dotfiles/`: 9 notas + `index.md`
- ≥15 verbetes novos no bloco `## Dotfiles` do Dicionário
- Tronco `Terminal/index.md` com wikilink ativo
- `verificar-wikilinks` em `Dotfiles/` sem broken links
- Quartz build limpo (cross-repo — fora do escopo)
- Todos commits sem `Co-Authored-By: Claude`
- Cada nota com ≥5 armadilhas (4 labels), ≥7 wikilinks, "Em inglês" em bullets bilíngues
- Cada verbete com "Veja também"

## 9. Risco e mitigação

- **Comparações injustas entre ferramentas:** tendência de favorecer uma. **Mitigação:** cada nota Adepto (04/05/06) tem seção explícita "Quando esta ferramenta vence" e "Quando outra ferramenta vence" pra forçar honestidade.
- **Fabricação de uso pessoal:** user em adoção zero; tentação de afirmar "no meu setup X..." é alta. **Mitigação:** reforço em cada implementer prompt + exemplos sempre neutros ou hipotéticos explícitos.
- **Secrets handling errado pode vazar dados:** instruções de git-crypt/age/sops sem cuidado podem causar exposição. **Mitigação:** armadilhas explícitas em nota 07 sobre "commitar antes de encriptar = vazou pro history".
- **Bootstrap script destruir setup existente:** `chsh`, `rm`, `mv` em script de bootstrap em máquina já configurada pode quebrar. **Mitigação:** Magus 08 enfatiza idempotência + verificações (`[[ -d ... ]]`) antes de cada ação.
- **WSL paths esquecidos:** notas focam em Linux/macOS; usuário WSL pode esbarrar em interop. **Mitigação:** nota 03 dedica seção a WSL; notas posteriores citam WSL específico quando relevante.
