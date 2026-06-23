---
title: "Bootstrap — máquina nova zero-to-ready"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - dotfiles
  - magus
  - bootstrap
  - provisioning
aliases:
  - Bootstrap
  - Provisioning
---

# Bootstrap — máquina nova zero-to-ready

> [!abstract] TL;DR
> Bootstrap = script único que leva máquina nova de zero até dev-ready em 1 comando. Etapas típicas: detectar OS, instalar package manager (Homebrew em macOS), instalar deps (Brewfile/apt), clonar dotfiles, aplicar (stow/chezmoi/bare). Propriedades essenciais: **idempotente** (rodar 2x não quebra), **modular** (skip etapa já completa), **logged** (`set -x`), **falha rápida** (`set -euo pipefail`). Alternativas pra orchestration: Ansible (overkill solo), justfile, Makefile.

## O que é / Como funciona

### O problema

Toda vez que uma máquina muda — laptop trocado, VM nova, container de dev, server provisionado —, o setup manual é longo e propenso a erro:

- Instalar Homebrew (macOS)
- Instalar N apps (`git`, `neovim`, `zsh`, `lazygit`, `stow`…)
- Clonar repositório de dotfiles
- Aplicar dotfiles (stow / chezmoi / bare)
- Configurar shell default (`chsh`)
- Adicionar SSH keys
- Setar `git user.email`

Sem automação: 1-3 horas. Com bootstrap: 1 comando, 5-20 minutos.

O objetivo do bootstrap não é fazer tudo automaticamente na primeira vez — é tornar a reprodução **determinística e repetível**. Você documenta o setup em código, não em memória.

### Etapas canônicas

1. **Detectar OS** — `uname -s`, `/etc/os-release`
2. **Instalar package manager** se faltar (Homebrew em macOS; `apt` já existe no Linux)
3. **Instalar deps** — `brew bundle --file=Brewfile` ou equivalente
4. **Clonar dotfiles** — se o diretório ainda não existe
5. **Aplicar dotfiles** — `stow zsh nvim git` ou `chezmoi init --apply <repo>` ou `dotfiles checkout`
6. **Configs pós-apply** — shell default (`chsh`), `git user.email`, SSH keys

A ordem importa: package manager → deps → clone → apply. Inverter quebra o apply (stow não está instalado ainda).

### Propriedades essenciais

**Idempotente:**
Rodar o script 2x não quebra a máquina. Cada etapa verifica o estado atual antes de agir.

```bash
# Mau — falha se bat já está instalado (dependendo de versão/estado)
brew install bat

# Bom — verifica antes
if ! command -v bat >/dev/null; then
  brew install bat
fi

# Homebrew moderno aceita install em já-instalado sem erro fatal
# brew bundle é idempotente nativamente
brew bundle --file=Brewfile
```

**Modular:**
Cada etapa é uma função independente. Facilita re-rodar só a parte que falhou.

```bash
install_brew() { ... }
install_deps() { ... }
clone_dotfiles() { ... }
apply_dotfiles() { ... }

install_brew
install_deps
clone_dotfiles
apply_dotfiles
```

**Logged:**
Toda saída vai pro log pra diagnóstico posterior.

```bash
set -x
exec > >(tee -a bootstrap.log)
exec 2>&1
```

**Falha rápida:**
Qualquer erro aborta o script imediatamente — sem continuar silenciosamente com estado inválido.

```bash
set -euo pipefail
# -e: exit on error
# -u: erro em var não-definida
# -o pipefail: erro em qualquer parte de pipe
```

### Estratégias de orchestration

**Script shell direto:**
A abordagem mais simples. Pro: sem dependências externas, qualquer shell executa. Con: cresce difícil de manter conforme o número de etapas aumenta; sem grafo de dependências.

**Brewfile (macOS + Linux brew):**
Arquivo declarativo que descreve todos os pacotes Homebrew. Idempotente nativo — `brew bundle` só instala o que falta.

```ruby
# Brewfile
tap "homebrew/cask"

brew "git"
brew "neovim"
brew "lazygit"
brew "lazydocker"
brew "zellij"
brew "stow"
brew "chezmoi"

cask "ghostty"
cask "raycast"
```

