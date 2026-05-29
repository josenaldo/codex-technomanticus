---
title: "GNU stow — symlinks declarativos"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - dotfiles
  - adepto
  - stow
  - symlink
aliases:
  - GNU stow
  - Stow
---

# GNU stow — symlinks declarativos

> [!abstract] TL;DR
> GNU stow é o gerenciador de dotfiles mais simples: 1 pasta por "package" no repo, `stow <pkg>` cria symlinks no home com a mesma estrutura. Exemplo: `~/dotfiles/zsh/.zshrc` + `stow zsh` → `~/.zshrc` (symlink). `stow -D` unstow; `stow -R` restow; `--adopt` adota files existentes. Vantagens: simples, sem state file, Unix-nativo. Desvantagens: sem templates, sem cross-OS automático, sem secrets nativos.

## O que é / Como funciona

### Conceito básico

GNU stow se descreve como um "symlink farm manager" — gerenciador de fazendas de symlinks. O nome "stow" vem de "stow away" (guardar de forma organizada).

A filosofia central é simples:

- Você mantém seus dotfiles no repo (`~/dotfiles/`)
- O stow cria symlinks no home apontando para esses arquivos
- Resultado bidirecional: edita no repo → mudança aparece no home; edita no home via symlink → mudança vai pro repo

Isso significa que você nunca perde o vínculo com o controle de versão. O repo é a única fonte de verdade; o home é apenas um espelho de symlinks.

O stow foi originalmente criado para gerenciar instalações de software (pacotes compilados em `/usr/local`), mas é amplamente adotado para dotfiles porque a mecânica é idêntica: um diretório espelha sua estrutura em outro via symlinks.

### Estrutura repo stow-friendly

O stow organiza o repo em "packages" — cada subdiretório direto do repo é um package independente:

```text
~/dotfiles/
├── zsh/
│   ├── .zshrc
│   └── .zshenv
├── nvim/
│   └── .config/
│       └── nvim/
│           └── init.lua
└── git/
    └── .gitconfig
```

A regra fundamental: **a estrutura dentro do package replica o path relativo a `$HOME`**. Ou seja:

- `dotfiles/zsh/.zshrc` → `~/.zshrc`
- `dotfiles/nvim/.config/nvim/init.lua` → `~/.config/nvim/init.lua`
- `dotfiles/git/.gitconfig` → `~/.gitconfig`

O stow remove mentalmente o prefixo do package e cria symlinks com o restante do path a partir do target (default: `$HOME`).

### Comandos essenciais

O stow assume que o target é o diretório pai do atual. Por isso, o fluxo canônico é sempre `cd ~/dotfiles && stow <pkg>`:

```bash
cd ~/dotfiles

stow zsh              # cria ~/.zshrc e ~/.zshenv como symlinks
stow -D zsh           # remove os symlinks (arquivos no repo intactos)
stow -R zsh           # restow: unstow + stow (útil após mover arquivos)
stow -v zsh           # verbose: mostra cada symlink criado
stow -n zsh           # dry-run: simula sem criar nada
stow -n -v zsh        # dry-run verbose: ideal pra checar antes de aplicar

# Target e diretório explícitos (quando não estiver em ~/dotfiles)
stow -t ~ -d ~/dotfiles zsh

# Stow múltiplos packages de uma vez
stow zsh nvim git tmux

# Adotar file existente no home: move pro repo e cria symlink
stow --adopt zsh
```

### Conflict handling

Se `~/.zshrc` já existe como arquivo real (não-symlink) e você executa `stow zsh`, o stow **falha com aviso** antes de fazer qualquer coisa:

```text
WARNING! stowing zsh would cause conflicts:
  * existing target is neither a link nor a directory: .zshrc
All operations aborted.
```

O stow nunca sobrescreve silenciosamente. Três caminhos para resolver:

1. **Backup manual e remove**: `mv ~/.zshrc ~/.zshrc.bak && stow zsh`
2. **Adopt**: `stow --adopt zsh` (veja seção abaixo)
3. **Mover manualmente pro repo**: `mv ~/.zshrc ~/dotfiles/zsh/.zshrc && stow zsh`

Se o target já é um symlink apontando para outro lugar, o stow também falha — ele não substituiria symlinks existentes sem `-R`.

### O que `stow --adopt` faz

O `--adopt` resolve conflitos movendo o arquivo do home para o repo e então criando o symlink:

1. Move `~/.zshrc` para `~/dotfiles/zsh/.zshrc`
2. Cria `~/.zshrc` como symlink apontando para `~/dotfiles/zsh/.zshrc`

O resultado final é o mesmo que o fluxo manual. A diferença está em **quem decide o conteúdo**: o `--adopt` usa a versão que estava no home, não a que estava no repo.

> **Atenção:** se o repo já tinha um `.zshrc`, `--adopt` vai **sobrescrever a versão do repo com a versão do home**. Faça sempre `git status` antes de usar `--adopt`.

### Limitações

O stow é propositalmente simples. Essa simplicidade tem um custo:

1. **Sem templates** — o stow não processa lógica condicional. Um `.zshrc` não pode ter blocos `{% if os == "macos" %}`. Para templates, veja [[05 - chezmoi — manager completo com templates]].
2. **Sem cross-OS automático** — para configurações específicas por OS, você precisa de packages separados (`zsh-linux/`, `zsh-macos/`) e um script de bootstrap que chama o correto.
3. **Sem secrets nativos** — o stow não oferece nenhum mecanismo de criptografia. Secrets ficam fora do repo ou em solução externa (age, git-crypt, chezmoi secrets).
4. **Sem state file** — vantagem e desvantagem. Sem estado, não há como perguntar "o que está stowado?". Você descobre via `ls -la ~` e `readlink`.
5. **Sem detecção de orphans automática** — symlinks quebrados após mover arquivos ficam até você rodar `stow -R` ou `find` manual.

## Na prática

### Setup inicial

O fluxo canônico para começar um repo de dotfiles com stow:

```bash
# 1. Criar repo
mkdir -p ~/dotfiles
cd ~/dotfiles
git init

# 2. Criar package para zsh
mkdir -p zsh

# 3. Mover dotfile existente pro package (preserva conteúdo)
mv ~/.zshrc zsh/.zshrc

# 4. Stow o package (cria symlink)
stow zsh

# 5. Confirmar: deve mostrar -> .../dotfiles/zsh/.zshrc
ls -la ~/.zshrc

# 6. Commit
git add zsh/
git commit -m "add zsh package"
```

O `ls -la` deve mostrar algo como:

```text
lrwxrwxrwx 1 alice alice 28 mai 22 10:00 /home/alice/.zshrc -> dotfiles/zsh/.zshrc
```

### Adicionar mais packages

Para adicionar nvim ao repo (seguindo XDG):

```bash
# Criar estrutura espelhando o path real
mkdir -p ~/dotfiles/nvim/.config/nvim

# Mover config existente
mv ~/.config/nvim/init.lua ~/dotfiles/nvim/.config/nvim/init.lua

# Stow
cd ~/dotfiles && stow nvim

# Verificar
ls -la ~/.config/nvim/init.lua
```

### Aplicar tudo numa máquina nova

Esse é o momento em que o stow brilha — setup de máquina nova em segundos:

```bash
# Clonar o repo
git clone https://github.com/alice/dotfiles ~/dotfiles

# Entrar no repo
cd ~/dotfiles

# Verificar antes de aplicar (dry-run)
stow -n -v zsh nvim git tmux

# Aplicar tudo
stow zsh nvim git tmux
```

Se a máquina nova tiver configs default nos paths (ex: `.bashrc` padrão da distro), o stow vai falhar no conflict. Solução: `stow --adopt` ou backup + remove manual.

### Cross-OS com stow (manual)

