---
title: "chezmoi — manager completo com templates"
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
  - chezmoi
  - templates
aliases:
  - chezmoi
---

# chezmoi — manager completo com templates

> [!abstract] TL;DR
> chezmoi é manager de dotfiles em Go com state machine declarativo. Source em `~/.local/share/chezmoi/`; `chezmoi apply` aplica diff entre source e target. Features: templates (Go syntax: `{{ .chezmoi.os }}`, `{{ .email }}`), encrypted files nativos (age/gpg), scripts (`run_once_`, `run_onchange_`), data customizada. Workflow: `chezmoi edit`, `chezmoi diff`, `chezmoi apply`. Cross-OS automático via templates; mais features que stow ao custo de curva de aprendizado.

## O que é / Como funciona

### Conceito básico

chezmoi significa "casa minha" em francês — reflexo da proposta: manter sua casa digital (dotfiles) organizada e portável. O projeto foi criado por Tom Payne (twpayne) e é escrito em Go.

A metáfora central é de **state machine**: o source directory contém a "descrição do que deveria estar" nos seus dotfiles; `chezmoi apply` calcula o diff entre source e target e aplica as mudanças necessárias. Diferente do stow (que usa symlinks), **chezmoi copia arquivos renderizados** para o target (`$HOME`).

Essa distinção tem um trade-off crítico:

- **Vantagem:** templates, encryption e lógica condicional acontecem em apply-time — você pode ter um único `dot_zshrc.tmpl` que gera `.zshrc` diferente no macOS e no Linux.
- **Desvantagem:** editar `~/.zshrc` diretamente não vai pro repo. Você precisa usar `chezmoi edit` ou `chezmoi add` para manter source e target em sincronia.

### Source directory

O source directory fica em `~/.local/share/chezmoi/` por default e é um repositório git normal. chezmoi usa uma **naming convention especial** para mapear arquivos do source para o target:

| Nome no source | Path no target |
|---|---|
| `dot_zshrc` | `~/.zshrc` |
| `dot_config/nvim/init.lua` | `~/.config/nvim/init.lua` |
| `private_dot_ssh/config` | `~/.ssh/config` (permissões 0600) |
| `executable_dot_local/bin/script` | `~/.local/bin/script` (chmod +x) |
| `dot_gitconfig.tmpl` | `~/.gitconfig` (renderizado como template) |
| `encrypted_private_dot_gnupg/key.gpg.age` | `~/.gnupg/key.gpg` (decriptado) |

Prefixos acumulam: `executable_private_dot_local/bin/myscript` → `~/.local/bin/myscript` com `chmod +x` e permissões privadas.

O chezmoi também suporta **diretórios externos** (`externals`): arquivos ou arquivos compactados baixados de URLs e extraídos no target. Exemplo: baixar `oh-my-zsh` de forma declarativa sem precisar de script de install.

Para inspecionar a estrutura atual do source:

```bash
chezmoi cd          # entra no source
ls -la              # ver estrutura real do source
exit

# Ou sem sair do cwd
chezmoi source-path ~/.zshrc  # mostra o path no source de um target específico
```

### Comandos essenciais

```bash
chezmoi init                                    # inicializa source vazio
chezmoi init https://github.com/alice/dotfiles  # clona repo + não aplica
chezmoi init --apply https://github.com/alice/dotfiles  # clona + aplica

chezmoi add ~/.zshrc                    # adiciona ao source como dot_zshrc
chezmoi add --template ~/.gitconfig     # adiciona como dot_gitconfig.tmpl
chezmoi add --encrypt ~/.config/secret  # adiciona criptografado

chezmoi edit ~/.zshrc                   # edita arquivo no source (abre $EDITOR)
chezmoi diff                            # mostra diff source → target (sem aplicar)
chezmoi apply                           # aplica diff: target ← source renderizado
chezmoi apply -v ~/.zshrc               # verbose, aplica só esse target
chezmoi apply -n                        # dry-run: mostra o que faria sem aplicar

chezmoi re-add ~/.zshrc                 # sincroniza source ← target (reverso)
chezmoi merge ~/.zshrc                  # abre merge tool pra conflito source/target

chezmoi update                          # git pull no source + apply
chezmoi cd                              # cd no source directory
chezmoi data                            # exibe todos os dados disponíveis em templates
chezmoi status                          # arquivos com divergência source/target
chezmoi verify                          # verifica se target bate com source
```

### Templates (Go syntax)

chezmoi usa o engine de templates da standard library do Go (`text/template`). Arquivos com extensão `.tmpl` no source são renderizados antes de serem copiados para o target.

**Variáveis builtin disponíveis:**

