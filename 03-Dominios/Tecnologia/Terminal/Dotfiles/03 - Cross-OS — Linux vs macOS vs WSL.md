---
title: "Cross-OS — Linux vs macOS vs WSL"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - dotfiles
  - iniciado
  - cross-os
  - macos
  - wsl
aliases:
  - Cross-OS dotfiles
---

# Cross-OS — Linux vs macOS vs WSL

> [!abstract] TL;DR
> Dotfiles que funcionam em Linux podem quebrar em macOS ou WSL. Diferenças críticas: paths (`/home/<user>` vs `/Users/<user>`), shell default (bash GNU vs zsh em macOS ≥ Catalina), package manager (apt/dnf vs brew vs scoop), GNU vs BSD utilities (`sed -i` tem syntax diferente). Quando dotfile precisa ramificar: env var `OSTYPE` ou `uname -s`, chezmoi templates, ou script externo. WSL especificidade: interop com Windows via `/mnt/c/`; I/O cross-filesystem é lento; trabalhar em `/home/<user>/`.

## O que é / Como funciona

### Paths de home

O caminho do diretório home do usuário **não é o mesmo** em todos os sistemas:

| OS | Path do home |
|---|---|
| Linux | `/home/<user>` |
| macOS | `/Users/<user>` |
| WSL (Linux) | `/home/<user>` dentro da distro |
| WSL → Windows | `/mnt/c/Users/<user>/` (Windows visto do WSL) |

A regra é simples: **nunca hardcode o path do home**. Sempre use `$HOME` ou `~`:

```bash
# ERRADO — quebra em macOS
export PROJECTS=/home/alice/projects

# CERTO — funciona em todos os sistemas
export PROJECTS="$HOME/projects"
```

### Shell default

O shell default varia por sistema operacional e até por versão:

| OS / Versão | Shell default |
|---|---|
| Linux (Debian/Ubuntu/Fedora) | bash |
| Linux (Arch, Manjaro) | bash (mas muitos usuários usam zsh) |
| macOS ≥ Catalina (2019) | zsh |
| macOS < Catalina | bash 3.2 (antigo, sem atualização por licença GPL) |
| WSL | depende da distro instalada |

> [!note] Por que macOS mudou pra zsh em 2019?
> O bash incluído no macOS era travado na versão 3.2 (2007) por causa da licença GPLv3 — a Apple não queria incluir software GPLv3. O zsh tem licença MIT, então a Apple adotou-o como default a partir do macOS Catalina (10.15). O bash ainda está disponível em `/bin/bash`, mas a Apple exibe um aviso pedindo para mudar de shell.

### Package manager

Não existe um package manager universal. Cada ecossistema tem o seu:

| OS | Package manager | Instalar um pacote |
|---|---|---|
| Linux Debian/Ubuntu | apt | `sudo apt install <pkg>` |
| Linux Fedora/RHEL | dnf | `sudo dnf install <pkg>` |
| Linux Arch | pacman | `sudo pacman -S <pkg>` |
| macOS | Homebrew | `brew install <pkg>` |
| WSL | package manager da distro | igual ao Linux |

Dotfiles que instalam dependências precisam detectar o OS e chamar o manager certo.

### GNU vs BSD utilities

macOS usa as **BSD utilities** herdadas do FreeBSD, enquanto Linux usa as **GNU utilities** (coreutils). O nome do comando é o mesmo, mas a syntax pode ser diferente — e às vezes o erro é silencioso.

**`sed -i` (edição in-place):**

```bash
# GNU (Linux, WSL)
sed -i 's/foo/bar/' arquivo.txt

# BSD (macOS) — requer argumento de extensão pra backup
sed -i '' 's/foo/bar/' arquivo.txt

# Workaround portável: cria arquivo .bak em ambos
sed -i.bak 's/foo/bar/' arquivo.txt
```

**`grep -P` (Perl regex):**

```bash
# GNU grep — suportado
grep -P '\d+' arquivo.txt

# BSD grep (macOS) — não suportado por default
# Solução: brew install grep && usar ggrep
ggrep -P '\d+' arquivo.txt
```

