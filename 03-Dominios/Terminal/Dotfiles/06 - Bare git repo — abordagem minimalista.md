---
title: "Bare git repo — abordagem minimalista"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - dotfiles
  - adepto
  - bare-repo
  - git
aliases:
  - Bare repo dotfiles
---

# Bare git repo — abordagem minimalista

> [!abstract] TL;DR
> Bare git repo = abordagem minimalista — só git, zero ferramentas extras. `git init --bare $HOME/.dotfiles` cria repo separado do working tree; `--work-tree=$HOME` faz tracking direto no home. Alias `dotfiles` no shell substitui `git`. `.gitignore` é whitelist (`*` + `!arquivo` específico). Vantagens: nada pra instalar, máxima portabilidade. Desvantagens: sem templates, sem secrets, sem cross-OS automático.

## O que é / Como funciona

### Conceito básico

Um **bare** git repo é um repo **sem working tree** — contém apenas os metadados internos do git (o que normalmente vive em `.git/`), sem os arquivos do projeto em si. Tradicionalmente, bare repos ficam em servidores para receber `git push` (ex: `git clone --bare`).

O truque para dotfiles: criar um bare repo localmente em `$HOME/.dotfiles/`, mas forçar o **working tree** para `$HOME`. O resultado: o git rastreia arquivos que existem em `$HOME` diretamente, sem precisar de um `.git/` no home.

