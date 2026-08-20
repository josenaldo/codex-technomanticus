---
title: "Sync entre máquinas heterogêneas"
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
  - sync
  - multi-machine
aliases:
  - Sync máquinas
---

# Sync entre máquinas heterogêneas

> [!abstract] TL;DR
> Cenário comum: laptop pessoal + work + servidor cloud, cada um com requisitos diferentes (work tem secrets corp; server não tem GUI). 4 estratégias: (1) branches per-host, (2) conditional includes no shell, (3) chezmoi data por host (`.chezmoi.hostname`), (4) stow com pastas host-specific. Branches pra diferenças grandes/estruturais; condicionais pra diferenças pequenas/dinâmicas. Tradeoff: manutenibilidade (branches) vs flexibilidade (condicionais).

## O que é / Como funciona

### O cenário

Múltiplas máquinas, cada uma com setup parcialmente diferente. A composição típica de um dev:

- `personal-laptop` — macOS, Homebrew, dev local, GUI tools pesadas
- `work-laptop` — Linux corporativo, restrições de install, secrets corp (AWS, VPN, email profissional)
- `cloud-server` — Ubuntu headless, sem GUI, shell minimalista, sem apps de desktop
- `dev-vm` — Linux full-feature, espelha o personal mas em ambiente isolado

Cada máquina exige variações em:

- **Email git** — `git config user.email` é pessoal num, profissional em outro
- **Aliases condicionais** — `alias k=kubectl` só faz sentido onde kubectl existe
- **Plugins de shell** — TUIs pesadas (lazygit, zellij) no laptop; apenas essentials no server
- **Secrets segregados** — AWS keys work não devem aparecer no personal; keys pessoais não devem aparecer no work
- **GPG signing** — obrigatório no work, opcional no personal

O desafio: um único repositório de dotfiles que serve todas essas máquinas sem duplicar config e sem vazar secrets entre contextos.

### Estratégia 1: Branches per-host

Cada máquina vive em uma branch separada. O `main` é o baseline funcional em qualquer máquina; branches derivam e adicionam overrides específicos.

```text
main          ──── baseline (funciona em qualquer lugar)
  └── work    ──── + AWS profile, kubectl alias, email corp, GPG signing
  └── server  ──── - GUI tools, plugins mínimos, subset do zshrc
```

```bash
# Setup em máquina work
git clone https://github.com/alice/dotfiles ~/dotfiles
cd ~/dotfiles
git checkout work
stow zsh git

# Absorver mudanças do main periodicamente
git checkout work
git merge main
# Resolver eventuais conflitos nos overrides
git push origin work
```

**Pro:** separação clara — `git diff main work` mostra exatamente o que é diferente no work. Fácil auditar o que cada branch adiciona ou remove.

**Con:** 2x manutenção. Mudanças feitas em `main` precisam ser mergeadas em todas as branches; divergência cresce com o tempo se o merge não for disciplinado.

### Estratégia 2: Conditional includes no shell

Single branch, lógica de inclusão condicional em runtime. O `.zshrc` principal detecta hostname ou OS e sourcia arquivos específicos se existirem.

```zsh
# ~/.zshrc (idêntico em todas as máquinas)
HOSTNAME_SHORT=$(hostname -s)
OS_TYPE="$(uname -s | tr '[:upper:]' '[:lower:]')"

# Source host-specific se existir
[[ -f "$HOME/.config/zsh/host-${HOSTNAME_SHORT}.zsh" ]] && \
  source "$HOME/.config/zsh/host-${HOSTNAME_SHORT}.zsh"

# Source OS-specific se existir
[[ -f "$HOME/.config/zsh/os-${OS_TYPE}.zsh" ]] && \
  source "$HOME/.config/zsh/os-${OS_TYPE}.zsh"
```

Estrutura de arquivos no repo:

```text
zsh/.config/zsh/
├── host-work-laptop.zsh     # só carrega em work-laptop
├── host-personal-mac.zsh    # só carrega no personal
├── host-cloud-server.zsh    # só carrega no server
├── os-darwin.zsh            # só carrega em macOS
└── os-linux.zsh             # só carrega em Linux
```

**Pro:** single branch, single history. Adicionar suporte a nova máquina = criar um arquivo `host-<nome>.zsh` e commitar. Zero conflito com outras máquinas.