**`readlink -f` e `realpath`:**

```bash
# GNU — ambos disponíveis nativamente
readlink -f /caminho/relativo
realpath /caminho/relativo

# BSD (macOS) — readlink sem -f; realpath precisa coreutils
brew install coreutils
greadlink -f /caminho/relativo
```

**`date` formatting:**

```bash
# GNU — aceita expressões em linguagem natural
date -d 'yesterday' '+%Y-%m-%d'

# BSD (macOS) — syntax diferente com ajustes numéricos
date -v-1d '+%Y-%m-%d'
```

### Quando dotfile precisa branch por OS

Nem todo dotfile precisa de lógica condicional. O branch por OS é necessário quando:

- O comando tem syntax diferente (GNU vs BSD)
- O path é diferente (Homebrew em Intel vs Apple Silicon)
- O comportamento esperado é diferente (clipboard, interop)
- Uma ferramenta só existe em um OS

A forma mais simples de detectar o OS em shell:

```bash
# Via OSTYPE (disponível em bash e zsh)
case "$OSTYPE" in
  linux-gnu*)    OS=linux ;;
  darwin*)       OS=macos ;;
  msys*|cygwin*) OS=windows ;;
  *)             OS=unknown ;;
esac

# Via uname -s (mais portável, funciona em sh puro)
case "$(uname -s)" in
  Linux*)  OS=linux ;;
  Darwin*) OS=macos ;;
  *)       OS=unknown ;;
esac
```

Detecção específica de WSL (Linux, mas com especificidades):

```bash
# WSL expõe "microsoft" em /proc/version
if grep -qi microsoft /proc/version 2>/dev/null; then
  OS=wsl
fi
```

### WSL — especificidades

O WSL2 (Windows Subsystem for Linux 2) roda um kernel Linux real dentro de uma VM leve gerenciada pelo Windows. Do ponto de vista do shell, é Linux — mas com algumas particularidades importantes para dotfiles.

**Filesystem cross-OS:**

| Path | O que é |
|---|---|
| `/home/<user>/` | Home Linux dentro da distro (filesystem nativo) |
| `/mnt/c/Users/<user>/` | Home Windows visto do WSL via 9P filesystem |
| `\\wsl$\Ubuntu\` | Distro WSL vista do Windows Explorer |

**Interop com Windows:**

O WSL2 permite chamar executáveis Windows diretamente do terminal Linux:

```bash
cmd.exe /c dir          # cmd do Windows
powershell.exe -c "..."  # PowerShell
explorer.exe .           # abre o Explorer no diretório atual
notepad.exe arquivo.txt  # abre o Bloco de Notas
```

**Clipboard:**

```bash
# Copiar output pra área de transferência do Windows
echo "texto" | clip.exe

# Colar da área de transferência
powershell.exe -c "Get-Clipboard"
```

**Tradução de paths com `wslpath`:**

```bash
# Linux path → Windows path
wslpath -w ~/projetos/foo
# resultado: \\wsl$\Ubuntu\home\alice\projetos\foo

# Windows path → Linux path
wslpath -u 'C:\Users\Alice\Documents'
# resultado: /mnt/c/Users/Alice/Documents
```

**Rede:**

O WSL2 tem seu próprio namespace de rede com um IP dedicado — diferente do WSL1, que compartilhava o IP do Windows. Isso afeta acesso a serviços rodando no host Windows (ex.: banco de dados em `localhost`).

## Na prática

### Setup OS detection completo no zsh

O lugar certo para definir `DOTFILES_OS` é o `~/.zshenv`, que é carregado antes de tudo — inclusive em shells não-interativos:

```zsh
# ~/.zshenv
case "$(uname -s)" in
  Linux*)
    if grep -qi microsoft /proc/version 2>/dev/null; then
      export DOTFILES_OS=wsl
    else
      export DOTFILES_OS=linux
    fi
    ;;
  Darwin*)
    export DOTFILES_OS=macos
    ;;
  *)
    export DOTFILES_OS=unknown
    ;;
