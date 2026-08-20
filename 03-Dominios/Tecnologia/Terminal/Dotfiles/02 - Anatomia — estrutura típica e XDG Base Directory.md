---
title: "Anatomia — estrutura típica e XDG Base Directory"
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
  - xdg
  - anatomia
aliases:
  - XDG Base Directory
  - Anatomia dotfiles
---

# Anatomia — estrutura típica e XDG Base Directory

> [!abstract] TL;DR
> Dotfiles antigos vivem direto em `$HOME` (`~/.bashrc`, `~/.vimrc`). XDG Base Directory Specification (freedesktop.org) moderniza: `$XDG_CONFIG_HOME` (default `~/.config/`), `$XDG_DATA_HOME` (default `~/.local/share/`), `$XDG_CACHE_HOME` (default `~/.cache/`), `$XDG_STATE_HOME` (default `~/.local/state/`). Apps modernos (Neovim, Zellij, Lazygit) respeitam. Apps legados (bash, git, ssh) ignoram. Benefício prático: backup só de config; cache descartável limpo com `rm -rf`; `$HOME` não polui.

## O que é / Como funciona

### Layout legacy (anos 90/00)

Antes da XDG spec, cada aplicativo escolhia livremente onde guardar seus dados:

- Tudo direto em `$HOME`: `~/.bashrc`, `~/.vimrc`, `~/.gitconfig`, `~/.profile`
- Diretórios por app com convenções próprias: `.vim/`, `.emacs.d/`, `.mozilla/`, `.thunderbird/`
- Resultado: `ls -la ~` exibia dezenas de entradas `.algo` sem relação aparente

```bash
# Cenário típico pré-XDG
ls -la ~ | grep '^\.' | wc -l   # 40, 50, 60 entradas misturadas
```

Não havia distinção entre configuração (deveria sobreviver), cache (descartável) e dados persistentes do usuário. Tudo virava um blob em `$HOME`.

### Layout XDG

A XDG Base Directory Specification define quatro variáveis de ambiente principais, cada uma com um papel e um default:

| Variável | Default | Tipo de conteúdo |
|---|---|---|
| `$XDG_CONFIG_HOME` | `~/.config/` | Configuração do usuário (editada manualmente) |
| `$XDG_DATA_HOME` | `~/.local/share/` | Dados persistentes do usuário (history, bookmarks, ícones) |
| `$XDG_CACHE_HOME` | `~/.cache/` | Cache (descartável — pode ser deletado sem perda funcional) |
| `$XDG_STATE_HOME` | `~/.local/state/` | Estado de runtime (logs, undo history, última sessão) |

> [!info] Regra dos defaults
> Se a variável não estiver definida **ou** estiver definida com valor vazio (`""`), aplicativos devem usar os defaults acima. A spec é explícita: variável vazia equivale a não-definida — nunca use `export XDG_CONFIG_HOME=` sem valor.

Além dessas quatro, a convenção — não obrigatória pela spec — é `~/.local/bin/` para binários do usuário.

### Por que XDG existe

Quatro motivações principais:

1. **Separação de responsabilidades** — config, data, cache e state têm ciclos de vida distintos. Backup só de `~/.config/`; limpar `~/.cache/` quando o disco enche; nunca versionar `~/.local/state/`.

2. **Home respirável** — com apps respeitando XDG, `ls -la ~` mostra poucas entradas; a "sujeira" migra para subdiretórios organizados.

3. **Perfis alternativos** — `XDG_CONFIG_HOME=/tmp/perfil-teste zellij` isola completamente a config de um app para testar algo sem afetar o config real.

4. **Portabilidade multi-OS** — Linux moderno segue XDG amplamente; macOS tem equivalente parcial (`~/Library/`); BSD e WSL2 funcionam com o mesmo layout.

### Apps que respeitam XDG

Apps do stack moderno que seguem a spec por padrão:

- **Neovim** → `~/.config/nvim/`, `~/.local/share/nvim/`, `~/.cache/nvim/`
- **Zellij** → `~/.config/zellij/`, `~/.cache/zellij/`
- **Lazygit** → `~/.config/lazygit/`
- **Lazydocker** → `~/.config/lazydocker/`
- **fish** → `~/.config/fish/`
- **atuin** → `~/.config/atuin/`, `~/.local/share/atuin/`
- **helix** → `~/.config/helix/`
- **starship** → `~/.config/starship.toml`

### Apps que ignoram XDG

Apps legados que mantêm paths hard-coded em `$HOME`:

- **bash** → `~/.bashrc`, `~/.bash_profile`, `~/.bash_history`
- **ssh** → `~/.ssh/` (não há suporte oficial a `$XDG_CONFIG_HOME/ssh/`)
- **gpg** → `~/.gnupg/` (controlado por `$GNUPGHOME`, não pelas vars XDG)
- **vim** (não nvim) → `~/.vimrc`, `~/.vim/`
- **git** → `~/.gitconfig` por padrão (mas **aceita** `$XDG_CONFIG_HOME/git/config` se a variável estiver definida)