**Con:** arquivos `host-XXX.zsh` são versionados — se contiverem secrets, precisam passar por encryption (ver [[07 - Secrets em dotfiles — git-crypt, age, sops]]). A lista de nomes de host fica exposta no repo.

### Estratégia 3: chezmoi data por host

chezmoi resolve a heterogeneidade em template-time: o `.chezmoi.toml.tmpl` no source define variáveis diferentes por hostname, e os templates as consomem.

```toml
{{- /* .chezmoi.toml.tmpl no source directory */ -}}
{{- if eq .chezmoi.hostname "work-laptop" -}}
[data]
  email      = "alice@bigcorp.com"
  machine    = "work"
  gpgsign    = "true"
  aws_profile = "work"
{{- else if eq .chezmoi.hostname "cloud-server" -}}
[data]
  email      = "alice@personal.dev"
  machine    = "server"
  gpgsign    = "false"
  aws_profile = ""
{{- else -}}
[data]
  email      = "alice@personal.dev"
  machine    = "personal"
  gpgsign    = "false"
  aws_profile = "personal"
{{- end -}}
```

Templates consomem os dados:

```gitconfig
{{- /* dot_gitconfig.tmpl */ -}}
[user]
  name  = Alice
  email = {{ .email }}
[commit]
  gpgsign = {{ .gpgsign }}
```

```zsh
{{- /* dot_config/zsh/env.zsh.tmpl */ -}}
{{ if ne .aws_profile "" -}}
export AWS_PROFILE={{ .aws_profile }}
{{- end }}
{{ if eq .machine "work" -}}
alias k=kubectl
alias tf=terraform
{{- end }}
```

**Pro:** idiomático em chezmoi; single source of truth; apply-time rendering garante que cada máquina recebe exatamente sua config sem arquivos extras. Zero arquivos "extras" em runtime.

**Con:** requer chezmoi como prerequisito. Máquinas que usam stow ou bare repo precisam de outro approach.

### Estratégia 4: Stow com pastas host-specific

O repo organiza pacotes separados por host, e o bootstrap sabe quais stow em cada máquina.

```text
~/dotfiles/
├── zsh-base/
│   └── .zshrc             # config comum a todas as máquinas
├── zsh-work/
│   └── .config/zsh/
│       └── local.zsh      # alias k=kubectl, AWS_PROFILE=work
├── zsh-personal/
│   └── .config/zsh/
│       └── local.zsh      # aliases pessoais, EDITOR=nvim
└── zsh-server/
    └── .config/zsh/
        └── local.zsh      # minimal: sem plugins pesados
```

O `.zshrc` base sempre sourcia `~/.config/zsh/local.zsh` se existir; o stow determina qual `local.zsh` é symlinked.

```bash
# bootstrap.sh — detecta host e aplica pacotes corretos
HOSTNAME_SHORT=$(hostname -s)

case "$HOSTNAME_SHORT" in
  work-*)
    stow zsh-base zsh-work git-work
    ;;
  *-server | cloud-*)
    stow zsh-base zsh-server
    ;;
  *)
    stow zsh-base zsh-personal git-personal
    ;;
esac
```

**Pro:** flexibilidade total; compatível com stow puro sem dependências extras.

**Con:** manutenção manual — mudanças no baseline precisam ser replicadas nos pacotes derivados se não forem modularizadas corretamente.

### Quando branchar vs quando condicionar

| Tipo de diferença | Estratégia recomendada |
|---|---|
| OS diferente (Linux vs macOS) | Condicional (env var `OS`) ou chezmoi template |
| Secret só em work | Encryption (nota 07) + conditional load |
| Email git diferente | chezmoi data ou `git config includeIf` |
| Aliases muito diferentes (k8s só no work) | Host-specific file (estratégia 2) |
| Plugins de shell muito diferentes | Host-specific file ou chezmoi template |
| Hardware muito diferente (server headless vs laptop) | Branch separada (estratégia 1) |
| Configuração que muda frequentemente | Condicional — merge de branch é fricção |
| Configuração estável que raramente muda | Branch — mais fácil auditar em diff |

### git config conditional include

git 2.13+ suporta `includeIf` para incluir configs condicionalmente por diretório, branch, ou URL de remote.