| Variável | Valores típicos |
|---|---|
| `{{ .chezmoi.os }}` | `"linux"`, `"darwin"`, `"windows"` |
| `{{ .chezmoi.arch }}` | `"amd64"`, `"arm64"` |
| `{{ .chezmoi.hostname }}` | nome do host |
| `{{ .chezmoi.username }}` | usuário atual |
| `{{ .chezmoi.osRelease.id }}` | `"ubuntu"`, `"fedora"`, `"arch"` (Linux apenas) |

Para verificar todos os valores disponíveis na máquina atual:

```bash
chezmoi data
```

**Custom data** em `~/.config/chezmoi/chezmoi.toml`:

```toml
[data]
email = "alice@example.com"
work_email = "alice@bigcorp.com"
```

**Uso em template** (`dot_gitconfig.tmpl`):

```gitconfig
[user]
  name = Alice
{{- if eq .chezmoi.hostname "work-laptop" }}
  email = {{ .work_email }}
{{- else }}
  email = {{ .email }}
{{- end }}
```

O hífen (`-`) em `{{-` e `-}}` remove espaços/newlines adjacentes, evitando linhas em branco no output renderizado.

### Encrypted files (age)

chezmoi suporta criptografia nativa de arquivos sensíveis usando age ou gpg. O arquivo criptografado fica no source (ciphertext no git); apply decripta para o target.

```bash
# Configurar encryption no chezmoi.toml
# [age]
#   identity = "~/.age/key.txt"
#   recipient = "age1ql3z..."

chezmoi add --encrypt ~/.config/myapp/secret.toml
# Source: encrypted_dot_config/myapp/secret.toml.age
```

O ciphertext pode ser commitado no repositório sem expor o conteúdo — apenas quem tem a chave age consegue decriptar no apply.

Para configurar age no `chezmoi.toml`:

```toml
[age]
  identity = "~/.age/key.txt"
  recipient = "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"
```

Gerar chave age:

```bash
age-keygen -o ~/.age/key.txt
# Saída: Public key: age1ql3z...
```

A chave privada (`~/.age/key.txt`) **nunca** entra no repo — fica apenas na máquina. O recipient (chave pública) pode ser versionado ou incluído no `chezmoi.toml`.

### Scripts

chezmoi executa scripts com base em seus prefixos de nome. Dois prefixos especiais:

- **`run_once_`** — executa 1 vez por conteúdo (state machine lembra o hash do script). Ideal para instalação de pacotes, bootstrap de ferramentas.
- **`run_onchange_`** — executa sempre que o conteúdo do script muda. Ideal para configuração incremental.

```bash
#!/usr/bin/env bash
# run_once_install-deps.sh
set -euo pipefail
brew install bat eza ripgrep fzf
```

Scripts com `run_once_` não re-executam em `chezmoi apply` subsequentes a menos que o script mude ou o estado seja resetado manualmente.

Um terceiro prefixo, `run_always_`, executa o script em todo `chezmoi apply` — útil para sincronização contínua de configurações que não têm estado próprio.

Scripts também suportam templates (`.tmpl`): `run_once_install-pkgs.sh.tmpl` é renderizado antes de executar, permitindo condicionar a instalação por OS:

```bash
#!/usr/bin/env bash
# run_once_install-pkgs.sh.tmpl
set -euo pipefail
{{ if eq .chezmoi.os "linux" -}}
sudo apt-get install -y bat ripgrep fd-find
{{- else if eq .chezmoi.os "darwin" -}}
brew install bat ripgrep fd
{{- end }}

### Comparativo com stow

| Aspecto | stow | chezmoi |
|---|---|---|
| Mecanismo | symlinks | cópia (com state) |
| Templates | não | sim (Go) |
| Cross-OS automático | manual (pastas) | sim (template) |
| Secrets | externa (git-crypt) | nativo (age/gpg) |
| Scripts integrados | não | sim (`run_once_`) |
| Curva de aprendizado | rasa | média |
| State file | não | sim (boltdb) |
| Edit home → source | automático (symlink) | manual (`chezmoi add`/`edit`) |

## Na prática

### Setup inicial em máquina nova

```bash
# 1. Instalar chezmoi
sh -c "$(curl -fsLS get.chezmoi.io)"

# 2. Inicializar a partir do repo e aplicar tudo
chezmoi init --apply https://github.com/alice/dotfiles

# Atalho pra GitHub: se o repo se chama "dotfiles"
chezmoi init --apply alice
```

O comando `init --apply` faz: clonar o repo para `~/.local/share/chezmoi/`, rodar `chezmoi apply`, e executar scripts `run_once_` na ordem correta. Setup completo em um comando.

Se o repo tiver `.chezmoi.toml.tmpl` no source, chezmoi interrompe e faz perguntas interativas antes de aplicar — útil para capturar email, hostname de trabalho ou preferências pessoais na primeira inicialização:

```toml
# .chezmoi.toml.tmpl no source
[data]
  email = "{{ promptString "email" }}"
  work = {{ promptBool "work machine?" }}