esac
```

### Conditional source no shell rc

Com `DOTFILES_OS` definido, o `~/.zshrc` pode carregar um arquivo específico do OS:

```zsh
# ~/.zshrc
# Carrega configurações específicas do OS (se existirem)
[[ -f "$HOME/.config/zsh/$DOTFILES_OS.zsh" ]] && source "$HOME/.config/zsh/$DOTFILES_OS.zsh"
```

Estrutura resultante nos dotfiles:

```
~/.config/zsh/
├── linux.zsh    # aliases/configs exclusivos do Linux
├── macos.zsh    # aliases/configs exclusivos do macOS
└── wsl.zsh      # aliases/configs exclusivos do WSL
```

Aliases condicionais direto no `~/.zshrc`:

```zsh
if [[ "$DOTFILES_OS" == "macos" ]]; then
  alias ls='gls --color=auto'  # GNU ls via brew (coreutils)
else
  alias ls='ls --color=auto'
fi
```

### macOS — corrigir GNU vs BSD

Se você quer usar a mesma syntax de sed/grep/date do Linux no macOS, instale as GNU utilities via Homebrew e coloque-as no início do PATH:

```bash
# Instalar GNU utilities
brew install coreutils gnu-sed grep findutils

# Em ~/.config/zsh/macos.zsh
# Apple Silicon: /opt/homebrew/  |  Intel: /usr/local/
eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"

export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"
export PATH="/opt/homebrew/opt/gnu-sed/libexec/gnubin:$PATH"
export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"
```

> [!warning] Intel vs Apple Silicon
> O Homebrew usa paths diferentes dependendo da arquitetura: `/opt/homebrew/` em Apple Silicon (M1/M2/M3) e `/usr/local/` em Intel. O `eval "$(...brew shellenv)"` lida com isso automaticamente — use-o sempre em vez de hardcodar o path.

### WSL — abrir Windows path do bash

Alguns comandos úteis para integração entre WSL e Windows:

```bash
# Abrir Explorer no diretório atual do WSL
explorer.exe .

# Abrir VS Code no projeto atual (via WSL extension)
code .

# Converter path WSL → Windows
wslpath -w ~/projetos/meu-projeto
# \\wsl$\Ubuntu\home\alice\projetos\meu-projeto

# Converter path Windows → WSL
wslpath -u 'C:\Users\Alice\Downloads'
# /mnt/c/Users/Alice/Downloads