```gitconfig
# ~/.gitconfig (base, em todas as máquinas)
[user]
  name = Alice

# Inclui config de work pra repos dentro de ~/work/
[includeIf "gitdir:~/work/"]
  path = ~/.config/git/work.gitconfig

# Inclui config personal pra repos dentro de ~/personal/
[includeIf "gitdir:~/personal/"]
  path = ~/.config/git/personal.gitconfig
```

O arquivo incluído sobrescreve os valores do base:

```gitconfig
# ~/.config/git/work.gitconfig
[user]
  email = alice@bigcorp.com
[commit]
  gpgsign = true
[core]
  sshCommand = ssh -i ~/.ssh/work_ed25519
```

```gitconfig
# ~/.config/git/personal.gitconfig
[user]
  email = alice@personal.dev
```

Formas de `includeIf` disponíveis:

- `gitdir:<path>` — match pelo path do `.git` (trailing slash = match recursivo)
- `gitdir/i:<path>` — case-insensitive (útil em macOS com HFS+)
- `onbranch:<pattern>` — match pela branch atual
- `hasconfig:remote.*.url:<pattern>` — match pela URL do remote (git 2.36+)

**Verificar qual config está ativa em um repo:**

```bash
git config --show-origin --get user.email
# Exibe: file:/home/alice/.config/git/work.gitconfig	alice@bigcorp.com
```

### ssh Match patterns

ssh_config suporta `Match` para aplicar configurações condicionalmente, sem duplicar blocos `Host`.

```ssh-config
# ~/.ssh/config

# Default para todos os hosts
Host *
  IdentityFile    ~/.ssh/id_ed25519
  AddKeysToAgent  yes
  ServerAliveInterval 60

# GitHub — usa chave work se existir, senão usa default
Match host github.com exec "[ -f ~/.ssh/work_ed25519 ]"
  IdentityFile    ~/.ssh/work_ed25519
  User            git

# Servidores internos work — só alcançável em rede corp ou VPN
Match host *.bigcorp.internal
  IdentityFile    ~/.ssh/work_ed25519
  ProxyJump       bastion.bigcorp.com
  User            alice

# Máquinas pessoais — sem ProxyJump
Match host *.personal.dev
  IdentityFile    ~/.ssh/id_ed25519
```

Os critérios de `Match` disponíveis incluem: `host` (hostname do target), `exec` (executa comando e testa exit code), `user` (usuário remoto), `localuser` (usuário local), `localnetwork` (CIDR de rede local). Critérios se combinam — `Match host X user Y` exige ambos verdadeiros.

**Verificar qual identidade ssh usa em uma conexão:**

```bash
ssh -v git@github.com 2>&1 | grep "identity file\|Trying"
```

## Na prática

### Setup conditional por host

```bash
# Criar estrutura
mkdir -p ~/.config/zsh

# zshrc base — sourcia host-specific se existir
cat >> ~/.zshrc << 'EOF'

# Host-specific config
HOSTNAME_SHORT=$(hostname -s)
[[ -f "$HOME/.config/zsh/host-${HOSTNAME_SHORT}.zsh" ]] && \
  source "$HOME/.config/zsh/host-${HOSTNAME_SHORT}.zsh"
EOF

# Criar host-specific para work (este arquivo vai pro repo, encrypta se tiver secrets)
cat > ~/.config/zsh/host-work-laptop.zsh << 'EOF'
alias k=kubectl
alias tf=terraform
export AWS_PROFILE=work
export KUBECONFIG=~/.kube/work-config
EOF

# Criar host-specific para personal
cat > ~/.config/zsh/host-personal-mac.zsh << 'EOF'
export HOMEBREW_NO_AUTO_UPDATE=1
alias ls='gls --color=auto'
EOF

# Versionar no dotfiles repo
cd ~/dotfiles
# Se usar stow: coloca em zsh/.config/zsh/host-work-laptop.zsh
# Se usar bare: adiciona direto no home
git add zsh/.config/zsh/
git commit -m "feat(zsh): add host-specific configs"
```

### chezmoi por hostname

