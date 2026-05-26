---
title: "Terminal"
created: 2026-04-01
updated: 2026-04-01
type: concept
status: seedling
tags:
  - infraestrutura
  - ferramentas
  - entrevista
publish: false
---

# Terminal

Zsh, Oh My Zsh, e configuração do terminal — produtividade na linha de comando.

## O que é

O terminal é a interface principal de interação para devs. Zsh (Z Shell) é o shell padrão do macOS e popular no Linux, com features como autocompletion avançado, globbing, e plugins via Oh My Zsh.

## Como funciona

### Zsh vs Bash

| Feature | Bash | Zsh |
| --- | --- | --- |
| Autocompletion | Básico | Avançado (tab com menu) |
| Globbing | Básico | Extended (`**/*.ts`) |
| Themes/Plugins | Manual | Oh My Zsh / Zinit |
| Spelling correction | Não | Sim |
| Right prompt | Não | Sim (RPROMPT) |

### Oh My Zsh

Framework de gerenciamento de configuração Zsh com 300+ plugins e 150+ temas.

```bash
# Instalar
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Configurar (~/.zshrc)
ZSH_THEME="robbyrussell"    # ou powerlevel10k
plugins=(
  git                       # aliases git (gst, gco, gp)
  docker                    # completions docker
  kubectl                   # completions k8s
  z                         # jump to directories
  zsh-autosuggestions       # sugestões baseadas no histórico
  zsh-syntax-highlighting   # highlighting de comandos
)
```

### Plugins essenciais

| Plugin | O que faz |
| --- | --- |
| git | Aliases: `gst`=status, `gco`=checkout, `gp`=push |
| z | Pular para diretórios frequentes: `z project` |
| zsh-autosuggestions | Sugere comandos do histórico (→ para aceitar) |
| zsh-syntax-highlighting | Colore comandos válidos/inválidos |
| docker / kubectl | Autocompletion para Docker e K8s |
| nvm | Gerenciar versões do Node.js |

### Ubuntu — Setup básico para devs

```bash
# Essenciais
sudo apt update && sudo apt install -y \
  git curl wget build-essential \
  zsh htop jq tree

# Zsh como default
chsh -s $(which zsh)

# Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# SDKMAN (Java)
curl -s "https://get.sdkman.io" | bash

# NVM (Node)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# Docker
# Seguir docs oficiais: https://docs.docker.com/engine/install/ubuntu/
```

### Aliases úteis

```bash
# ~/.zshrc
alias ll='ls -la'
alias dc='docker compose'
alias k='kubectl'
alias g='git'
alias nr='npm run'
alias code='code .'
```

## Quando usar

- **Sempre:** o terminal é a ferramenta mais poderosa de um dev
- **Zsh + Oh My Zsh:** em qualquer ambiente de desenvolvimento
- **Plugins:** instalar os relevantes para sua stack (git, docker, kubectl, nvm)

## How to explain in English

"I'm a terminal-first developer. I use Zsh with Oh My Zsh for an enhanced shell experience — autosuggestions based on history, syntax highlighting, and plugins for git, Docker, and Kubernetes. This setup significantly boosts my productivity on the command line, which is where I spend most of my time."

### Key vocabulary

- terminal → terminal / command line
- shell → shell: interpretador de comandos
- alias → alias: atalho para comandos
- plugin → plugin: extensão de funcionalidade
- autocompletamento → autocompletion / tab completion

## Recursos

- [Oh My Zsh](https://ohmyz.sh/) — framework Zsh
- [Powerlevel10k](https://github.com/romkatv/powerlevel10k) — tema popular

## Veja também

- [[Linux]]
- [[Versionamento]]
- [[Docker]]