Essa abordagem foi popularizada em 2016 num thread do Hacker News (item #11070797) e se tornou canônica pela elegância: **nenhuma ferramenta extra** — só git.

### Setup canônico

```bash
git init --bare "$HOME/.dotfiles"
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
```

O que cada linha faz:

- `git init --bare "$HOME/.dotfiles"` — cria o bare repo (só metadados git, sem working tree).
- `alias dotfiles='...'` — cria atalho que injeta `--git-dir` e `--work-tree` a cada comando. A partir daqui, `dotfiles` substitui `git` para gerenciar dotfiles.
- `status.showUntrackedFiles no` — oculta os milhares de arquivos não-rastreados em `$HOME` no output de `dotfiles status`.

O alias deve ser persistido no `~/.zshrc` (ou `~/.bashrc`) para sobreviver a reinicializações:

```bash
echo "alias dotfiles='git --git-dir=\$HOME/.dotfiles --work-tree=\$HOME'" >> ~/.zshrc
source ~/.zshrc
```

### Workflow básico

Após o setup, a operação é idêntica ao git normal — só troca `git` por `dotfiles`:

```bash
dotfiles add ~/.zshrc
dotfiles add ~/.gitconfig
dotfiles commit -m "feat: initial dotfiles"
dotfiles remote add origin git@github.com:alice/dotfiles.git
dotfiles push -u origin main
```

Não há passos extras de "registrar" ou "aplicar". O que você rastreia fica disponível imediatamente no lugar certo — não há symlinks, cópias ou diretório de staging.

### `.gitignore` whitelist

**Problema:** `$HOME` contém milhares de arquivos (downloads, caches, diretórios de apps) que não devem ser rastreados. Com o working tree em `$HOME`, `dotfiles status` listaria todo esse noise mesmo com `showUntrackedFiles no`.

**Solução:** `.gitignore` em `$HOME` configurado como **whitelist** — ignora tudo por default e libera só o que deve ser rastreado:

```gitignore
# Ignora absolutamente tudo
*

# Libera o próprio .gitignore (senão ele fica fora do repo)
!.gitignore

# Libera arquivos específicos com !
!.zshrc
!.zshenv
!.gitconfig

# Libera pastas (parents antes de children)
!.config/
!.config/nvim/
!.config/nvim/init.lua
!.config/nvim/lua/
!.config/nvim/lua/**

!.local/
!.local/bin/
!.local/bin/myscript
```

Combinado com `status.showUntrackedFiles no`, o output de `dotfiles status` fica limpo — só mostra o que você decidiu rastrear.

### Nova máquina — checkout

Para restaurar dotfiles em uma máquina nova:

```bash
# 1. Clonar o repo como bare
git clone --bare git@github.com:alice/dotfiles.git "$HOME/.dotfiles"

# 2. Criar o alias (temporário ou já no .zshrc recém-clonado)
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

# 3. Fazer checkout — popula os arquivos em $HOME
dotfiles checkout
```

O passo 3 pode falhar se já existirem arquivos no home que conflitam com o repo:

```
error: The following untracked working tree files would be overwritten by checkout
```

Se isso ocorrer, há duas opções:

```bash
# Opção 1: fazer backup dos arquivos existentes e forçar checkout
mkdir -p ~/.dotfiles-backup
dotfiles checkout 2>&1 | grep -E "^\s+\." | xargs -I{} mv {} ~/.dotfiles-backup/
dotfiles checkout

# Opção 2: aceitar overwrite (só se souber que pode descartar os arquivos locais)
dotfiles checkout -f
```

### Limitações

Esta abordagem é deliberadamente minimalista. O que ela **não** oferece:

- **Sem templates** — não resolve `{{ .email }}` ou variáveis por hostname/OS. Para isso, use chezmoi.
- **Sem secrets nativos** — encryption fica externa (ex: git-crypt aplicado sobre o repo de dotfiles).
- **Sem cross-OS automático** — a separação por OS requer branches ou lógica condicional no próprio shell.
- **Whitelist explícita exige paciência** — cada novo arquivo ou pasta precisa ser liberado manualmente no `.gitignore`.
- **Conflitos no checkout** — arquivos pré-existentes no home precisam ser tratados manualmente.
- **`showUntrackedFiles no` pode esconder novos arquivos** que deveriam ser versionados.

## Na prática

### Setup completo passo-a-passo

```bash
# 1. Inicializar o bare repo
git init --bare "$HOME/.dotfiles"

# 2. Adicionar alias ao shell e recarregar
echo "alias dotfiles='git --git-dir=\$HOME/.dotfiles --work-tree=\$HOME'" >> ~/.zshrc
source ~/.zshrc

# 3. Configurar pra ocultar untracked por default
dotfiles config --local status.showUntrackedFiles no

# 4. Adicionar primeiros dotfiles e commitar
dotfiles add ~/.zshrc
dotfiles commit -m "feat: add zshrc"

# 5. Criar a whitelist do .gitignore e commitá-la
cat > ~/.gitignore <<'EOF'
*
!.gitignore
!.zshrc
!.gitconfig
!.config/
EOF

dotfiles add ~/.gitignore
dotfiles commit -m "feat: gitignore whitelist"

# 6. Conectar ao remote e fazer o primeiro push
dotfiles remote add origin git@github.com:alice/dotfiles.git
dotfiles push -u origin main
```

### Adicionar pasta inteira (com whitelist)

Pastas exigem que todos os diretórios parents sejam liberados antes dos filhos — o git (e o gitignore) não libera subdirs implicitamente:

```bash
# Adicionar ~/.config/nvim/ ao repo
cat >> ~/.gitignore <<'EOF'
!.config/nvim/
!.config/nvim/**
EOF

dotfiles add ~/.gitignore
dotfiles add ~/.config/nvim/
dotfiles commit -m "feat: add nvim config"
```

O `**` é necessário para incluir arquivos em subdirs profundos da pasta.

### Workflow diário

O dia-a-dia é igual ao git normal:

```bash
dotfiles status          # ver o que mudou
dotfiles diff            # ver as diferenças
dotfiles add ~/.zshrc    # adicionar mudança
dotfiles commit -m "tweak: ajuste no prompt"
dotfiles push            # sincronizar pro remote

dotfiles pull            # sincronizar de outra máquina
```

Para checar periodicamente se há novos arquivos que deveriam ser rastreados (que `showUntrackedFiles no` oculta):

```bash
dotfiles -c status.showUntrackedFiles=normal status
```

## Armadilhas

**`git status` direto em `$HOME` lista milhares de arquivos**
**Causa:** `git status` padrão em `$HOME` não usa o alias `dotfiles` — ignora a configuração de `showUntrackedFiles no` do repo bare.
**Sintoma:** terminal trava ou imprime scroll infinito de arquivos não rastreados ao rodar `git status` no home.
**Como detectar:** rodar `git status` diretamente em `$HOME` (sem alias).
**Solução:** nunca usar `git` diretamente no home para dotfiles — sempre o alias `dotfiles`. O git "normal" no home não tem contexto do repo bare.

---

**`dotfiles status` esconde arquivos novos que deveriam ser versionados**
**Causa:** `status.showUntrackedFiles no` é global para o alias — oculta tudo que não está rastreado, incluindo arquivos que você esqueceu de adicionar.
**Sintoma:** cria `~/.config/nvim/plugin.lua`, esquece de rastrear, descobre meses depois.
**Como detectar:** `dotfiles -c status.showUntrackedFiles=normal status` lista todos os untracked temporariamente.
**Solução:** hábito de checar untracked periodicamente; ou criar alias `dotfiles-all` com `showUntrackedFiles=normal`.

---

**Checkout em máquina nova falha por arquivo pré-existente**
**Causa:** git se recusa a sobrescrever arquivos do home que já existem e divergem do repo — comportamento de segurança padrão.
**Sintoma:** mensagem `error: The following untracked working tree files would be overwritten by checkout`.
**Como detectar:** a própria mensagem de erro lista os arquivos conflitantes.
**Solução:** fazer backup dos arquivos existentes antes do checkout (`mv ~/.zshrc ~/.dotfiles-backup/`) e depois `dotfiles checkout`. Ou `dotfiles checkout -f` se souber que pode descartar as versões locais.

---

**Whitelist `.gitignore` com ordem errada silencia arquivos**
**Causa:** no gitignore, `!arquivo` dentro de uma pasta ignorada só funciona se a pasta pai foi explicitamente liberada antes. O git não libera children de diretórios ignorados implicitamente.
**Sintoma:** `dotfiles add ~/.config/nvim/init.lua` não adiciona o arquivo — parece sumir.
**Como detectar:** `dotfiles check-ignore -v ~/.config/nvim/init.lua` mostra qual regra no `.gitignore` está bloqueando o path e em qual linha.
**Solução:** sempre liberar parents antes de children: primeiro `!.config/`, depois `!.config/nvim/`, depois `!.config/nvim/init.lua`. A ordem no arquivo importa.

---

**Bare repo (`$HOME/.dotfiles/`) rastreado por engano em outro repo**
**Causa:** se você tem outro repo git cobrindo `$HOME` (ex: uma tentativa anterior com outra ferramenta), ele pode enxergar `~/.dotfiles/` como diretório não rastreado e oferecer adicioná-lo.
**Sintoma:** `git status` em outro repo mostra `~/.dotfiles/` como untracked.
**Como detectar:** `git status` no repo B lista `.dotfiles/` como novo diretório.
**Solução:** adicionar `.dotfiles/` ao `.gitignore` do repo B.

---

**Alias não persiste após reinicialização**
**Causa:** o alias foi criado só na sessão atual, sem ser salvo no `~/.zshrc`.
**Sintoma:** `dotfiles: command not found` ao abrir novo terminal.
**Como detectar:** abrir novo terminal e rodar `dotfiles status`.
**Solução:** garantir que a linha `alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'` esteja salva no `~/.zshrc` (ou `~/.bashrc`).

## Em inglês

- **bare repo** — *repo bare*. "Git repository sem working tree — só metadados em `.git/`; base da abordagem minimalista de dotfiles."
- **working tree** — *árvore de trabalho*. "Diretório onde os arquivos rastreados pelo git vivem fisicamente; forçado para `$HOME` no setup bare."
- **alias** — *alias*. "Atalho de shell (`dotfiles='git --git-dir=...'`) que substitui `git` para operações de dotfiles."
- **whitelist** — *whitelist / lista de permissões*. "Padrão de `.gitignore` que começa com `*` (ignora tudo) e libera só o explícito com `!arquivo`."
- **checkout** — *checkout*. "Comando `dotfiles checkout` que popula os arquivos rastreados em `$HOME` ao restaurar numa máquina nova."
- **force** — *forçar*. "Flag `-f` em `dotfiles checkout -f` que sobrescreve arquivos existentes no home sem pedir confirmação."
- **untracked** — *não rastreado*. "Arquivo em `$HOME` que o git conhece mas que não foi explicitamente adicionado ao bare repo."
- **native** — *nativo*. "Sem dependências externas — bare repo usa apenas git, ferramenta já presente em praticamente todo sistema."
- **minimalist** — *minimalista*. "Abordagem que resolve o problema com o mínimo possível: sem instalações, sem state files, sem configuração de ferramenta."
- **portability** — *portabilidade*. "Capacidade de restaurar o ambiente em qualquer máquina com git disponível, sem instalar gerenciador de dotfiles."

## Veja também

- [[01 - Princípios — o que são dotfiles e por que versionar]] — pré-req
- [[04 - GNU stow — symlinks declarativos]] — alternativa com symlinks
- [[05 - chezmoi — manager completo com templates]] — alternativa completa com templates e secrets
- [[08 - Bootstrap — máquina nova zero-to-ready]] — bootstrap com bare repo
- [[03-Dominios/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Bare repo (dotfiles)|bare repo]], [[Dicionário do Terminal#Whitelist (.gitignore)|whitelist]]

## Referências

- Atlassian — Dotfiles tutorial: https://www.atlassian.com/git/tutorials/dotfiles
- HN thread original: https://news.ycombinator.com/item?id=11070797