O stow não tem cross-OS nativo. A estratégia manual é packages separados por OS:

```text
~/dotfiles/
├── zsh-linux/
│   └── .zshrc          # config com aliases linux
├── zsh-macos/
│   └── .zshrc          # config com aliases macOS
└── shared/
    └── .gitconfig      # igual em todos os OS
```

No script de bootstrap:

```bash
case "$(uname -s)" in
  Linux*)  cd ~/dotfiles && stow zsh-linux shared ;;
  Darwin*) cd ~/dotfiles && stow zsh-macos shared ;;
esac
```

Para lógica mais elaborada de cross-OS, [[05 - chezmoi — manager completo com templates]] oferece templates com condicionais.

## Armadilhas

### (1) `stow` em diretório errado cria symlinks em path inesperado

**Causa:** o stow assume que o target é o diretório pai do cwd. Se você executar `stow zsh` de `~/dotfiles/zsh/` em vez de `~/dotfiles/`, o target será `~/dotfiles/` e os symlinks serão criados lá, não em `$HOME`.

**Sintoma:** `~/.zshrc` não foi criado; em vez disso aparece `~/dotfiles/.zshrc` como symlink apontando para `~/dotfiles/zsh/.zshrc`.

**Como detectar:** `ls -la ~/.zshrc` não mostra nada; `ls -la ~/dotfiles/` mostra symlinks inesperados.

**Solução:** sempre `cd ~/dotfiles && stow <pkg>` — jamais execute stow de dentro do package. Ou use explicitamente `stow -t ~ -d ~/dotfiles <pkg>` para deixar os paths sem ambiguidade.

---

### (2) Stow recusa quando o home tem file real existente

**Causa:** o stow se recusa a sobrescrever silenciosamente arquivos existentes no target. É um comportamento de segurança intencional.

**Sintoma:** `WARNING! stowing zsh would cause conflicts: * existing target is neither a link nor a directory: .zshrc` + `All operations aborted.`

**Como detectar:** ler a mensagem de erro — o stow é explícito sobre qual arquivo causa o conflict.

**Solução:** três opções em ordem de controle crescente: (a) `stow --adopt zsh` (adota versão do home); (b) `mv ~/.zshrc ~/.zshrc.bak && stow zsh` (backup manual); (c) mover manualmente para o repo e então stow.

---

### (3) `--adopt` sobrescreve a versão do repo com a versão do home

**Causa:** o `--adopt` foi projetado para "adotar" arquivos que ainda não estão no repo. Se o repo já tem uma versão do arquivo, o `--adopt` move a versão do home (possivelmente mais antiga) sobre ela.

**Sintoma:** mudanças recentes no repo desaparecem; `git diff` mostra conteúdo revertido.

**Como detectar:** `git status` e `git diff` antes de qualquer `--adopt` revelam o que seria perdido.

**Solução:** regra invariável — só use `--adopt` com `git status` mostrando working tree limpo; ou faça commit antes; ou copie manualmente e revise o diff antes de sobrescrever.

---

### (4) Arquivos em `~/.config/` precisam de estrutura aninhada no package

**Causa:** o stow replica a estrutura de dentro do package a partir de `$HOME`. Para que `~/.config/nvim/init.lua` seja criado, o package precisa ter exatamente `nvim/.config/nvim/init.lua` — não apenas `nvim/init.lua`.

**Sintoma:** `stow nvim` cria `~/.config/` como symlink para a pasta inteira `~/dotfiles/nvim/.config/`, em vez de criar symlinks individuais dentro de `~/.config/`. Ou pior: `~/.config/` não é criado e o arquivo simplesmente não aparece.

**Como detectar:** `stow -v -n nvim` (dry-run verbose) mostra exatamente quais symlinks seriam criados antes de aplicar.

**Solução:** a estrutura do package replica o path absoluto sem o `$HOME`:
- `nvim/.config/nvim/init.lua` → `~/.config/nvim/init.lua`
- `nvim/.config/nvim/lua/plugins/` → `~/.config/nvim/lua/plugins/`