Run: `brew bundle --file=Brewfile`. Para gerar o Brewfile a partir dos pacotes instalados: `brew bundle dump --force`.

**justfile (just):**
`just` é um command runner que resolve dependências entre "recipes". Cada recipe é uma etapa.

```just
default:
    @just --list

bootstrap: install-brew install-deps clone-dotfiles apply-dotfiles

install-brew:
    if ! command -v brew >/dev/null; then \
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; \
    fi

install-deps:
    brew bundle --file=~/dotfiles/Brewfile

clone-dotfiles:
    [ -d ~/dotfiles ] || git clone https://github.com/alice/dotfiles ~/dotfiles

apply-dotfiles:
    cd ~/dotfiles && stow zsh nvim git
```

Pro: grafo de dependências entre recipes; `just install-deps` reexecuta só uma etapa. Con: `just` precisa estar instalado antes — bootstrapping problem (resolver com script mínimo que instala just).

**Makefile:**
Mesma ideia do justfile, mas com `make`. Desvantagem: tabs obrigatórias (fricção) e semântica pra build de files (não pra tasks).

**chezmoi `run_once_*.sh` scripts:**
chezmoi executa scripts com prefixo `run_once_` exatamente uma vez por máquina (controle via hash em state). Ideal pra instalar deps que são pré-requisito do apply.

```bash
# ~/.local/share/chezmoi/run_once_install-deps.sh.tmpl
#!/usr/bin/env bash
set -euo pipefail
{{ if eq .chezmoi.os "darwin" }}
brew bundle --file={{ .chezmoi.sourceDir }}/Brewfile
{{ else if eq .chezmoi.os "linux" }}
sudo apt update && sudo apt install -y git neovim zsh
{{ end }}
```

**Ansible:**
Overkill pra single-machine; bom pra fleet (≥5 máquinas similares). Curva de aprendizado alta. Para dev solo no terminal, bootstrap em shell + Brewfile resolve sem overhead.

### Cross-OS bootstrap — exemplo end-to-end

Exemplo funcional de script cross-OS com todas as propriedades essenciais:

```bash
#!/usr/bin/env bash
set -euo pipefail

log() { echo "[bootstrap] $*"; }

# 1. Detectar OS
case "$(uname -s)" in
  Darwin*) OS=macos ;;
  Linux*)
    if grep -qi microsoft /proc/version 2>/dev/null; then
      OS=wsl
    else
      OS=linux
    fi
    ;;
  *) log "OS desconhecido"; exit 1 ;;
esac
log "OS: $OS"

# 2. Package manager
if [[ "$OS" == "macos" ]] && ! command -v brew >/dev/null; then
  log "Instalando Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 3. Deps por OS
case "$OS" in
  macos)
    log "Instalando deps macOS"
    [[ -d "$HOME/dotfiles" ]] || git clone https://github.com/alice/dotfiles "$HOME/dotfiles"
    brew bundle --file="$HOME/dotfiles/Brewfile"
    ;;
  linux|wsl)
    log "Instalando deps Linux"
    sudo apt update
    sudo apt install -y git zsh neovim stow ripgrep fzf bat
    ;;
esac

# 4. Dotfiles
if [[ ! -d "$HOME/dotfiles" ]]; then
  log "Clonando dotfiles"
  git clone https://github.com/alice/dotfiles "$HOME/dotfiles"
fi

# 5. Aplicar (stow exemplo)
log "Aplicando dotfiles"
cd "$HOME/dotfiles"
stow zsh git nvim

# 6. Shell default
if [[ "$SHELL" != *zsh ]]; then
  log "Setando zsh como default"
  ZSH_PATH="$(which zsh)"
  if ! grep -q "$ZSH_PATH" /etc/shells; then
    echo "$ZSH_PATH" | sudo tee -a /etc/shells
  fi
  chsh -s "$ZSH_PATH"
fi

log "Bootstrap completo! Restart shell ou exec zsh"
```

## Na prática

### Testar bootstrap em VM/container

Antes de confiar no script em máquina real, testar em ambiente descartável:

```bash
# Docker (Ubuntu 22.04)
docker run --rm -it -v "$(pwd):/dotfiles" ubuntu:22.04 bash
# Dentro do container:
apt update && apt install -y curl git sudo
useradd -m alice -s /bin/bash
su - alice -c "bash /dotfiles/bootstrap.sh"
```

```bash
# Multipass (macOS) — VM Linux leve
multipass launch --name test-bootstrap
multipass shell test-bootstrap
# Dentro da VM:
bash <(curl -fsSL https://raw.githubusercontent.com/alice/dotfiles/main/bootstrap.sh)
```

Testar em container tem uma limitação: não testa mudanças de shell (`chsh`) nem serviços de sistema — é bom pra verificar instalação de pacotes e apply de dotfiles.

### Bootstrap incremental

Para máquinas onde parte do setup já está feita, uma função `ensure_installed` evita reinstalar o que já existe:

```bash
ensure_installed() {
  for pkg in "$@"; do
    if ! command -v "$pkg" >/dev/null; then
      log "Installing $pkg"
      brew install "$pkg" || sudo apt install -y "$pkg"
    fi
  done
}

ensure_installed git neovim zsh stow
```

Isso permite rodar o bootstrap como "refresh" — aplica só o que falta — sem efeitos colaterais no que já está correto.

### Recovery

Se o bootstrap falhar no meio (rede cai, pacote não encontra versão, etc.), a idempotência garante que re-rodar é seguro:

```bash
bash bootstrap.sh         # re-roda tudo; pula o que já está ok
just install-deps         # ou só uma etapa específica
chezmoi apply             # só o apply dos dotfiles
```

Manter logs habilitados (`set -x`, `tee bootstrap.log`) facilita identificar onde a falha ocorreu.

## Armadilhas

**Bootstrap destrutivo em máquina já configurada**
**Causa:** comandos como `rm`, `mv`, `chsh` sem verificação de estado atual executam em cima de config existente.
**Sintoma:** shell config anterior sobrescrito; symlinks de stow criados em cima de arquivos reais (stow falha com "already exists").
**Como detectar:** ler o script inteiro antes de rodar pela primeira vez; testar em VM.
**Solução:** verificações explícitas antes de cada operação destrutiva — `[[ -d ]]`, `[[ -f ]]`, `[[ -L ]]`; backup com timestamp (`cp ~/.zshrc ~/.zshrc.bak.$(date +%Y%m%d)`).

---

**`brew install` sem `Brewfile` cresce desorganizado**
**Causa:** ao instalar pacotes ad-hoc com `brew install X` ao longo do tempo, o bootstrap não rastreia o que é intencional.
**Sintoma:** máquina nova não tem a mesma lista de ferramentas; sync entre máquinas inconsistente.
**Como detectar:** `brew leaves` mostra top-level installs; comparar com o que está no Brewfile.
**Solução:** centralizar todas as deps em `Brewfile` versionado no repo de dotfiles; `brew bundle dump --force` regenera o Brewfile a partir do estado atual.

---

**Script falha silenciosa sem `set -e`**
**Causa:** sem `set -e` (ou `set -euo pipefail`), um comando que falha no meio do script não aborta — a execução continua com estado inválido.
**Sintoma:** bootstrap "completou" com sucesso aparente mas etapas críticas falharam silenciosamente (clone não aconteceu, apply não rodou).
**Como detectar:** ler os logs; verificar se os arquivos/ferramentas esperados existem após o script.
**Solução:** sempre `set -euo pipefail` na segunda linha do script (após o shebang); adicionar `log()` antes de cada etapa para output rastreável.

---

**`chsh` sem zsh em `/etc/shells` falha**
**Causa:** `chsh` só permite setar um shell que está listado em `/etc/shells`. Em sistemas Linux onde zsh foi instalado manualmente (não via apt), o path não está na lista.
**Sintoma:** `chsh: /home/alice/.local/bin/zsh is not listed in /etc/shells`.
**Como detectar:** ler a mensagem de erro; `cat /etc/shells` confirma ausência.
**Solução:** antes do `chsh`, verificar e adicionar: `grep -q "$(which zsh)" /etc/shells || echo "$(which zsh)" | sudo tee -a /etc/shells`.