> [!tip] Git é um caso especial
> O git lê `$XDG_CONFIG_HOME/git/config` apenas se `~/.gitconfig` não existir. Para migrar, delete o `~/.gitconfig` após criar `~/.config/git/config` com o mesmo conteúdo — ou use `git config --global` que escreve no path encontrado.

### Como forçar XDG em app que ignora

Quatro estratégias, do mais ao menos recomendado:

**1. Env var própria do app** Muitos apps legados têm variável própria que sobrescreve o path:
```bash
# bash usa HISTFILE
export HISTFILE="$XDG_STATE_HOME/bash/history"
mkdir -p "${HISTFILE%/*}"

# zsh usa HISTFILE também
export HISTFILE="$XDG_STATE_HOME/zsh/history"
mkdir -p "${HISTFILE%/*}"
```

**2. Flag de linha de comando** Alguns apps aceitam `--config` ou `--config-dir` na invocação.

**3. Wrapper alias**
```bash
alias vim='vim -u "$XDG_CONFIG_HOME/vim/vimrc"'
```

**4. Aceitar e deixar legacy** Quando o app não tem mecanismo de override (ssh, gpg), simplesmente aceite o path legado e versione de lá. Forçar override em apps que não suportam causa mais problemas do que resolve.

### `~/.local/bin/`

Não é parte da XDG spec strict, mas é a convenção universal para binários do usuário:

- Equivale a `/usr/local/bin/` no escopo do usuário
- Usado por: `pip install --user`, `cargo install`, `go install`, scripts manuais
- Precisa estar no `$PATH` — não é adicionado automaticamente em todas as distros:

```bash
# Adicionar ao shell config (~/.zshenv ou ~/.profile)
export PATH="$HOME/.local/bin:$PATH"
```

```bash
# Verificar o que já está lá
ls -la ~/.local/bin/ 2>/dev/null
```

## Na prática

### Inventário XDG na máquina

Antes de qualquer setup, verifique o estado atual:

```bash
# Ver quais vars estão definidas (ou qual default será usado)
echo "CONFIG: ${XDG_CONFIG_HOME:-$HOME/.config (default)}"
echo "DATA:   ${XDG_DATA_HOME:-$HOME/.local/share (default)}"
echo "CACHE:  ${XDG_CACHE_HOME:-$HOME/.cache (default)}"
echo "STATE:  ${XDG_STATE_HOME:-$HOME/.local/state (default)}"

# Ver o que já existe em ~/.config
ls -la ~/.config/ 2>/dev/null | head -20

# Ver tamanho do cache
du -sh ~/.cache/ 2>/dev/null
```

Se as variáveis não estiverem definidas, os defaults já funcionam — apps modernos os reconhecem sem configuração extra.

### Setup XDG completo no shell

Para tornar o setup explícito e garantir compatibilidade máxima, defina as variáveis no arquivo lido por todos os shells — `~/.zshenv` para Zsh, `~/.profile` para bash/POSIX:

```zsh
# ~/.zshenv (carregado em todo shell Zsh — interativo ou não)

# XDG Base Directory (definir explicitamente com fallback pro default)
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# Forçar app legado: histórico do Zsh no lugar correto
export HISTFILE="$XDG_STATE_HOME/zsh/history"
mkdir -p "${HISTFILE%/*}"   # cria o dir se não existir

# Binários do usuário no PATH
export PATH="$HOME/.local/bin:$PATH"
```

> [!warning] Ordem importa em `.zshenv`
> As linhas que usam `$XDG_CONFIG_HOME` devem vir **depois** da linha que exporta a variável. Se você usa o padrão `${XDG_CONFIG_HOME:-$HOME/.config}` (fallback), a ordem fica automática.

### Limpar cache periódico

```bash
# Ver quais caches estão consumindo espaço
du -sh ~/.cache/* | sort -hr | head -10

# Deletar cache de app específico (seguro — será regenerado)
# rm -rf ~/.cache/nome-do-app/

# Exemplo: limpar cache do pip
# rm -rf ~/.cache/pip/
```

O cache é por definição descartável. Deletar qualquer entrada em `~/.cache/` nunca causa perda de dados — o pior caso é o app demorar mais na próxima execução enquanto reconstrói o cache.

## Armadilhas

### (1) Editar `$XDG_CACHE_HOME` esperando persistência

**Causa:** tratar `~/.cache/` como local de configuração ou dados permanentes.

**Sintoma:** mudanças em `~/.cache/<app>/` desaparecem — apps sobrescrevem o cache ao rodar.

**Como detectar:** verificar na documentação do app se o path em questão é `config`, `data` ou `cache`.

**Solução:** mover dados persistentes para `$XDG_DATA_HOME`. Config vai em `$XDG_CONFIG_HOME`.

---