```

### Workflow editar + sync

```bash
chezmoi edit ~/.zshrc        # abre source no $EDITOR
chezmoi diff                 # preview do que será aplicado
chezmoi apply                # target ← source renderizado

chezmoi cd                   # cd no source directory
git add . && git commit -m "tweak prompt"
git push
exit                         # volta pro cwd anterior
```

A separação entre `chezmoi edit` e `chezmoi apply` permite revisar as mudanças antes de aplicar — especialmente útil em templates onde `chezmoi diff` mostra o output renderizado final.

### Template cross-OS exemplo (`dot_zshrc.tmpl`)

```zsh
# Configuração comum a todos os sistemas
export EDITOR=nvim
export PAGER=less

{{ if eq .chezmoi.os "darwin" -}}
# macOS-specific
export PATH="/opt/homebrew/bin:$PATH"
alias ls='gls --color=auto'
alias sed='gsed'
{{- else if eq .chezmoi.os "linux" -}}
# Linux-specific
alias ls='ls --color=auto'
{{- end }}

# Carrega por hostname — configurações específicas de máquina
{{ if eq .chezmoi.hostname "work-laptop" -}}
source ~/.config/work/aliases.zsh
{{- end }}
```

O mesmo arquivo fonte gera `.zshrc` diferentes dependendo do OS e hostname. Sem duplicar arquivos, sem packages separados.

### Re-aplicar parcial

```bash
chezmoi apply ~/.zshrc       # só esse target
chezmoi apply ~/.config/nvim # todos os targets dentro do diretório
chezmoi apply -n ~/.zshrc    # dry-run: mostra o diff sem aplicar
```

Útil após editar um único arquivo no source: aplica sem tocar no restante do home.

### Verificar estado de sincronia

Para saber quais arquivos estão fora de sincronia entre source e target sem aplicar nada:

```bash
chezmoi status     # lista arquivos com divergência (A=add, M=modify, D=delete)
chezmoi verify     # retorna código de saída 1 se houver divergência (útil em CI)
chezmoi diff       # diff completo de tudo
chezmoi diff ~/.gitconfig  # diff de um arquivo específico
```

`chezmoi status` é a forma rápida de auditoria: mostra os arquivos que seriam modificados por um `chezmoi apply`, sem realizar nenhuma mudança.

## Armadilhas

### (1) Editar `~/.zshrc` (target) e perder na próxima apply

**Causa:** edição direta no target não vai pro source; `chezmoi apply` ou `chezmoi update` sobrescreve com o source renderizado.

**Sintoma:** mudança feita em `~/.zshrc` desaparece após o próximo `chezmoi apply` ou `chezmoi update`.

**Como detectar:** `chezmoi diff` mostra divergência entre target (modificado) e source (original). Se aparecer diff, o target tem mudanças não capturadas.

**Solução:** sempre `chezmoi edit ~/.zshrc` em vez de editar o target direto. Se já editou o target, use `chezmoi re-add ~/.zshrc` para sincronizar na direção target → source antes do próximo apply.

---

### (2) Template com `{{ ... }}` literal em file não-template

**Causa:** copy-paste de sintaxe Go template em arquivo sem extensão `.tmpl`. chezmoi não processa templates em arquivos sem `.tmpl`.

**Sintoma:** o arquivo é copiado literalmente para o target — `{{ .chezmoi.os }}` aparece no `.zshrc` em vez do valor real.

**Como detectar:** verificar o target após apply — se contém `{{`, o template não foi processado.

**Solução:** renomear o arquivo no source para `<name>.tmpl`. Exemplo: `dot_zshrc` → `dot_zshrc.tmpl`. Depois `chezmoi apply`.

---

### (3) Confundir as duas configs do chezmoi

**Causa:** chezmoi tem duas configurações com propósitos distintos:
- `~/.config/chezmoi/chezmoi.toml` — config da ferramenta (encryption, editor, data) — **não versionada no source**.
- `.chezmoi.toml.tmpl` no source — gera o `chezmoi.toml` interativamente na inicialização via `chezmoi init`.

**Sintoma:** config de `[data]` ou `[age]` não é aplicada; variáveis de template retornam zero ou erro.

**Como detectar:** `chezmoi data` mostra todos os valores disponíveis. Se `email` ou outra variável custom estiver ausente, a config está no lugar errado ou com sintaxe inválida.

**Solução:** verificar `~/.config/chezmoi/chezmoi.toml` para a config da ferramenta. Consultar a documentação de referência: https://www.chezmoi.io/reference/configuration-file/.

---

### (4) `run_once_` com bug não re-executa após correção

**Causa:** chezmoi usa uma state machine (boltdb) que armazena o hash SHA256 do script após execução bem-sucedida. Se o script falhou mas chezmoi registrou a tentativa, ou se o script rodou e você quer forçar re-execução, o estado impede.

**Sintoma:** script corrigido não re-executa em `chezmoi apply` subsequente.

**Como detectar:** verificar o estado com `chezmoi state dump`. O bucket `scriptState` contém os hashes dos scripts executados.

**Solução:** opção 1 — renomear o script (ex: adicionar `_v2`) força re-execução porque o hash do nome muda. Opção 2 — usar `run_onchange_` em vez de `run_once_` se você quer que o script rode sempre que seu conteúdo mudar. Opção 3 — resetar o estado manualmente com `chezmoi state delete-bucket --bucket=scriptState` (cuidado: reseta todos os scripts).

---

### (5) Encrypted file commitado antes de adicionar `--encrypt`

**Causa:** `chezmoi add ~/.config/myapp/secret.toml` sem `--encrypt` adiciona o plaintext ao source. Se commitado no git, o conteúdo fica no history mesmo após corrigi-lo.

**Sintoma:** o arquivo secreto está no histórico git em plaintext — `git log --all -p -- dot_config/myapp/secret.toml` mostra o conteúdo.

**Como detectar:** `git log --all -p --` seguido do path no source. Qualquer conteúdo sensível visível = vazamento.

**Solução:** purgar o histórico com `git filter-repo` ou BFG Repo Cleaner. Rotar o secret imediatamente (assumir que foi vazado). Em seguida, remover o arquivo do source, re-adicionar com `chezmoi add --encrypt` e commitar o `.age` criptografado.

---

### (6) `chezmoi diff` mostra mudanças mas `chezmoi apply` não aplica nada

**Causa:** o source tem arquivos `.tmpl` que referenciam variáveis não definidas em `chezmoi.toml`. Por default, chezmoi usa `missingkey=error` — template com chave ausente falha silenciosamente ou aborta.

**Sintoma:** `chezmoi apply` termina sem erros mas os arquivos esperados não são atualizados.

**Como detectar:** rodar `chezmoi apply -v` (verbose) e observar erros de template. Confirmar com `chezmoi data` que todas as variáveis referenciadas nos templates estão definidas.

**Solução:** adicionar as variáveis faltantes em `~/.config/chezmoi/chezmoi.toml` na seção `[data]`. Ou ajustar o comportamento com `[template] options = ["missingkey=zero"]` para variáveis opcionais.

## Em inglês

- **source** — *fonte*. "Diretório `~/.local/share/chezmoi/` onde ficam os dotfiles e templates versionados."
- **target** — *alvo*. "Diretório do usuário (`$HOME`) onde chezmoi aplica os arquivos renderizados."
- **template** — *template*. "Arquivo com placeholders Go (`.tmpl`) processado em apply-time para gerar o conteúdo final."
- **render** — *renderizar*. "Processar um template substituindo variáveis pelos valores reais e avaliando condicionais."
- **state machine** — *máquina de estados*. "Modelo de funcionamento do chezmoi: mantém estado (boltdb) do que já foi aplicado para calcular diffs."
- **idempotent** — *idempotente*. "Rodar `chezmoi apply` múltiplas vezes produz o mesmo resultado; só aplica o que mudou."
- **encrypted** — *criptografado*. "Arquivo protegido por age ou gpg no source; decriptado pelo chezmoi em apply-time."
- **hook** — *gancho*. "Script `run_once_` ou `run_onchange_` executado automaticamente em apply conforme condição de estado."
- **init** — *inicializar*. "Comando `chezmoi init` que clona o repo de dotfiles e configura o source directory na máquina."
- **apply** — *aplicar*. "Comando `chezmoi apply` que propaga as mudanças do source para o target, renderizando templates."
- **diff** — *diff*. "Comando `chezmoi diff` que exibe o que seria alterado no target sem aplicar; saída no formato unified diff."
- **update** — *atualizar*. "Comando `chezmoi update` que combina `git pull` no source com `chezmoi apply`; fluxo canônico de sync."

## Veja também

- [[01 - Princípios — o que são dotfiles e por que versionar]] — pré-req
- [[03 - Cross-OS — Linux vs macOS vs WSL]] — templates resolvem cross-OS
- [[04 - GNU stow — symlinks declarativos]] — alternativa mais simples
- [[06 - Bare git repo — abordagem minimalista]] — alternativa minimalista
- [[07 - Secrets em dotfiles — git-crypt, age, sops]] — encryption nativa do chezmoi
- [[03-Dominios/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#chezmoi|chezmoi]], [[Dicionário do Terminal#Template (dotfiles)|template]]

## Referências

- chezmoi docs: https://www.chezmoi.io/
- chezmoi quick start: https://www.chezmoi.io/quick-start/
- Go template syntax: https://pkg.go.dev/text/template