```bash
# Criar template de configuração por hostname
cat > ~/.local/share/chezmoi/.chezmoi.toml.tmpl << 'EOF'
{{- if eq .chezmoi.hostname "work-laptop" -}}
[data]
  machine    = "work"
  email      = "alice@bigcorp.com"
  gpgsign    = "true"
{{- else if eq .chezmoi.hostname "cloud-server" -}}
[data]
  machine    = "server"
  email      = "alice@personal.dev"
  gpgsign    = "false"
{{- else -}}
[data]
  machine    = "personal"
  email      = "alice@personal.dev"
  gpgsign    = "false"
{{- end -}}
EOF

# Template do gitconfig que consome as variáveis
cat > ~/.local/share/chezmoi/dot_gitconfig.tmpl << 'EOF'
[user]
  name  = Alice
  email = {{ .email }}
[commit]
  gpgsign = {{ .gpgsign }}
EOF

# Verificar o que chezmoi renderiza antes de aplicar
chezmoi data              # mostra as variáveis disponíveis
chezmoi diff ~/.gitconfig # mostra o diff de como ficaria

# Aplicar
chezmoi apply ~/.gitconfig
```

### Branches per-host workflow

```bash
# Setup: criar branch work a partir do main
cd ~/dotfiles
git checkout main
git checkout -b work

# Adicionar override só no work
cat >> zsh/.zshrc << 'EOF'
# work overrides — não vai pro main
alias k=kubectl
export AWS_PROFILE=work
EOF

git add zsh/.zshrc
git commit -m "work: add k8s aliases and AWS_PROFILE"

# Push ambas as branches
git push origin main work

# --- Workflow de manutenção (toda semana) ---
# Absorver mudanças do main na branch work
git checkout main
git pull origin main
git checkout work
git merge main
# Se houver conflito: resolver, depois commitar
git push origin work
```

Para um workflow mais organizado em branches per-host, manter as mudanças work-specific em commits atômicos com prefixo `work:` facilita cherry-pick reverso (trazer algo de work pro main se não for sensível).

## Armadilhas

**Branches divergem demais — work nunca é mergeado** **Causa:** trabalho contínuo em main sem fazer merge periódico em work; a branch work envelhece. **Sintoma:** `git merge main` na branch work gera conflito grande e assustador. **Como detectar:** `git log work..main --oneline` mostra quantos commits main está à frente de work. Se passar de 20, a dívida é alta. **Solução:** disciplinar merge regular (1x por semana); configurar lembrete no calendário. Alternativa: trocar para estratégia 2 (conditional includes) se a diferença entre máquinas for pequena.

---

**`hostname -s` retorna valor diferente em macOS vs Linux** **Causa:** macOS às vezes retorna hostname com sufixo `.local` ou `.lan` dependendo da configuração de rede; Linux retorna o nome curto puro. **Sintoma:** o arquivo `host-work-laptop.zsh` não é sourceiado em macOS porque `hostname -s` retorna `work-laptop.local` em vez de `work-laptop`. **Como detectar:** rodar `hostname` e `hostname -s` na máquina afetada; comparar com o nome esperado do arquivo. **Solução:** `hostname -s` remove sufixo na maioria dos casos; para macOS consistente, usar `scutil --get LocalHostName`. Ou normalizar no zshrc: `HOSTNAME_SHORT=${$(hostname -s)%%.*}` (remove tudo após o primeiro ponto).

---

**`includeIf "gitdir:~/work/"` não inclui — trailing slash ausente** **Causa:** git exige trailing slash no `gitdir:` para match recursivo. Sem ela, só faz match no diretório exato `~/work`, não em `~/work/foo/`. **Sintoma:** a config de work não é aplicada em repos dentro de `~/work/algum-repo/`; `git config user.email` retorna o email base. **Como detectar:** `git config --show-origin --get user.email` dentro do repo work — se mostrar `~/.gitconfig` como origem, o include não foi ativado. **Solução:** sempre incluir trailing slash: `"gitdir:~/work/"` (não `"gitdir:~/work"`). Confirmar com `git config --show-origin --get user.email` que a origem correta é mostrada.

---

**Files host-specific commitados acidentalmente com secrets em plaintext** **Causa:** ao criar `host-work-laptop.zsh` com `export AWS_SECRET_KEY=...` e commitar sem encryption, o secret vai pro repo. **Sintoma:** secret em plaintext visível em `git log -p`; vaza para qualquer clone do repo. **Como detectar:** `git log --all -p -- "zsh/.config/zsh/host-work-laptop.zsh"` — qualquer valor sensível visível é vazamento. **Solução:** arquivos com secrets devem usar encryption (git-crypt ou age via chezmoi) ou ser adicionados ao `.gitignore` e mantidos apenas localmente. Decidir conscientemente: versionar (com encryption) ou ignorar. Rotacionar qualquer secret já exposto imediatamente.