---

### (5) Stow re-aplicado após mover arquivo dentro do package deixa symlinks quebrados

**Causa:** o stow não rastreia movimentos de arquivo. Se você mover `dotfiles/zsh/.zshrc` para `dotfiles/zsh/.config/zsh/.zshrc`, o symlink antigo `~/.zshrc` continua apontando para o path anterior (que não existe mais).

**Sintoma:** `~/.zshrc` aponta para um arquivo que não existe mais; o shell pode falhar ao carregar.

**Como detectar:** `find ~ -maxdepth 3 -xtype l 2>/dev/null` lista todos os symlinks quebrados (dangling). Ou `ls -la ~/.zshrc` mostra o path do alvo — verificar se existe.

**Solução:** após qualquer reestruturação interna do package, execute `stow -R <pkg>` (restow): remove os symlinks antigos e cria os novos conforme a estrutura atual.

---

### (6) `.stow-local-ignore` custom desativa a lista de ignore padrão

**Causa:** ao criar `.stow-local-ignore` no repo, você substitui completamente a lista padrão — ela não é meramente estendida.

**Sintoma:** o stow começa a criar symlinks para `README.md`, `LICENSE`, `.git/`, que antes eram ignorados automaticamente.

**Como detectar:** `stow -v -n .` mostra os symlinks que seriam criados, incluindo indesejados.

**Solução:** ao criar `.stow-local-ignore`, inclua explicitamente o que a lista padrão cobre: `\.git`, `README.*`, `LICENSE.*`, `COPYING`, `Makefile`, e qualquer arquivo que não deve ir para `$HOME`.

## Em inglês

- **symlink** — *link simbólico*. "Arquivo no filesystem que aponta para outro path; base de funcionamento do stow."
- **package** — *pacote* (no contexto stow). "Subdiretório do repo stow que agrupa dotfiles de um app."
- **target** — *alvo*. "Diretório onde os symlinks são criados; default é o parent do stow dir (`$HOME`)."
- **source** — *fonte*. "Diretório do repo onde os arquivos reais residem (`~/dotfiles/`)."
- **adopt** — *adotar*. "Operação `--adopt`: move arquivo existente do home para o repo e cria symlink no lugar."
- **conflict** — *conflito*. "Situação em que o target já contém um arquivo real (não-symlink) no path onde stow quer criar um symlink."
- **dry-run** — *simulação*. "Execução de `stow -n` que mostra o que seria feito sem modificar nada."
- **declarative** — *declarativo*. "Abordagem onde você descreve o estado desejado (estrutura de pastas) e a ferramenta realiza."
- **idempotent** — *idempotente*. "Rodar `stow <pkg>` múltiplas vezes produz o mesmo resultado; não duplica symlinks."
- **restow** — *re-stowar*. "Operação `stow -R`: remove symlinks antigos e recria; útil após reestruturar o package."

## Veja também

- [[01 - Princípios — o que são dotfiles e por que versionar]] — pré-requisito: por que versionar dotfiles
- [[02 - Anatomia — estrutura típica e XDG Base Directory]] — pré-requisito: entender paths XDG antes de estruturar packages
- [[05 - chezmoi — manager completo com templates]] — alternativa com templates e cross-OS automático
- [[06 - Bare git repo — abordagem minimalista]] — alternativa sem dependência externa
- [[07 - Secrets em dotfiles — git-crypt, age, sops]] — secrets e arquivos sensíveis em dotfiles
- [[08 - Bootstrap — máquina nova zero-to-ready]] — usa stow no script de bootstrap
- [[03-Dominios/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Stow|stow]], [[Dicionário do Terminal#Symlink|symlink]]

## Referências

- GNU stow — página oficial: https://www.gnu.org/software/stow/
- GNU stow manual: https://www.gnu.org/software/stow/manual/stow.html