---

**Bootstrap clona dotfiles e aplica antes das dependências instaladas**
**Causa:** ordem das etapas errada — clone/apply antes de instalar as ferramentas que o apply precisa (`stow`, `chezmoi`).
**Sintoma:** `stow` not found ao tentar `stow zsh nvim`; ou `.zshrc` faz `source` de plugins que ainda não existem.
**Como detectar:** ler o erro de "command not found" no log.
**Solução:** ordem canônica obrigatória: package manager → deps → clone dotfiles → apply. Documentar a ordem no comentário do script.

---

**Homebrew `install.sh` muda de URL/comportamento sem aviso**
**Causa:** o script de instalação do Homebrew é baixado de URL remota em tempo de execução — não é versionado junto com o bootstrap.
**Sintoma:** `curl` retorna 404 ou o script mudou de comportamento e falha; ou requer interação (prompt) que quebra automação.
**Como detectar:** rodar com `set -x` mostra a URL e a resposta do curl.
**Solução:** checar a URL canônica na documentação do Homebrew antes de usar; adicionar `|| true` + verificação manual apenas pra Homebrew (caso já instalado via PATH diferente).

## Em inglês

- **bootstrap** — *bootstrap / inicialização do ambiente*. "Script único que provisiona máquina nova do zero — instala package manager, deps, clona e aplica dotfiles em sequência determinística."
- **provisioning** — *provisionamento*. "Automação de setup inicial de uma máquina: instalar deps, configurar serviços, aplicar configs. Pode ser single-machine (script bash) ou fleet (Ansible, Salt)."
- **idempotent** — *idempotente*. "Operação que produz o mesmo resultado se executada N vezes — rodar `bash bootstrap.sh` 2x não quebra a máquina porque cada etapa verifica estado antes de agir."
- **modular** — *modular*. "Estrutura em que cada etapa do bootstrap é uma função independente, permitindo re-rodar só a parte que falhou sem repetir o setup inteiro."
- **recovery** — *recuperação / recovery*. "Capacidade de retomar o bootstrap de onde parou após falha — garantida pela idempotência: re-rodar o script (ou só a etapa que falhou) é seguro."
- **dependency** — *dependência*. "Ferramenta ou pacote que outro precisa pra funcionar. Em bootstrap: instalar deps antes de aplicar dotfiles evita 'command not found' no apply."
- **package manager** — *gerenciador de pacotes*. "Ferramenta que instala, atualiza e remove pacotes de software — Homebrew (macOS/Linux), apt (Debian/Ubuntu), pacman (Arch). Bootstrap começa por instalar o package manager se ausente."
- **fleet** — *fleet / frota de máquinas*. "Conjunto de máquinas com setup similar gerenciadas em massa — Ansible, Salt, Puppet. Para dev solo, bootstrap em shell + Brewfile resolve sem overhead de fleet management."
- **declarative** — *declarativo*. "Descreve o estado desejado, não os passos. Brewfile é declarativo: lista quais pacotes devem estar instalados; `brew bundle` resolve o delta."
- **automation** — *automação*. "Substituir passos manuais repetitivos por código executável — bootstrap é automação de setup de ambiente, transformando 1-3h de trabalho manual em 1 comando."

## Veja também

- [[04 - GNU stow — symlinks declarativos]] — pré-requisito para o apply com stow
- [[05 - chezmoi — manager completo com templates]] — alternativa com `run_once_` scripts nativos
- [[06 - Bare git repo — abordagem minimalista]] — alternativa para apply de dotfiles
- [[07 - Secrets em dotfiles — git-crypt, age, sops]] — bootstrap precisa provisionar keys antes de restaurar secrets
- [[09 - Sync entre máquinas heterogêneas]] — bootstrap branched por host
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Bootstrap|bootstrap]], [[Dicionário do Terminal#Idempotente|idempotente]], [[Dicionário do Terminal#Provisioning|provisioning]]

## Referências

- Homebrew Bundle: https://github.com/Homebrew/homebrew-bundle
- just (command runner): https://github.com/casey/just