# Copiar path atual para clipboard do Windows
pwd | clip.exe
```

## Armadilhas

### (1) Dotfile com `/home/<user>` hardcoded falha em macOS

**Causa:** macOS usa `/Users/<user>` como home; qualquer path `/home/algo` simplesmente não existe.

**Sintoma:** comandos falham com "No such file or directory" em macOS, mas funcionam perfeitamente em Linux.

**Como detectar:** `grep -r '/home/' ~/dotfiles/` — qualquer hit é candidato ao problema.

**Solução:** substituir todo `/home/<user>` por `$HOME` ou `~`.

---

### (2) `sed -i 's/a/b/' file` quebra em macOS sem warning visível

**Causa:** o BSD sed exige que `-i` receba um argumento (sufixo do backup) — mesmo que vazio.

**Sintoma:** em Linux funciona; em macOS o comando cria um arquivo chamado literalmente `s/a/b/` e não edita o original.

**Como detectar:** rodar o script em macOS e verificar o diretório — aparece um arquivo com nome estranho.

**Solução:** usar `sed -i.bak 's/a/b/' file` (funciona em GNU e BSD) ou instalar `gnu-sed` via brew.

---

### (3) Brew path errado em Apple Silicon vs Intel

**Causa:** Homebrew mudou o prefix de `/usr/local/` para `/opt/homebrew/` no Apple Silicon (M1+).

**Sintoma:** apps instalados via brew não estão no PATH; `which brew` retorna nothing ou path errado.

**Como detectar:** `arch` mostra `arm64` (Apple Silicon) ou `x86_64` (Intel); `which brew` confirma o prefix.

**Solução:** usar `eval "$(brew shellenv)"` no lugar de hardcodar o PATH — o brew já sabe onde está.

---

### (4) WSL — I/O em `/mnt/c/` é 10x mais lento que em `/home/`

**Causa:** o acesso ao filesystem Windows pelo WSL2 passa pelo protocolo 9P, que tem overhead significativo de IPC.

**Sintoma:** `npm install` em `/mnt/c/projeto` leva 5 minutos; o mesmo comando em `/home/<user>/projeto` leva 30 segundos.

**Como detectar:** comparar o tempo de operações pesadas de I/O nos dois locais — a diferença é imediata.

**Solução:** trabalhar sempre em `/home/<user>/`; usar `/mnt/c/` apenas pra acessar arquivos Windows pontuais.

---

### (5) Versionar shell rc do WSL como `linux.zsh` perde as especificidades

**Causa:** WSL é tecnicamente Linux, mas tem particularidades únicas — interop com Windows, clipboard via `clip.exe`, paths via `wslpath`.

**Sintoma:** `linux.zsh` é sourcejado no WSL, mas não tem as configs de interop; ou configs de interop entram no `linux.zsh` e quebram em Linux puro.

**Como detectar:** testar o mesmo `linux.zsh` em uma VM Linux real — os comandos Windows não existem lá.

**Solução:** detectar WSL separadamente (`grep -qi microsoft /proc/version`) e manter um `wsl.zsh` dedicado.

---

### (6) macOS bash antigo pode quebrar scripts modernos

**Causa:** o bash do macOS é 3.2 (2007) por restrição de licença; arrays associativos (`declare -A`) foram adicionados no bash 4.

**Sintoma:** script com `declare -A mapa` funciona no Linux (bash 5.x) e falha no macOS com "syntax error".

**Como detectar:** rodar `bash --version` no macOS — se mostrar 3.x, o ambiente é afetado.

**Solução:** ou instalar bash moderno via `brew install bash`, ou migrar o script para zsh, ou evitar features de bash 4+.

## Em inglês

Termos usados em contextos de dotfiles cross-platform e entrevistas técnicas:

- **cross-platform** → portável entre sistemas operacionais; "my dotfiles are cross-platform"
- **OS detection** → detecção de sistema operacional em tempo de execução; "the script does OS detection via `uname`"
- **package manager** → gerenciador de pacotes; "Homebrew is the de facto package manager on macOS"
- **utility / CLI utility** → ferramenta de linha de comando; "GNU utilities behave differently from BSD utilities"
- **interop** → interoperabilidade; "WSL2 has Windows interop — you can call `explorer.exe` from bash"
- **path translation** → tradução de caminho entre sistemas de arquivo; "`wslpath` handles path translation between WSL and Windows"
- **native** → nativo, rodando diretamente no OS sem camada de abstração; "prefer working in the native Linux filesystem"
- **portable** → portável, que funciona em múltiplos ambientes; "use `$HOME` instead of `/home/user` to keep the script portable"
- **abstract away** → abstrair, esconder detalhes de implementação; "the detection function abstracts away the OS differences"
- **branching** (em dotfiles) → lógica condicional por OS; "use branching in your `.zshrc` to handle macOS vs Linux differences"

## Veja também

- [[01 - Princípios — o que são dotfiles e por que versionar]] — pré-requisito: conceito base de dotfile
- [[02 - Anatomia — estrutura típica e XDG Base Directory]] — pré-requisito: estrutura de arquivos
- [[05 - chezmoi — manager completo com templates]] — templates resolvem cross-OS de forma declarativa
- [[09 - Sync entre máquinas heterogêneas]] — sync entre OSes diferentes na prática
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#WSL|WSL]], [[Dicionário do Terminal#Dotfile|dotfile]]

## Referências

- Microsoft. *What is Windows Subsystem for Linux* — https://learn.microsoft.com/en-us/windows/wsl/
- Apple. *Use zsh as the default shell on your Mac* — https://support.apple.com/en-us/102360