### (2) `$XDG_CONFIG_HOME` definida com valor vazio

**Causa:** typo ou export sem valor: `export XDG_CONFIG_HOME=`.

**Sintoma:** apps procuram config em path absurdo (`/app/config.yml` em vez de `~/.config/app/config.yml`); erros de permissão ou config ignorada.

**Como detectar:**
```bash
echo "${XDG_CONFIG_HOME}"   # linha em branco = problema
```

**Solução:** se precisar definir, sempre com valor não-vazio. Se quiser usar o default, deixe a variável unset — não faça `export XDG_CONFIG_HOME=`.

---

### (3) Versionar `~/.cache/` por engano

**Causa:** configuração de GNU stow ou bare repo com whitelist mal-feita que inclui `~/.cache/`.

**Sintoma:** repositório de dotfiles cresce para centenas de MB; `git status` cheio de ruído de cache.

**Como detectar:**
```bash
du -sh .git/    # repo grande demais é sinal
```

**Solução:** adicionar `~/.cache/` e `~/.local/state/` explicitamente ao `.gitignore` do repo de dotfiles.

---

### (4) App escreve em `~/.app/` em vez de `~/.config/app/`

**Causa:** app que não respeita XDG — escreve diretamente em `$HOME`.

**Sintoma:** novo diretório `.appname/` aparece em `$HOME` mesmo com `XDG_CONFIG_HOME` definido.

**Como detectar:**
```bash
ls -la ~ | grep '^\.'    # listar todos os dotfiles/dotdirs em $HOME
```

**Solução:** verificar se o app aceita env var própria ou flag `--config`; se não aceitar, versionar de onde está em `$HOME` mesmo — não tente forçar um app que não suporta.

---

### (5) Confundir `~/.local/share/` (data) com `~/.local/bin/` (binários)

**Causa:** os dois paths começam com `~/.local/` e parecem relacionados pela proximidade.

**Sintoma:** binário instalado em `~/.local/share/` não roda (não está no `$PATH`); ou dados de app colocados em `~/.local/bin/` quebram organização.

**Como detectar:** `~/.local/bin/` deve conter apenas arquivos executáveis; `~/.local/share/` contém subdirs por app.

**Solução:** `~/.local/bin/` é exclusivo para executáveis; `~/.local/share/<app>/` para dados persistentes.

---

### (6) Definir XDG vars em `~/.zshrc` em vez de `~/.zshenv`

**Causa:** colocar os exports de XDG em `~/.zshrc`, que é carregado apenas em shells interativos.

**Sintoma:** apps lançados via script, systemd user units ou ferramentas de build não encontram `$XDG_CONFIG_HOME` — usam defaults ou falham.

**Como detectar:**
```bash
zsh --no-rcs -c 'echo $XDG_CONFIG_HOME'   # deve mostrar o valor; se vazio, está no lugar errado
```

**Solução:** exports de variáveis de ambiente base vão em `~/.zshenv` (carregado em todo Zsh) ou `~/.profile` (POSIX, carregado por login shells e gestores de sessão).

## Em inglês

- **spec** / **specification** — *especificação*. "Documento técnico que define regras ou padrões."
- **base directory** — *diretório base*. "Diretório raiz a partir do qual outros paths são derivados."
- **environment variable** — *variável de ambiente*. "Variável do processo acessível a todos os subprocessos; define comportamento sem alterar código."
- **fallback** — *fallback* (ou *valor de reserva*). "Valor usado quando a configuração principal não está disponível ou está vazia."
- **cache** — *cache*. "Dados temporários gerados automaticamente e descartáveis; pode ser deletado sem perda funcional."
- **state** — *estado*. "Dados de runtime persistidos entre sessões — histórico, undo, última posição — mas não configuração."
- **namespace** — *namespace* (ou *espaço de nomes*). "Subdirectory por app em `~/.config/<app>/` que evita colisão de nomes entre aplicativos."
- **legacy** — *legado*. "Aplicativo ou comportamento que antecede um padrão moderno e ainda mantém convenção antiga."
- **convention** — *convenção*. "Acordo informal (não spec obrigatória) adotado pela comunidade — como `~/.local/bin/`."
- **override** — *sobrescrever* / *override*. "Definir variável ou flag que substitui o comportamento default de um app."

## Veja também

- [[01 - Princípios — o que são dotfiles e por que versionar]] — pré-requisito desta nota
- [[03 - Cross-OS — Linux vs macOS vs WSL]] — como XDG se comporta em outros sistemas operacionais
- [[04 - GNU stow — symlinks declarativos]] — GNU stow respeita XDG naturalmente
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#XDG Base Directory|XDG Base Directory]], [[Dicionário do Terminal#Dotfile|dotfile]]

## Referências

- [XDG Base Directory Specification — freedesktop.org](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [Arch Wiki — XDG Base Directory](https://wiki.archlinux.org/title/XDG_Base_Directory)