---

**chezmoi hostname template não funciona em containers (hostname genérico)** **Causa:** containers Docker têm hostname gerado aleatoriamente (`abc123def456`), nunca igual ao nome configurado no template. **Sintoma:** o bloco `if eq .chezmoi.hostname "work-laptop"` nunca executa em container; a config cai sempre no else. **Como detectar:** `chezmoi data | grep hostname` dentro do container mostra o hostname gerado. **Solução:** em containers, preferir outras variáveis de distinção: `chezmoi.username`, variável de ambiente custom (`MACHINE_TYPE=work`), ou setar `--hostname` no `chezmoi init`. Outra opção: usar `promptString` no `.chezmoi.toml.tmpl` para capturar interativamente o tipo de máquina no primeiro apply.

---

**git ssh usa chave errada — Match exec ignora arquivo inexistente** **Causa:** no ssh_config, `Match exec "[ -f ~/.ssh/work_ed25519 ]"` retorna false se o arquivo não existir — o Match silenciosamente não se aplica, e a config volta pro default. **Sintoma:** push para GitHub work usa a chave pessoal; commit aparece sob o usuário pessoal. **Como detectar:** `ssh -v git@github.com 2>&1 | grep "identity file"` — mostra qual chave está sendo tentada. **Solução:** verificar que o arquivo referenciado em `Match exec` existe antes de depender do comportamento. Usar `ssh-add -l` para listar chaves carregadas no agent. Em bootstrap, incluir a criação/cópia da chave work como pré-requisito explícito.

## Em inglês

- **sync** — *sincronização / sync*. "Processo de manter dotfiles consistentes entre múltiplas máquinas, propagando mudanças do repositório para cada host."
- **hostname** — *hostname / nome do host*. "Identificador da máquina em rede. Em dotfiles: usado como chave de distinção para carregar configs específicas — `hostname -s` retorna o nome curto."
- **conditional** — *condicional*. "Instrução que executa um bloco apenas se uma condição for verdadeira. Em dotfiles: `includeIf` no gitconfig, `[[ -f ]]` no zshrc, `{{ if }}` em templates chezmoi."
- **branch** — *branch / ramificação*. "Em estratégia per-host: cada máquina tem sua própria branch derivada do main, carregando overrides específicos. Facilita auditoria mas exige merge disciplinado."
- **merge** — *merge / mesclar*. "Integrar mudanças de uma branch em outra. Em workflow per-host: `main → work` absorve o baseline atualizado na branch da máquina."
- **override** — *override / sobrescrever*. "Valor ou configuração que substitui o default. Host-specific files e branches per-host são mecanismos de override localizado."
- **fleet** — *fleet / frota*. "Conjunto de máquinas gerenciadas com a mesma base de dotfiles. Quanto maior a frota, mais vantajoso usar chezmoi templates em vez de branches manuais."
- **heterogeneous** — *heterogêneas / heterogêneous*. "Máquinas com OS, hardware, restrições ou propósito diferentes — oposto de homogêneas. O problema central desta nota: como um repo serve uma frota heterogênea."
- **divergence** — *divergência*. "Estado em que uma branch per-host acumulou tantas diferenças do main que o merge se torna custoso. Detectada com `git log work..main --oneline`."
- **single source** — *fonte única de verdade / single source of truth*. "Princípio: uma config existe em um lugar só e é renderizada/adaptada para cada contexto — objetivo das estratégias 2 e 3."

## Veja também

- [[04 - GNU stow — symlinks declarativos]] — sync via stow + pastas host-specific
- [[05 - chezmoi — manager completo com templates]] — sync via chezmoi data e templates
- [[06 - Bare git repo — abordagem minimalista]] — sync via branches per-host
- [[07 - Secrets em dotfiles — git-crypt, age, sops]] — encryption para host-specific files com secrets
- [[08 - Bootstrap — máquina nova zero-to-ready]] — bootstrap que detecta host e aplica config correta
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#chezmoi|chezmoi]], [[Dicionário do Terminal#Template (dotfiles)|template]]

## Referências

- chezmoi machines: https://www.chezmoi.io/user-guide/machines/
- git includeIf: https://git-scm.com/docs/git-config#_conditional_includes
- ssh_config Match: https://man.openbsd.org/ssh_config.5
