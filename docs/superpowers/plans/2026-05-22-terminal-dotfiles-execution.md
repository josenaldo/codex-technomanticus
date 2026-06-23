# Galho 5 — Dotfiles — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar o galho 5 da trilha Terminal — 9 notas atômicas (3 Iniciado + 3 Adepto + 3 Magus) sobre dotfiles em `03-Dominios/Tecnologia/Terminal/Dotfiles/`, MOC do galho, expansão do Dicionário com bloco `## Dotfiles`, e ativação do wikilink no tronco. Formato catálogo comparativo das 3 ferramentas principais (stow, chezmoi, bare repo).

**Architecture:** Mesmo padrão consolidado nos galhos 2-4. Estrutura H2 fixa. Tom pedagógico — user em adoção zero. Exemplos sempre neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos. Fluxo SDD: implementer → reviewer combinado → fix se Critical/Important. Pesquisa-âncora em docs oficiais antes de cada nota.

**Tech Stack:** Obsidian + Quartz, Markdown + frontmatter YAML, wikilinks. Ferramentas-alvo das notas: GNU stow, chezmoi, git (bare repo), git-crypt, age, sops.

---

## Spec de referência

`docs/superpowers/specs/2026-05-22-terminal-dotfiles-design.md`

## Restrições absolutas (em TODOS os subagent prompts)

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `myproj`, `<user>`) ou hipotéticos explícitos (`# hipotético: ...`). NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de comandos/flags. Verificar via doc oficial.
3. **Sem `Co-Authored-By: Claude`**. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em `## Veja também`.
6. **Tronco wikilink obrigatório**: `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`.
7. **MOC wikilink** em "Veja também": `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`.
8. **≥5 armadilhas** por nota, cada uma com 4 labels (Causa / Sintoma / Como detectar / Solução).
9. **"Em inglês" em bullets bilíngues** `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
10. **Code fences corretos:** `bash` pra shell, `yaml`/`toml` pra config, `text` pra ASCII.
11. **Tom pedagógico** — assume zero conhecimento prévio em Iniciado.
12. **Comparações justas** — sem hype, sem desmerecimento entre ferramentas.

---

## Task 0: Pré-flight

**Files:**
- (nenhum — só captura)

- [ ] **Step 1: Capturar versões disponíveis**

```bash
stow --version 2>&1 | head -3 || echo "(stow não instalado)"
echo "---"
chezmoi --version 2>&1 || echo "(chezmoi não instalado)"
echo "---"
git --version
echo "---"
uname -a
echo "---"
cat /etc/os-release 2>&1 | head -5
```

Anotar versões e OS pra usar no Task 12.

- [ ] **Step 2: Verificar deps secundárias**

```bash
gpg --version 2>&1 | head -1 || echo "(gpg não instalado)"
command -v git-crypt && git-crypt --version 2>&1 || echo "(git-crypt não instalado)"
command -v age && age --version 2>&1 || echo "(age não instalado)"
command -v sops && sops --version 2>&1 || echo "(sops não instalado)"
```

Anotar — informa Magus 07.

---

## Task 1: MOC do galho Dotfiles — esqueleto

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/index.md`

- [ ] **Step 1: Criar pasta**

```bash
mkdir -p "03-Dominios/Tecnologia/Terminal/Dotfiles"
```

- [ ] **Step 2: Escrever MOC**

Use `Write` em `03-Dominios/Tecnologia/Terminal/Dotfiles/index.md`:

```markdown
---
title: "Dotfiles"
type: moc
publish: true
created: 2026-05-22
updated: 2026-05-22
status: growing
progresso: andamento
tags:
  - terminal
  - dotfiles
  - moc
aliases:
  - Dotfiles
---
# Dotfiles

> [!abstract] TL;DR
> Galho 5 da trilha Terminal. Domínio de dotfiles — arquivos de config (`.zshrc`, `.gitconfig`, `~/.config/*`) versionados e syncados entre máquinas. 9 notas (3 Iniciado + 3 Adepto + 3 Magus). Formato catálogo comparativo das 3 ferramentas principais: GNU stow, chezmoi, bare git repo.

Esse galho parte do zero (o que são dotfiles, por que versionar) até workflows operacionais avançados (secrets encryption, bootstrap automático, sync entre máquinas heterogêneas). As 3 ferramentas principais recebem profundidade equivalente — Adepto cobre stow, chezmoi e bare repo em notas separadas com mesmos critérios, deixando o leitor escolher informadamente.

## Conteúdo

### Iniciado

- [[01 - Princípios — o que são dotfiles e por que versionar]]
- [[02 - Anatomia — estrutura típica e XDG Base Directory]]
- [[03 - Cross-OS — Linux vs macOS vs WSL]]

### Adepto

- [[04 - GNU stow — symlinks declarativos]]
- [[05 - chezmoi — manager completo com templates]]
- [[06 - Bare git repo — abordagem minimalista]]

### Magus

- [[07 - Secrets em dotfiles — git-crypt, age, sops]]
- [[08 - Bootstrap — máquina nova zero-to-ready]]
- [[09 - Sync entre máquinas heterogêneas]]

## Rotas alternativas

- **Mínimo viável** (entender + 1 ferramenta): `01` → `02` → `04`
- **Comparativo das ferramentas**: `01` → `02` → `04` → `05` → `06`
- **Maestria operacional**: `04` (ou `05`) → `07` → `08` → `09`
- **Cross-OS first**: `01` → `02` → `03` → `05`

## Versões assumidas

- **GNU stow:** `<VERSAO_STOW>` (capturada no pré-flight)
- **chezmoi:** `<VERSAO_CHEZMOI>` (capturada no pré-flight)
- **git:** `<VERSAO_GIT>` (capturada no pré-flight)
- **OS de referência:** `<OS_REF>`

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/index.md"
git commit -m "feat(terminal-dotfiles): MOC do galho 5 — esqueleto"
```

---

## Task 2: Dicionário — bloco "Dotfiles" esqueleto

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Localizar fim do bloco TUIs**

Use `Read` no final do Dicionário pra encontrar o último verbete do bloco `## TUIs de Dev / Lazygit / Lazydocker` (último alfabético: `Worktree`).

- [ ] **Step 2: Inserir header**

Após o último verbete `### Worktree` + "Veja também:", inserir:

```markdown
## Dotfiles

```

Use `Edit`: `old_string` = bloco final do verbete Worktree (5 linhas), `new_string` = mesmo + `## Dotfiles\n\n`.

- [ ] **Step 3: Confirmar `updated:`**

Frontmatter deve ter `updated: 2026-05-22`. Se não, Edit.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): adiciona bloco 'Dotfiles' ao Dicionário"
```

---

## Task 3: Nota 01 — Princípios: o que são dotfiles e por que versionar

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/01 - Princípios — o que são dotfiles e por que versionar.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbete: Dotfile)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://wiki.archlinux.org/title/Dotfiles
WebFetch: https://dotfiles.github.io/
```

Capturar: definição canônica, origem histórica do nome, padrões de uso.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Princípios — o que são dotfiles e por que versionar"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - dotfiles
  - iniciado
  - principios
aliases:
  - Princípios dotfiles
---
```

- [ ] **Step 3: Escrever nota**

Estrutura: callout TL;DR + H2s (O que é/Como funciona, Na prática, Armadilhas, Em inglês, Veja também, Referências).

**TL;DR (callout):**
"Dotfile = arquivo de configuração começando com `.` (oculto no `ls` por convenção Unix). Exemplos: `~/.zshrc`, `~/.gitconfig`, `~/.config/nvim/init.lua`. Por que versionar: setup repetível, sync entre máquinas, history de mudanças, dotfiles públicos como portfólio. O QUE não versionar: secrets sem encryption, configs geradas (P10k wizard output, OAuth tokens), paths absolutos hardcoded."

**O que é / Como funciona** (H3s):

### Definição e origem do nome
- Dotfile = arquivo cujo nome começa com `.`
- Convenção Unix antiga: `ls` por default não mostra files começando com `.` (`ls -a` mostra)
- Origem: nos anos 70 alguém quis evitar mostrar `.` e `..` em `ls`; convenção pegou e virou padrão pra "metadata/config oculta"
- Resultado moderno: configs de aplicações vivem em arquivos `.algo` em `$HOME` ou pasta `.config/`

### Exemplos comuns no home (Linux/macOS moderno)
- `~/.zshrc` — config Zsh
- `~/.bashrc` — config Bash
- `~/.gitconfig` — config git global (user.name, user.email, aliases)
- `~/.ssh/config` — config SSH (Host blocks)
- `~/.gnupg/` — keys GPG (NÃO versionar como-está; secrets!)
- `~/.config/nvim/init.lua` — config Neovim
- `~/.config/zellij/config.kdl` — config Zellij
- `~/.config/lazygit/config.yml` — config Lazygit

### Por que versionar dotfiles
- **Setup repetível:** máquina nova fica idêntica em minutos (não horas)
- **Sync entre máquinas:** edita no laptop, pull no desktop
- **History de mudanças:** "por que mudei isso?" → `git log`
- **Backup natural:** repo remoto (GitHub/GitLab) protege contra perda
- **Portfolio:** `github.com/<user>/dotfiles` vira CV demonstrável de skill
- **Compartilhamento:** ver dotfiles de outros é a melhor forma de aprender

### O que NÃO versionar
- **Secrets sem encryption:** API tokens, senhas em plaintext, SSH/GPG private keys (sem encryption)
- **Configs geradas por wizard:** `~/.p10k.zsh` (gerado por `p10k configure`), arquivos auto-gerados
- **Paths hardcoded por usuário:** `/home/alice/specific-path/...` que não funciona em outra máquina
- **Cache/state:** `~/.cache/`, `~/.local/state/` — descartável
- **Configs de single-shot tools:** OAuth tokens, refresh tokens (rotacionam)

### Cultura dotfiles no GitHub
- Pasta `dotfiles/` ou repo dedicado `<user>/dotfiles` é convenção
- Listado em sites como dotfiles.github.io
- README explica setup steps (clone + ferramenta de aplicação)
- Vira referência aprendizado pra outros

**Na prática** (H3s):

### Ver seus dotfiles atuais
```bash
ls -la ~ | grep '^\.' | head -20         # legacy (direto em $HOME)
ls -la ~/.config/ 2>&1 | head -20        # XDG (em ~/.config/)
```

### Inventário rápido (decisão "o que vale versionar")
Critérios de inclusão:
1. **Você editou manualmente?** Sim → versionar.
2. **É config (vs cache/state)?** Sim → versionar.
3. **Tem secret?** Sim → encriptar primeiro (nota 07) ou não versionar.
4. **Funciona em outra máquina?** Sim → versionar. Não (paths hardcoded) → refatorar primeiro.

### Roadmap pra adoção
```text
1. Escolher ferramenta (stow / chezmoi / bare repo — notas 04-06)
2. Criar repo público (GitHub) ou privado
3. Adicionar dotfiles aos poucos (zsh primeiro; depois git; depois config/)
4. Testar restore em VM ou container
5. Lidar com secrets quando aparecer necessidade (nota 07)
```

**Armadilhas (≥5, 4 labels):**

1. **Commitar secret em plaintext**
   - **Causa:** copiar arquivo com API token sem revisar.
   - **Sintoma:** secret aparece em `git log` / GitHub público.
   - **Como detectar:** `git log -p | grep -iE "(token|password|api[_-]?key)"`.
   - **Solução:** se já pushado, **rotacionar o secret IMEDIATAMENTE** (assumir vazado). Depois `git filter-repo` ou BFG pra purgar history; force-push.

2. **Versionar `~/.ssh/id_rsa` (private key)**
   - **Causa:** copiar `.ssh/` inteiro sem filtrar.
   - **Sintoma:** chave privada em repo (público ou não).
   - **Como detectar:** `git ls-files | grep id_rsa`.
   - **Solução:** versionar SÓ `~/.ssh/config` (com `Host` blocks). Private keys: gerar novas localmente, copiar manualmente em máquinas novas. Ou usar encryption (nota 07).

3. **Versionar configs com paths hardcoded**
   - **Causa:** `/home/alice/projects/foo` literal em config.
   - **Sintoma:** funciona em alice; falha em bob (path não existe).
   - **Como detectar:** clone em VM com user diferente, testa.
   - **Solução:** usar `$HOME`, `~`, ou template engine (chezmoi templates — nota 05).

4. **Esquecer `.gitignore` ampla → repo polui com cache/state**
   - **Causa:** sem ignore, `~/.cache`, `~/.local/state` viram parte do repo.
   - **Sintoma:** repo gigante (centenas de MB), commits cheios de noise.
   - **Como detectar:** `du -sh .git/`.
   - **Solução:** bare repo usa whitelist (`*` + `!nome` específico); stow só vê o que está na pasta; chezmoi tem source explícita.

5. **Atualizar em uma máquina, esquecer de sync — divergência silenciosa**
   - **Causa:** editou no laptop, esqueceu de commit; depois editou no desktop a partir de versão antiga.
   - **Sintoma:** conflito feio no merge ou perda de mudança.
   - **Como detectar:** `git status` regular antes de editar.
   - **Solução:** hábito de `git pull && edit && commit && push` em cada máquina. Notas 04-06 mostram aliases que facilitam isso.

6. **Versionar config gerada por wizard (`.p10k.zsh`, etc.) e editar à mão depois**
   - **Causa:** rodar wizard sobrescreve sua edição manual.
   - **Sintoma:** customização desaparece após `p10k configure` ou similar.
   - **Como detectar:** comparar antes/depois do wizard com `git diff`.
   - **Solução:** ou comprometer com wizard (re-rodar sempre que mudar), ou comentar diff no topo do file (`# CUSTOM: ...`), ou usar template (chezmoi) pra gerar.

**Em inglês (8-10 bullets bilíngues):**
Termos: dotfile, versionar (version), sync (sync), repo (repo), home directory, hidden file, config, portfolio, idempotent, bootstrap.

Formato `- **PT** — *EN*. "frase técnica curta em PT."`.

**Veja também:**
- `[[02 - Anatomia — estrutura típica e XDG Base Directory]]` — anatomia detalhada
- `[[03 - Cross-OS — Linux vs macOS vs WSL]]` — diferenças entre OSes
- `[[04 - GNU stow — symlinks declarativos]]` — ferramenta mais simples pra começar
- `[[07 - Secrets em dotfiles — git-crypt, age, sops]]` — encryption pra dados sensíveis
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Dotfile|dotfile]]`

**Referências:**
- Arch Wiki — Dotfiles: https://wiki.archlinux.org/title/Dotfiles
- Dotfiles community: https://dotfiles.github.io/

- [ ] **Step 4: 1 verbete pro Dicionário**

Inserir no bloco `## Dotfiles` (atualmente vazio):

```markdown
### Dotfile
Arquivo de configuração de aplicação cujo nome começa com `.` (oculto no `ls` por default), tipicamente em `$HOME` ou `~/.config/`. Exemplos: `~/.zshrc`, `~/.gitconfig`, `~/.config/nvim/init.lua`. Versionar dotfiles permite setup repetível, sync entre máquinas e history de mudanças.

Veja também: [[01 - Princípios — o que são dotfiles e por que versionar]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/01 - Princípios — o que são dotfiles e por que versionar.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/01 - Princípios — o que são dotfiles e por que versionar.md"
grep -E "^### Dotfile$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥7 wikilinks, verbete Dotfile visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/01 - Princípios — o que são dotfiles e por que versionar.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 01 — Princípios"
```

---

## Task 4: Nota 02 — Anatomia: estrutura típica + XDG Base Directory spec

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/02 - Anatomia — estrutura típica e XDG Base Directory.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbete: XDG Base Directory)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
WebFetch: https://wiki.archlinux.org/title/XDG_Base_Directory
```

Confirmar: env vars exatas, defaults, apps que respeitam vs ignoram.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Anatomia — estrutura típica e XDG Base Directory"
created: 2026-05-22
updated: 2026-05-22
type: concept
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
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Dotfiles antigos vivem direto em `$HOME` (`~/.bashrc`, `~/.vimrc`). XDG Base Directory spec (freedesktop.org) moderniza: `$XDG_CONFIG_HOME` (`~/.config/`), `$XDG_DATA_HOME` (`~/.local/share/`), `$XDG_CACHE_HOME` (`~/.cache/`), `$XDG_STATE_HOME` (`~/.local/state/`). Apps modernos (Neovim, Zellij, Lazygit) respeitam. Apps legados (bash, git, ssh) ignoram. Separação: backup só config; clean cache facilmente; não polui home."

**O que é / Como funciona** (H3s):

### Layout legacy (anos 90/00)
- Tudo direto em `$HOME`: `~/.bashrc`, `~/.vimrc`, `~/.gitconfig`, `~/.profile`
- Cada app com convenção própria (`.vim/`, `.emacs.d/`, `.mozilla/`)
- Resultado: `ls -la ~` mostra dezenas de `.algo/` poluindo

### Layout XDG (moderno, padrão freedesktop.org)
Spec: https://specifications.freedesktop.org/basedir-spec/

Variáveis e defaults:
- `$XDG_CONFIG_HOME` — default `~/.config/` — **configs do usuário**
- `$XDG_DATA_HOME` — default `~/.local/share/` — **dados de usuário** (state persistente: history, bookmarks)
- `$XDG_CACHE_HOME` — default `~/.cache/` — **cache** (descartável)
- `$XDG_STATE_HOME` — default `~/.local/state/` — **state runtime** (logs, last session, undo files)
- `~/.local/bin/` — **binários do usuário** (não-XDG mas convenção forte; deveria estar em `$PATH`)

### Por que XDG existe
1. **Separa config/data/cache:** backup só config; clean cache facilmente
2. **Não polui `$HOME`:** `ls -la ~` fica respirável
3. **Múltiplos configs por user:** alternar `XDG_CONFIG_HOME` muda o app pra outro perfil
4. **Padrão multi-OS:** Linux moderno, macOS (parcial), BSD

### Apps que respeitam XDG (modernos)
- Neovim → `~/.config/nvim/`
- Zellij → `~/.config/zellij/`
- Lazygit → `~/.config/lazygit/`
- Lazydocker → `~/.config/lazydocker/`
- fish → `~/.config/fish/`
- atuin → `~/.config/atuin/`
- helix → `~/.config/helix/`
- starship → `~/.config/starship.toml`

### Apps que ignoram XDG (legados)
- bash → `~/.bashrc` (não `~/.config/bash/`)
- git → `~/.gitconfig` (mas aceita `$XDG_CONFIG_HOME/git/config` se setado!)
- ssh → `~/.ssh/`
- gpg → `~/.gnupg/`
- vim (sem nvim) → `~/.vimrc`

### Como forçar XDG em app que ignora
Algumas opções:
- **Env var explícita:** `export HISTFILE=$XDG_STATE_HOME/bash/history` no shell
- **Flag de comando:** `git -c includeIf...` pra paths custom
- **Wrapper alias:** `alias gpg='gpg --homedir $XDG_CONFIG_HOME/gnupg'`
- **Aceitar e deixar legacy:** muitos não brigam com isso

### `~/.local/bin/` — binários do user
- Não é XDG strict, mas convenção
- Adicione ao `$PATH`: `export PATH="$HOME/.local/bin:$PATH"` no shell rc
- Lugar pra scripts custom, binários instalados via `pip install --user`, `cargo install`, etc.

**Na prática** (H3s):

### Inventário XDG na máquina
```bash
# Ver env vars XDG (definidas ou não)
echo "CONFIG: ${XDG_CONFIG_HOME:-$HOME/.config (default)}"
echo "DATA:   ${XDG_DATA_HOME:-$HOME/.local/share (default)}"
echo "CACHE:  ${XDG_CACHE_HOME:-$HOME/.cache (default)}"
echo "STATE:  ${XDG_STATE_HOME:-$HOME/.local/state (default)}"

# Listar configs em ~/.config
ls -la ~/.config/ 2>/dev/null | head -20

# Tamanho do cache
du -sh ~/.cache/ 2>/dev/null
```

### Setup XDG completo no shell (zsh exemplo)
```zsh
# ~/.zshenv (carrega em todo shell, login ou não)
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"

# Forçar apps legados a usar XDG (alguns)
export HISTFILE="$XDG_STATE_HOME/zsh/history"
mkdir -p "${HISTFILE%/*}"

# Adicionar ~/.local/bin ao PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Limpar cache periódico
```bash
# Cache descartável — pode deletar inteiro
du -sh ~/.cache/* | sort -hr | head -10
# Deletar caches grandes específicos (sempre conferir antes)
# rm -rf ~/.cache/nome-do-app/
```

**Armadilhas (≥5, 4 labels):**

1. **Editar `$XDG_CACHE_HOME` esperando persistência**
   - **Causa:** cache é tratado como descartável por apps; podem limpar.
   - **Sintoma:** mudanças desaparecem.
   - **Como detectar:** ler doc do app.
   - **Solução:** mover dados persistentes pra `$XDG_DATA_HOME`.

2. **`$XDG_CONFIG_HOME` definida vazia (`export XDG_CONFIG_HOME=`)**
   - **Causa:** export sem valor.
   - **Sintoma:** apps procuram em `/` ou path absurdo.
   - **Como detectar:** `echo "$XDG_CONFIG_HOME"` retorna linha vazia.
   - **Solução:** se setar, valor não-vazio; se não setar, deixar unset (apps usam default).

3. **Versionar `~/.cache/` por engano**
   - **Causa:** stow numa pasta com `.cache/` ou whitelist mal-feita.
   - **Sintoma:** repo enorme, history poluído.
   - **Como detectar:** `du -sh .git/`, `git ls-files | grep cache`.
   - **Solução:** ignorar explicitamente. Cache nunca vai pro repo.

4. **App escreve em `~/.app/` em vez de `~/.config/app/`**
   - **Causa:** app não respeita XDG.
   - **Sintoma:** config aparece em `$HOME` direto, não em `~/.config/`.
   - **Como detectar:** `ls -la ~ | grep '^\.' | grep -v config`.
   - **Solução:** verificar se app aceita env var (`APP_CONFIG_DIR`) ou flag; senão, aceitar e versionar onde tá.

5. **Confundir `~/.local/share/` (data) com `~/.local/bin/` (binários)**
   - **Causa:** nomes parecem próximos.
   - **Sintoma:** binário não roda (não está no PATH); ou dados em `.local/bin/` quebram organização.
   - **Como detectar:** ler structure.
   - **Solução:** `bin/` é só pra executáveis; `share/` é pra dados (apps instalados via `pipx`, `cargo`, etc. tipicamente vão em `~/.local/share/<app>/`).

**Em inglês (8-10 bullets bilíngues):**
Termos: spec, base directory, environment variable, fallback, cache, state, namespace, legacy, convention, override.

**Veja também:**
- `[[01 - Princípios — o que são dotfiles e por que versionar]]` — pré-req
- `[[03 - Cross-OS — Linux vs macOS vs WSL]]` — XDG em outros OSes
- `[[04 - GNU stow — symlinks declarativos]]` — stow respeita XDG naturalmente
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#XDG Base Directory|XDG]]`, `[[Dicionário do Terminal#Dotfile|dotfile]]`

**Referências:**
- XDG Base Directory spec: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
- Arch Wiki — XDG: https://wiki.archlinux.org/title/XDG_Base_Directory

- [ ] **Step 4: 1 verbete pro Dicionário**

```markdown
### XDG Base Directory
Spec freedesktop.org que define paths padronizados pra configs (`$XDG_CONFIG_HOME` → `~/.config/`), dados (`$XDG_DATA_HOME` → `~/.local/share/`), cache (`$XDG_CACHE_HOME` → `~/.cache/`) e state (`$XDG_STATE_HOME` → `~/.local/state/`). Apps modernos respeitam; legados (bash, git, ssh) tipicamente ignoram.

Veja também: [[02 - Anatomia — estrutura típica e XDG Base Directory]].
```

Inserir em ordem alfabética. Bloco atual: Dotfile. XDG vem depois de Dotfile alfabeticamente (D < X).

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/02 - Anatomia — estrutura típica e XDG Base Directory.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/02 - Anatomia — estrutura típica e XDG Base Directory.md"
grep -E "^### XDG Base Directory$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/02 - Anatomia — estrutura típica e XDG Base Directory.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 02 — Anatomia + XDG"
```

---

## Task 5: Nota 03 — Cross-OS: Linux vs macOS vs WSL

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/03 - Cross-OS — Linux vs macOS vs WSL.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbete: WSL)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://learn.microsoft.com/en-us/windows/wsl/about
WebFetch: https://en.wikipedia.org/wiki/Bash_(Unix_shell)
```

Confirmar: estados atuais dos sistemas, comportamentos default.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Cross-OS — Linux vs macOS vs WSL"
created: 2026-05-22
updated: 2026-05-22
type: concept
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
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Dotfiles que funcionam em Linux podem quebrar em macOS ou WSL. Diferenças críticas: paths (`/home/<user>` vs `/Users/<user>`), shell default (bash GNU vs zsh em macOS ≥ Catalina), package manager (apt/dnf vs brew vs scoop), GNU vs BSD utilities (`sed -i` syntax difference). Quando dotfile precisa branch: env var `OSTYPE`, `chezmoi` templates, ou script externo. WSL específico: interop com Windows via `/mnt/c/`."

**O que é / Como funciona** (H3s):

### Paths de home
- **Linux:** `/home/<user>` (em maioria das distros)
- **macOS:** `/Users/<user>`
- **WSL:** `/home/<user>` dentro da distro; Windows visível em `/mnt/c/Users/<user>/`
- **Importante:** sempre usar `$HOME` ou `~` em dotfiles, NUNCA hardcode

### Shell default
- **Linux:** bash em maioria; Arch/Manjaro às vezes zsh
- **macOS:** zsh desde Catalina (2019); antes era bash
- **WSL:** depende da distro (Ubuntu → bash; Arch → bash; depende)
- **Implicação:** se dotfile inclui `~/.zshrc` e a máquina usa bash, não aplica

### Package manager
- **Linux (Debian/Ubuntu):** `apt` (`apt install pkg`)
- **Linux (Fedora/RHEL):** `dnf` (`dnf install pkg`)
- **Linux (Arch):** `pacman` (`pacman -S pkg`)
- **macOS:** Homebrew (`brew install pkg`)
- **macOS (opcional):** MacPorts (alternativa menos comum)
- **Linux+macOS unificado:** Homebrew funciona em Linux também (linuxbrew); Nix funciona em ambos
- **WSL:** package manager da distro WSL (bash dentro de Ubuntu WSL = `apt`)

### GNU vs BSD utilities
Linux usa GNU coreutils; macOS usa BSD utils. Diferenças sutis quebram dotfiles:

**`sed -i` (in-place edit):**
- GNU: `sed -i 's/a/b/' file` (sem arg)
- BSD (macOS): `sed -i '' 's/a/b/' file` (string vazia obrigatória)
- Workaround: `sed -i.bak 's/a/b/' file` funciona em ambos (cria backup)

**`grep -P` (Perl regex):**
- GNU: suportado
- BSD: não suportado por default; precisa `ggrep` (via `brew install grep`)

**`readlink -f`, `realpath`:**
- GNU: ambos disponíveis
- BSD: `readlink` sem `-f`; `realpath` precisa `coreutils` (`brew install coreutils` → `grealpath`)

**`date` formatting:**
- GNU: `date -d 'yesterday'`
- BSD: `date -v-1d`

### Quando dotfile precisa branch por OS

Detectar OS em shell:
```bash
case "$OSTYPE" in
  linux-gnu*)   OS=linux ;;
  darwin*)      OS=macos ;;
  msys*|cygwin*) OS=windows ;;
  *)            OS=unknown ;;
esac

# Ou alternativa
case "$(uname -s)" in
  Linux*)  OS=linux ;;
  Darwin*) OS=macos ;;
esac
```

Aliases conditional:
```bash
if [[ "$OS" == "macos" ]]; then
  alias ls='gls --color=auto'  # GNU ls via brew
else
  alias ls='ls --color=auto'
fi
```

Detecção WSL específica:
```bash
if grep -qi microsoft /proc/version 2>/dev/null; then
  OS=wsl
fi
```

### WSL — especificidades

- **Interop com Windows:** `cmd.exe`, `powershell.exe`, `wsl.exe`
- **Filesystem cross:** `/mnt/c/Users/<user>/` é Windows visto do WSL; `\\wsl$\Ubuntu\` é WSL visto do Windows
- **Performance:** I/O entre `/mnt/c/` e `/home/` é LENTO. Trabalhar em `/home/<user>/...` se possível
- **Clipboard:** `clip.exe` (envia pra clipboard Windows). Pra colar do Windows, `powershell.exe -c "Get-Clipboard"`
- **VS Code remote:** WSL extension permite editar arquivos WSL no VS Code Windows
- **Network:** WSL2 tem IP próprio; localhost geralmente funciona ambas direções

**Na prática** (H3s):

### Setup OS detection completo no zsh
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
  Darwin*) export DOTFILES_OS=macos ;;
  *)       export DOTFILES_OS=unknown ;;
esac
```

### Conditional source no shell rc
```zsh
# ~/.zshrc
[[ -f "$HOME/.config/zsh/$DOTFILES_OS.zsh" ]] && source "$HOME/.config/zsh/$DOTFILES_OS.zsh"
```

Cria pastas/files:
- `~/.config/zsh/linux.zsh` — aliases/exports Linux
- `~/.config/zsh/macos.zsh` — aliases/exports macOS (brew prefix, GNU coreutils path)
- `~/.config/zsh/wsl.zsh` — interop Windows

### macOS — corrigir GNU vs BSD
```bash
# Instalar GNU coreutils
brew install coreutils gnu-sed grep findutils

# No shell rc — usar GNU como default
export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"
export PATH="/opt/homebrew/opt/gnu-sed/libexec/gnubin:$PATH"
export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"
```

(Path do brew varia: `/usr/local/...` no Intel, `/opt/homebrew/...` em Apple Silicon.)

### WSL — abrir Windows path do bash
```bash
# Abrir explorer no cwd
explorer.exe .

# Abrir VS Code no cwd
code .

# Converter path
wslpath -w ~/projects/foo    # /home/alice/... → \\wsl$\Ubuntu\home\alice\...
wslpath -u 'C:\Users\Alice'  # C:\... → /mnt/c/...
```

**Armadilhas (≥5, 4 labels):**

1. **Dotfile com `/home/<user>` hardcoded falha em macOS**
   - **Causa:** macOS usa `/Users/<user>`, não `/home/`.
   - **Sintoma:** path inválido; comandos falham.
   - **Como detectar:** `grep -r '/home/' ~/dotfiles/`.
   - **Solução:** sempre `$HOME` ou `~`.

2. **`sed -i 's/a/b/' file` quebra em macOS sem warning**
   - **Causa:** BSD sed requer arg pra `-i` (string vazia).
   - **Sintoma:** Linux ok; macOS cria arquivo `s/a/b/`.
   - **Como detectar:** rodar script em macOS.
   - **Solução:** `sed -i.bak 's/a/b/' file` (funciona em ambos), depois `rm file.bak`.

3. **Brew path errado em Apple Silicon vs Intel**
   - **Causa:** Apple Silicon usa `/opt/homebrew/`, Intel usa `/usr/local/`.
   - **Sintoma:** apps via brew não no PATH.
   - **Como detectar:** `which brew` ou `arch`.
   - **Solução:** `eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"` no rc.

4. **WSL — I/O em `/mnt/c/` 10x mais lento que `/home/`**
   - **Causa:** filesystem 9P entre WSL e Windows.
   - **Sintoma:** `npm install` em `/mnt/c/projeto` leva 5 min; em `/home/alice/projeto`, 30s.
   - **Como detectar:** comparar tempos.
   - **Solução:** trabalhar projetos em `/home/<user>/`; só usar `/mnt/c/` pra acessar files Windows ocasionalmente.

5. **Versionar shell rc do WSL como `linux.zsh`**
   - **Causa:** WSL é Linux mas tem peculiaridades (interop).
   - **Sintoma:** `linux.zsh` source em WSL puxa configs que assumem `/home/...` puro, sem interop.
   - **Como detectar:** comparar setups.
   - **Solução:** detectar WSL separadamente (`grep microsoft /proc/version`); arquivo `wsl.zsh` separado pra interop.

**Em inglês (8-10 bullets bilíngues):**
Termos: cross-platform, OS detection, package manager, utility, interop, path translation, native, portable, abstract, branching.

**Veja também:**
- `[[01 - Princípios — o que são dotfiles e por que versionar]]` — pré-req
- `[[02 - Anatomia — estrutura típica e XDG Base Directory]]` — pré-req
- `[[05 - chezmoi — manager completo com templates]]` — templates são solução pra cross-OS
- `[[09 - Sync entre máquinas heterogêneas]]` — sync entre OSes diferentes
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#WSL|WSL]]`, `[[Dicionário do Terminal#Dotfile|dotfile]]`

**Referências:**
- WSL docs: https://learn.microsoft.com/en-us/windows/wsl/
- macOS shell change (2019): https://support.apple.com/en-us/102360

- [ ] **Step 4: 1 verbete pro Dicionário**

```markdown
### WSL
Windows Subsystem for Linux — execução de Linux dentro de Windows via WSL2 (com kernel completo). Filesystem cross-OS: `/mnt/c/` é Windows visto do WSL; `\\wsl$\Ubuntu\` é WSL visto do Windows. I/O entre os dois é lento — trabalhar em `/home/` por padrão. Interop via `cmd.exe`, `powershell.exe`, `clip.exe`.

Veja também: [[03 - Cross-OS — Linux vs macOS vs WSL]].
```

Ordem alfabética no bloco. Atualmente: Dotfile, XDG. WSL entra antes de XDG (W < X).

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/03 - Cross-OS — Linux vs macOS vs WSL.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/03 - Cross-OS — Linux vs macOS vs WSL.md"
grep -E "^### WSL$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/03 - Cross-OS — Linux vs macOS vs WSL.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 03 — Cross-OS"
```

---

## ✅ Checkpoint Iniciado

Após Task 5, 3 notas de Iniciado entregues. Total no galho: 3 notas + MOC.

---

## Task 6: Nota 04 — GNU stow: symlinks declarativos

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/04 - GNU stow — symlinks declarativos.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: Stow, Symlink)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://www.gnu.org/software/stow/manual/stow.html
WebFetch: https://www.gnu.org/software/stow/
```

Confirmar: comandos, flags, conflitos handling, versão atual.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "GNU stow — symlinks declarativos"
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
  - stow
  - symlink
aliases:
  - GNU stow
  - Stow
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"GNU stow é o gerenciador de dotfiles mais simples: 1 pasta por 'package' no repo, `stow <pkg>` cria symlinks no home com a mesma estrutura. Exemplo: `~/dotfiles/zsh/.zshrc` + `stow zsh` → `~/.zshrc` (symlink). `stow -D` unstow; `--adopt` adota files existentes. Vantagens: simples, sem state file, Unix-nativo. Desvantagens: sem templates, sem cross-OS automático, sem secrets."

**O que é / Como funciona** (H3s):

### Conceito básico
- stow = "stow away" (guardar de forma organizada)
- Filosofia: você mantém os files no repo (`~/dotfiles/`); stow cria symlinks no home apontando pra eles
- Resultado: edita no repo, mudança aparece no home; edita no home (via symlink), mudança vai pro repo

### Estrutura repo "stow-friendly"
```
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

Cada pasta direta de `~/dotfiles/` é um "package". O conteúdo é estrutura relativa a `$HOME`.

### Comandos essenciais
```bash
cd ~/dotfiles

# Aplica (cria symlinks)
stow zsh         # cria ~/.zshrc, ~/.zshenv como symlinks

# Remove symlinks
stow -D zsh      # remove ~/.zshrc, ~/.zshenv (arquivos no repo intactos)

# Re-aplica (unstow + stow)
stow -R zsh      # útil após reorganizar dentro do package

# Verbose (mostra o que faz)
stow -v zsh

# Dry-run (mostra o que faria, sem executar)
stow -n zsh

# Target diferente (default é parent dir do repo, ou seja, $HOME se repo está em ~/dotfiles)
stow -t /etc -d /path/to/repo apache

# Adopt (mover file existente pro repo, criar symlink no lugar)
stow --adopt zsh    # raro; útil pra migração inicial
```

### Conflict handling
- Se `~/.zshrc` já existe (não-symlink) e você `stow zsh`, stow **falha** com erro:
  ```
  WARNING! stowing zsh would cause conflicts:
    * existing target is neither a link nor a directory: .zshrc
  ```
- Solução: ou backup do file existente e remove, ou `stow --adopt zsh` (move pro repo).

### O que `stow --adopt` faz
- Move file existente do home pro repo
- Cria symlink no home apontando pro file movido
- **Atenção:** sobrescreve file do repo com versão do home! Sempre `git status` antes pra ver se overwriting.

### Limitações
1. **Sem templates** — não pode rodar lógica em apply (e.g. inserir hostname)
2. **Sem cross-OS automático** — pra OS-specific, você precisa pastas separadas (`zsh-linux/`, `zsh-macos/`) e stow do correto
3. **Sem secrets nativos** — encryption fica externa (usar git-crypt em files do repo)
4. **Sem state file** — vantagem (simples) e desvantagem (sem "memory" do que foi stowed; só `find ~ -lname '*/dotfiles/*'` pra inventário)

**Na prática** (H3s):

### Setup inicial
```bash
# 1. Criar repo
mkdir -p ~/dotfiles
cd ~/dotfiles
git init

# 2. Criar package pro zsh
mkdir -p zsh
mv ~/.zshrc zsh/.zshrc      # cuidado: move file existente
stow zsh                      # cria ~/.zshrc como symlink → ~/dotfiles/zsh/.zshrc

# 3. Confirmar
ls -la ~/.zshrc              # deve mostrar -> .../dotfiles/zsh/.zshrc

# 4. Commit
git add zsh/
git commit -m "add zsh package"
```

### Adicionar mais packages
```bash
mkdir -p ~/dotfiles/nvim/.config/nvim
mv ~/.config/nvim/init.lua ~/dotfiles/nvim/.config/nvim/init.lua
cd ~/dotfiles && stow nvim
```

### Aplicar tudo numa máquina nova
```bash
git clone https://github.com/alice/dotfiles ~/dotfiles
cd ~/dotfiles
stow zsh nvim git tmux      # cria symlinks pra todos os packages
```

### Cross-OS com stow (manual)
```bash
~/dotfiles/
├── zsh-linux/
│   └── .zshrc
├── zsh-macos/
│   └── .zshrc
└── shared/
    └── .gitconfig

# No bootstrap script:
case "$(uname -s)" in
  Linux*)  cd ~/dotfiles && stow zsh-linux shared ;;
  Darwin*) cd ~/dotfiles && stow zsh-macos shared ;;
esac
```

**Armadilhas (≥5, 4 labels):**

1. **`stow` em diretório errado cria symlinks em path inesperado**
   - **Causa:** stow assume target = parent do current dir; se cd em pasta errada, symlinks vão pro lugar errado.
   - **Sintoma:** symlinks aparecem em `~/dotfiles/.zshrc` em vez de `~/.zshrc`.
   - **Como detectar:** `ls -la ~/.zshrc` mostra path real.
   - **Solução:** sempre `cd ~/dotfiles && stow <pkg>`; ou explicit `stow -t ~ -d ~/dotfiles <pkg>`.

2. **Stow recusa quando home tem file não-symlink existente**
   - **Causa:** evita destruir dados.
   - **Sintoma:** "would cause conflicts".
   - **Como detectar:** ler erro.
   - **Solução:** mover file existente pro repo manualmente, ou `--adopt`.

3. **`--adopt` sobrescreve file do repo com versão do home**
   - **Causa:** adopt copia home → repo; se home tem versão mais antiga, perde repo.
   - **Sintoma:** changes recentes no repo desaparecem.
   - **Como detectar:** `git diff` antes de `--adopt`.
   - **Solução:** `git status` clean ANTES; ou commit antes de adopt; ou copy + manual review.

4. **Dotfiles do `~/.config/` ficam em estrutura aninhada — stow precisa replicar**
   - **Causa:** XDG layout = `~/.config/nvim/`; no package precisa `nvim/.config/nvim/`.
   - **Sintoma:** `stow nvim` cria `~/.config/nvim/init.lua` apenas se package está com structure correta.
   - **Como detectar:** ler `stow -v -n nvim` (dry-run verbose).
   - **Solução:** estrutura do package replica path absoluto (sem o `~`): `nvim/.config/nvim/init.lua` → `~/.config/nvim/init.lua`.

5. **Stow re-aplicado após mover file dentro do package quebra symlinks**
   - **Causa:** stow não detecta moves; vê arquivo "novo" e antigo orphan.
   - **Sintoma:** symlinks quebrados (apontam pra inexistente).
   - **Como detectar:** `find ~ -xtype l` (lista symlinks órfãos).
   - **Solução:** `stow -R <pkg>` (restow) limpa e recria.

**Em inglês (8-10 bullets bilíngues):**
Termos: symlink, package, target, source, adopt, conflict, dry-run, declarative, idempotent, restow.

**Veja também:**
- `[[01 - Princípios — o que são dotfiles e por que versionar]]` — pré-req
- `[[02 - Anatomia — estrutura típica e XDG Base Directory]]` — pré-req
- `[[05 - chezmoi — manager completo com templates]]` — alternativa com templates
- `[[06 - Bare git repo — abordagem minimalista]]` — alternativa minimalista
- `[[08 - Bootstrap — máquina nova zero-to-ready]]` — usa stow no bootstrap
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Stow|stow]]`, `[[Dicionário do Terminal#Symlink|symlink]]`

**Referências:**
- GNU stow manual: https://www.gnu.org/software/stow/manual/stow.html
- GNU stow: https://www.gnu.org/software/stow/

- [ ] **Step 4: 2 verbetes pro Dicionário**

```markdown
### Stow
GNU stow — gerenciador de symlinks declarativos pra dotfiles. Estrutura: 1 pasta por "package" no repo; `stow <pkg>` cria symlinks no home replicando a estrutura. Comandos: `stow`, `stow -D` (unstow), `stow -R` (restow), `stow --adopt`. Simples, sem state file, mas sem templates/cross-OS automático.

Veja também: [[04 - GNU stow — symlinks declarativos]].

### Symlink
Symbolic link — arquivo no filesystem que aponta pra outro path (file ou dir). Comando: `ln -s <alvo> <link>`. Inspecionar: `ls -la` (mostra `link -> alvo`). Editar via symlink edita o file alvo. Removendo symlink não afeta alvo. Base de funcionamento do stow.

Veja também: [[04 - GNU stow — symlinks declarativos]].
```

Ordem alfabética no bloco. Atualmente: Dotfile, WSL, XDG. Adicionar Stow e Symlink (ambos S). Ordem final: Dotfile → Stow → Symlink → WSL → XDG.

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/04 - GNU stow — symlinks declarativos.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/04 - GNU stow — symlinks declarativos.md"
grep -E "^### (Stow|Symlink)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/04 - GNU stow — symlinks declarativos.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 04 — GNU stow"
```

---

## Task 7: Nota 05 — chezmoi: manager completo com templates

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/05 - chezmoi — manager completo com templates.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: chezmoi, Template (dotfiles))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://www.chezmoi.io/
WebFetch: https://www.chezmoi.io/quick-start/
WebFetch: https://www.chezmoi.io/reference/templates/
```

Confirmar: sintaxe atual de templates, variáveis disponíveis, comandos principais.

- [ ] **Step 2: Frontmatter**

```yaml
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
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"chezmoi é manager de dotfiles em Go com state machine declarativo. Source em `~/.local/share/chezmoi/`; `chezmoi apply` aplica diff entre source e target. Features: templates (Go syntax: `{{ .chezmoi.os }}`, `{{ .email }}`), encrypted files nativos (age/gpg), scripts (`run_once_`, `run_onchange_`), data customizada. Workflow: `chezmoi edit`, `chezmoi diff`, `chezmoi apply`. Cross-OS automático; mais features que stow ao custo de curva de aprendizado."

**O que é / Como funciona** (H3s):

### Conceito básico
- chezmoi = "casa minha" em francês (mantenedor twpayne é fã da linguagem)
- State machine: source dir tem "template do que deveria estar"; `chezmoi apply` aplica diff
- Diferente de stow (symlinks): chezmoi COPIA files renderizados (templates resolvidos) pro target
- Trade-off: editar no home não vai automaticamente pro repo; precisa `chezmoi add` ou `chezmoi edit`

### Source directory
- Default: `~/.local/share/chezmoi/`
- Versionado como repo git
- Naming convention pra files:
  - `dot_zshrc` no source → `~/.zshrc` no target
  - `dot_config/nvim/init.lua` → `~/.config/nvim/init.lua`
  - `private_dot_ssh/config` → `~/.ssh/config` (com permissões private)
  - `executable_dot_local/bin/script` → `~/.local/bin/script` (chmod +x)
  - `<name>.tmpl` → template (renderizado em apply)
  - `encrypted_<name>` → arquivo encrypted

### Comandos essenciais
```bash
# Inicializar (vazio ou clone de repo existente)
chezmoi init                                    # vazio
chezmoi init https://github.com/alice/dotfiles  # clone + apply automático

# Adicionar file existente do home
chezmoi add ~/.zshrc                            # copia ~/.zshrc → source como dot_zshrc

# Adicionar como template
chezmoi add --template ~/.gitconfig             # source vira dot_gitconfig.tmpl

# Editar source
chezmoi edit ~/.zshrc                           # abre source no editor

# Ver diff entre source (renderizado) e target
chezmoi diff

# Aplicar (target ← source)
chezmoi apply

# Pull do remoto + apply
chezmoi update

# cd na source
chezmoi cd                                       # exit pra voltar

# Ver dados disponíveis em templates
chezmoi data
```

### Templates (Go syntax)
Variáveis builtin (`chezmoi.*`):
- `{{ .chezmoi.os }}` — `"linux"`, `"darwin"`, `"windows"`
- `{{ .chezmoi.arch }}` — `"amd64"`, `"arm64"`
- `{{ .chezmoi.hostname }}`
- `{{ .chezmoi.username }}`
- `{{ .chezmoi.osRelease.id }}` — `"ubuntu"`, `"fedora"`, `"arch"` (Linux)

Custom data em `~/.config/chezmoi/chezmoi.toml`:
```toml
[data]
email = "alice@example.com"
work_email = "alice@bigcorp.com"
```

Uso em template (`dot_gitconfig.tmpl`):
```gitconfig
[user]
  name = Alice
{{- if eq .chezmoi.hostname "work-laptop" }}
  email = {{ .work_email }}
{{- else }}
  email = {{ .email }}
{{- end }}
```

Sintaxe Go template completa: https://pkg.go.dev/text/template

### Encrypted files (age)
```bash
# Configurar age key no chezmoi
chezmoi --use-builtin-age=true ...   # ou configurar em chezmoi.toml

# Add file encrypted
chezmoi add --encrypt ~/.config/myapp/secret.toml
# Source: encrypted_dot_config/myapp/secret.toml.age (ciphertext no repo; OK pra push público)
```

### Scripts
- `run_once_install-deps.sh` — roda 1x (state machine lembra que já rodou)
- `run_onchange_install-pkgs.sh` — roda quando o script muda (hash do content)
- Útil pra: `brew install`, `apt install`, setup de zsh plugins, etc.

```bash
#!/usr/bin/env bash
# run_once_install-deps.sh
set -euo pipefail
brew install bat eza ripgrep
```

### Comparativo com stow
| Aspecto | stow | chezmoi |
|---|---|---|
| Mecanismo | symlinks | cópia (com state) |
| Templates | não | sim (Go) |
| Cross-OS automático | manual (pastas) | sim (template) |
| Secrets | externa (git-crypt) | nativo (age/gpg) |
| Scripts integrados | não | sim (run_once_) |
| Curva | rasa | média |
| State file | não | sim (boltdb) |
| Edit home → source | automático (symlink) | manual (`chezmoi add/edit`) |

**Na prática** (H3s):

### Setup inicial em máquina nova
```bash
# Instalar
sh -c "$(curl -fsLS get.chezmoi.io)"   # comando oficial do site

# Inicializar com repo existente
chezmoi init --apply https://github.com/alice/dotfiles
```

### Workflow editar + sync
```bash
chezmoi edit ~/.zshrc        # abre source no editor
chezmoi diff                  # preview
chezmoi apply                 # target ← source
chezmoi cd                    # cd na source
git add . && git commit -m "tweak prompt"
git push
exit                          # volta pro cwd anterior
```

### Template cross-OS exemplo
`dot_zshrc.tmpl`:
```zsh
# Comum
export EDITOR=nvim

{{ if eq .chezmoi.os "darwin" -}}
# macOS-specific
export PATH="/opt/homebrew/bin:$PATH"
alias ls='gls --color=auto'
{{- else if eq .chezmoi.os "linux" -}}
# Linux-specific
alias ls='ls --color=auto'
{{- end }}
```

### Re-aplicar parcial
```bash
chezmoi apply ~/.zshrc        # só esse target
```

**Armadilhas (≥5, 4 labels):**

1. **Editar `~/.zshrc` (target) e perder na próxima apply**
   - **Causa:** edit direto no target não vai pro source; apply sobrescreve.
   - **Sintoma:** mudança desaparece após `chezmoi apply` ou `chezmoi update`.
   - **Como detectar:** `chezmoi diff` mostra divergência target → source.
   - **Solução:** sempre `chezmoi edit ~/.zshrc` em vez de editar target direto. Ou `chezmoi re-add ~/.zshrc` pra sincronizar (source ← target).

2. **Template com `{{ ... }}` literal num file não-template**
   - **Causa:** copy-paste de template em file não-`.tmpl`.
   - **Sintoma:** apply copia literal `{{ ... }}` pro target.
   - **Como detectar:** ver target após apply.
   - **Solução:** renomear file pra `<name>.tmpl` (com extensão `.tmpl`).

3. **Confundir `.chezmoi.toml` (data) vs `chezmoi.toml` (state) em path errado**
   - **Causa:** chezmoi tem 2 configs: `~/.config/chezmoi/chezmoi.toml` (config tool) + `.chezmoi.toml.tmpl` no source (data inicial).
   - **Sintoma:** config não aplica.
   - **Como detectar:** `chezmoi data` mostra valores; ausentes = config errada.
   - **Solução:** consultar https://www.chezmoi.io/reference/configuration-file/.

4. **`run_once_` script com bug não re-roda**
   - **Causa:** state machine lembra que rodou (com sucesso ou falha?).
   - **Sintoma:** script falhou; corrigi; não re-roda.
   - **Como detectar:** `chezmoi state get-bucket --bucket=scriptState`.
   - **Solução:** `chezmoi state delete-bucket --bucket=scriptState` pra resetar; ou renomear pra `run_onchange_` (re-roda quando muda).

5. **Encrypted file commitado antes de `--encrypt`**
   - **Causa:** `chezmoi add` sem `--encrypt`, depois adicionou flag.
   - **Sintoma:** plaintext já está no git history.
   - **Como detectar:** `git log --all -p -- path/to/file`.
   - **Solução:** `git filter-repo` ou BFG pra purgar; rotacionar o secret (assumir vazado).

**Em inglês (8-10 bullets bilíngues):**
Termos: source, target, template, render, state machine, idempotent, encrypted, hook, init, apply.

**Veja também:**
- `[[01 - Princípios — o que são dotfiles e por que versionar]]` — pré-req
- `[[03 - Cross-OS — Linux vs macOS vs WSL]]` — templates resolvem cross-OS
- `[[04 - GNU stow — symlinks declarativos]]` — alternativa mais simples
- `[[06 - Bare git repo — abordagem minimalista]]` — alternativa minimalista
- `[[07 - Secrets em dotfiles — git-crypt, age, sops]]` — encryption nativa do chezmoi
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#chezmoi|chezmoi]]`, `[[Dicionário do Terminal#Template (dotfiles)|template]]`

**Referências:**
- chezmoi docs: https://www.chezmoi.io/
- chezmoi quick start: https://www.chezmoi.io/quick-start/
- Go template syntax: https://pkg.go.dev/text/template

- [ ] **Step 4: 2 verbetes pro Dicionário**

```markdown
### chezmoi
Manager de dotfiles em Go com state machine declarativo. Source em `~/.local/share/chezmoi/`; `chezmoi apply` aplica diff. Features: templates (Go), encryption nativa (age/gpg), scripts (`run_once_`), cross-OS automático. Workflow: `chezmoi edit`, `chezmoi diff`, `chezmoi apply`, `chezmoi update`.

Veja também: [[05 - chezmoi — manager completo com templates]].

### Template (dotfiles)
Arquivo com placeholders renderizados em apply-time. chezmoi usa Go template syntax — `{{ .chezmoi.os }}`, `{{ .email }}`, `{{ if ... }}`. Permite single source funcionar cross-OS (`if eq .chezmoi.os "darwin"`) ou por hostname/user.

Veja também: [[05 - chezmoi — manager completo com templates]].
```

Ordem alfabética: chezmoi (c) e Template (T) entram no bloco. Atual: Dotfile, Stow, Symlink, WSL, XDG. Final: chezmoi → Dotfile → Stow → Symlink → Template → WSL → XDG.

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/05 - chezmoi — manager completo com templates.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/05 - chezmoi — manager completo com templates.md"
grep -E "^### (chezmoi|Template \(dotfiles\))$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/05 - chezmoi — manager completo com templates.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 05 — chezmoi"
```

---

## Task 8: Nota 06 — Bare git repo: abordagem minimalista

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/06 - Bare git repo — abordagem minimalista.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: Bare repo (dotfiles), Whitelist (.gitignore))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://www.atlassian.com/git/tutorials/dotfiles
WebFetch: https://news.ycombinator.com/item?id=11070797
```

Capturar: comando exato, alias canônico, conflitos de checkout.

- [ ] **Step 2: Frontmatter**

```yaml
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
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Bare git repo = abordagem minimalista — só git, zero ferramentas extras. `git init --bare $HOME/.dotfiles` cria repo separado do working tree; `--work-tree=$HOME` faz tracking direto no home. Alias `dotfiles` no shell substitui `git`. `.gitignore` é whitelist (`*` + `!arquivo` específico). Vantagens: nada pra instalar, máxima portabilidade. Desvantagens: sem templates, sem secrets, sem cross-OS automático."

**O que é / Como funciona** (H3s):

### Conceito básico
- "Bare" git repo = repo SEM working tree (só metadata em `.git/`)
- Tradicionalmente: bare repo é o que está em servidores (`git clone --bare`)
- Truque: bare repo localmente em `$HOME/.dotfiles/`, com working tree forçado pra `$HOME`
- Resultado: git rastreia files em `$HOME` direto, sem `.git/` no home

### Setup canônico
```bash
# 1. Criar bare repo
git init --bare "$HOME/.dotfiles"

# 2. Alias no shell (zsh/bash)
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

# 3. Configurar pra não mostrar arquivos não-tracked
dotfiles config --local status.showUntrackedFiles no
```

### Workflow básico
```bash
# Adicionar files
dotfiles add ~/.zshrc
dotfiles add ~/.gitconfig
dotfiles commit -m "initial commit"

# Connect a remote
dotfiles remote add origin git@github.com:alice/dotfiles.git
dotfiles push -u origin main
```

### `.gitignore` whitelist
Problema: `git status` no `$HOME` lista MILHARES de files (downloads, cache, etc.).

Solução: `.gitignore` em `$HOME` configurado como whitelist:

```gitignore
# Ignora tudo
*

# Libera específicos com !
!.zshrc
!.zshenv
!.gitconfig
!.config/
!.config/nvim/
!.config/nvim/init.lua
!.config/nvim/lua/
!.config/nvim/lua/**
!.local/
!.local/bin/
!.local/bin/myscript

# Pastas precisam estar listadas em ordem (parents primeiro)
```

(Combinado com `status.showUntrackedFiles no`, esconde o noise.)

### Nova máquina — checkout
```bash
# 1. Clone bare
git clone --bare git@github.com:alice/dotfiles.git "$HOME/.dotfiles"

# 2. Alias
alias dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'

# 3. Checkout (pode falhar se ~/.zshrc já existe e diverge)
dotfiles checkout
```

Se falhar com "would be overwritten":
```bash
# Opção 1: backup e force
mkdir -p ~/.dotfiles-backup
dotfiles checkout 2>&1 | grep -E "^\s+\." | xargs -I{} mv {} ~/.dotfiles-backup/
dotfiles checkout

# Opção 2: aceitar overwrite
dotfiles checkout -f
```

### Limitações
- **Sem templates** — não pode resolver `{{ .email }}` ou similar
- **Sem secrets nativos** — encryption fica externa (git-crypt em files do repo)
- **Sem cross-OS automático** — branches ou conditional shell
- **Setup inicial fricção** — whitelist explícita exige paciência
- **Conflitos no checkout** — files já no home precisam ser tratados manualmente
- **`status.showUntrackedFiles no`** pode esconder files novos que deveriam ser versionados

**Na prática** (H3s):

### Setup completo passo-a-passo
```bash
# 1. Bare repo
git init --bare "$HOME/.dotfiles"

# 2. Alias permanente (adicionar ao ~/.zshrc ou ~/.bashrc)
echo "alias dotfiles='git --git-dir=\$HOME/.dotfiles --work-tree=\$HOME'" >> ~/.zshrc
source ~/.zshrc

# 3. Config
dotfiles config --local status.showUntrackedFiles no

# 4. Primeiro file
dotfiles add ~/.zshrc
dotfiles commit -m "feat: add zshrc"

# 5. Whitelist .gitignore
cat > ~/.gitignore <<'EOF'
*
!.gitignore
!.zshrc
!.gitconfig
!.config/
EOF

dotfiles add ~/.gitignore
dotfiles commit -m "feat: gitignore whitelist"
```

### Adicionar pasta inteira (com whitelist)
```bash
# Liberar pasta nvim no whitelist
cat >> ~/.gitignore <<'EOF'
!.config/nvim/
!.config/nvim/**
EOF

dotfiles add ~/.config/nvim/
dotfiles commit -m "feat: add nvim config"
```

### Workflow diário
```bash
# Status
dotfiles status

# Diff
dotfiles diff

# Commit + push
dotfiles add ~/.zshrc
dotfiles commit -m "tweak prompt"
dotfiles push

# Pull em outra máquina
dotfiles pull
```

**Armadilhas (≥5, 4 labels):**

1. **Cd no `$HOME` e rodar `git status` (sem alias) lista milhares**
   - **Causa:** o `.gitignore` é só pra `dotfiles` alias, não pro git "normal".
   - **Sintoma:** `git status` no home mostra noise enorme.
   - **Como detectar:** rodar.
   - **Solução:** não há "git normal" no home — só usar via alias `dotfiles`.

2. **`dotfiles status` esconde arquivos novos que deveriam ser versionados**
   - **Causa:** `status.showUntrackedFiles no` esconde untracked.
   - **Sintoma:** esquece de adicionar files novos.
   - **Como detectar:** `dotfiles config status.showUntrackedFiles` mostra valor; temporariamente trocar pra `normal` (`dotfiles -c status.showUntrackedFiles=normal status`).
   - **Solução:** hábito de `dotfiles ls-files | xargs ls -la` periódico pra confirmar.

3. **Checkout em máquina com file pre-existente falha**
   - **Causa:** git rejeita overwrite por segurança.
   - **Sintoma:** "would be overwritten by checkout".
   - **Como detectar:** mensagem clara.
   - **Solução:** backup files pre-existentes antes; ou `checkout -f` se sabe que pode descartar.

4. **Whitelist `.gitignore` ordem importa**
   - **Causa:** `!arquivo` dentro de pasta ignorada só funciona se pasta foi liberada antes.
   - **Sintoma:** liberou `!.config/nvim/init.lua` mas `.config/` está ignorado.
   - **Como detectar:** `dotfiles check-ignore -v <path>` mostra qual regra matou.
   - **Solução:** sempre liberar parents primeiro (`!.config/`, depois `!.config/nvim/`, depois `!.config/nvim/init.lua`).

5. **Bare repo dir (`$HOME/.dotfiles/`) commitado por engano em outro repo**
   - **Causa:** se você tem outro repo cobrindo $HOME (ex: chezmoi target).
   - **Sintoma:** repo "B" tenta versionar `~/.dotfiles/`.
   - **Como detectar:** `git status` em B mostra `~/.dotfiles/`.
   - **Solução:** adicionar `.dotfiles/` no `.gitignore` do repo B.

**Em inglês (8-10 bullets bilíngues):**
Termos: bare, working tree, alias, whitelist, checkout, force, untracked, native, minimalist, portability.

**Veja também:**
- `[[01 - Princípios — o que são dotfiles e por que versionar]]` — pré-req
- `[[04 - GNU stow — symlinks declarativos]]` — alternativa
- `[[05 - chezmoi — manager completo com templates]]` — alternativa completa
- `[[08 - Bootstrap — máquina nova zero-to-ready]]` — bootstrap com bare repo
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Bare repo (dotfiles)|bare repo]]`, `[[Dicionário do Terminal#Whitelist (.gitignore)|whitelist]]`

**Referências:**
- Atlassian — Dotfiles tutorial: https://www.atlassian.com/git/tutorials/dotfiles
- HN thread original: https://news.ycombinator.com/item?id=11070797

- [ ] **Step 4: 2 verbetes pro Dicionário**

```markdown
### Bare repo (dotfiles)
Abordagem minimalista de versionar dotfiles usando só git: `git init --bare $HOME/.dotfiles` cria repo separado; `--work-tree=$HOME` rastreia files no home. Alias `dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'` no shell. Vantagens: zero ferramentas extras; portabilidade total. Desvantagens: sem templates, sem secrets, sem cross-OS automático.

Veja também: [[06 - Bare git repo — abordagem minimalista]].

### Whitelist (.gitignore)
Padrão de `.gitignore` que ignora tudo (`*`) e libera só o explícito (`!arquivo`). Útil em bare repo dotfiles onde o working tree é `$HOME` (com milhares de files que NÃO devem ser tracked). Ordem importa: liberar parent dirs antes de children.

Veja também: [[06 - Bare git repo — abordagem minimalista]].
```

Ordem alfabética: Bare repo (B) entra antes de tudo no bloco. Whitelist (W) entra antes de WSL (W-S < W-h... wait: Whitelist W-h-i vs WSL W-S-L. comparando: pos 2 h vs S. Case-insensitive: 'h' < 's', então Whitelist < WSL).

Ordem final do bloco: Bare repo (dotfiles) → chezmoi → Dotfile → Stow → Symlink → Template (dotfiles) → Whitelist (.gitignore) → WSL → XDG Base Directory.

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/06 - Bare git repo — abordagem minimalista.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/06 - Bare git repo — abordagem minimalista.md"
grep -E "^### (Bare repo \(dotfiles\)|Whitelist \(\.gitignore\))$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/06 - Bare git repo — abordagem minimalista.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 06 — Bare git repo"
```

---

## ✅ Checkpoint Adepto

Após Task 8, 3 notas Adepto entregues. Total: 6 notas + MOC.

---

## Task 9: Nota 07 — Secrets em dotfiles: git-crypt, age, sops

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/07 - Secrets em dotfiles — git-crypt, age, sops.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: git-crypt, age, sops, Secret (dotfiles))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/AGWA/git-crypt
WebFetch: https://github.com/FiloSottile/age
WebFetch: https://github.com/getsops/sops
```

Confirmar: comandos, sintaxe, opções de backend.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Secrets em dotfiles — git-crypt, age, sops"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - dotfiles
  - magus
  - secrets
  - encryption
aliases:
  - Secrets dotfiles
  - git-crypt
  - age
  - sops
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"3 abordagens canônicas pra secrets em dotfiles: git-crypt (encryption transparente em git, GPG-based, marca files em `.gitattributes`), age (encryption moderna ssh-key based, simples), sops (Mozilla, YAML/JSON aware com partial encryption, suporta age/GPG/KMS). Cada um vence em contexto diferente. **Regra crítica:** commitar plaintext UMA vez = vazou pro history; tem que rotacionar o secret."

**O que é / Como funciona** (H3s):

### O problema
- Dotfiles tipicamente têm secrets:
  - `~/.aws/credentials` — keys AWS
  - `~/.gnupg/` — GPG private keys
  - `~/.ssh/id_*` — SSH private keys
  - `~/.netrc` — credentials FTP/HTTP
  - `~/.config/<app>/secret.toml` — API tokens custom
- Commitar plaintext = expor (mesmo em repo privado: leak de empresa, contractor, etc.)
- Solução: encryption antes de commit

### Opção 1: git-crypt
- Mecanismo: filter de git (clean/smudge) que encripta files marcados em `.gitattributes`
- Backend: GPG keys (público + privado)
- Workflow:
  ```bash
  # Setup no repo
  cd ~/dotfiles
  git-crypt init                           # gera key local
  git-crypt add-gpg-user alice@example.com # autoriza GPG key

  # Marcar arquivos pra encriptar
  cat >> .gitattributes <<'EOF'
  secrets/* filter=git-crypt diff=git-crypt
  *.key filter=git-crypt diff=git-crypt
  EOF

  # Adicionar secret
  echo "API_KEY=xyz" > secrets/api.env
  git add secrets/api.env
  git commit -m "add secret (encrypted)"
  ```

- Em nova máquina:
  ```bash
  git clone <repo>
  git-crypt unlock      # usa GPG key local pra decriptar
  ```

- Pro: integra com workflow git normal (transparente após unlock)
- Con: GPG é complicado pra muitos; key management
- Repo: https://github.com/AGWA/git-crypt

### Opção 2: age
- Mecanismo: tool standalone moderna (2019+) por Filippo Valsorda
- Backend: ssh-key based (`-i ~/.ssh/id_ed25519`) ou X25519 keys próprias
- Workflow:
  ```bash
  # Gerar key (X25519)
  age-keygen -o ~/.age/key.txt
  # Pub: chave pública (compartilhável)
  # Priv: chave privada (NUNCA compartilhar)

  # Encrypt arquivo
  age -e -r "age1abc..." -o secret.enc secret.txt
  # Ou com ssh key
  age -e -R ~/.ssh/id_ed25519.pub -o secret.enc secret.txt

  # Decrypt
  age -d -i ~/.age/key.txt secret.enc > secret.txt
  ```

- Pro: simples, fast, ssh-key based (já tem)
- Con: não integra automaticamente com git — encryption manual (ou via chezmoi templates)
- Repo: https://github.com/FiloSottile/age

### Opção 3: sops (Mozilla)
- Mecanismo: Secrets OPerationS — YAML/JSON aware, encrypta valores (não chaves) preservando estrutura
- Backends: age, GPG, AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault
- Workflow:
  ```bash
  # Setup
  cat > .sops.yaml <<'EOF'
  creation_rules:
    - path_regex: '^secrets/.*\.yaml$'
      age: 'age1abc...'
  EOF

  # Encrypt
  sops -e -i secrets/config.yaml    # in-place

  # Resultado: file com chaves preservadas, valores encrypted
  # database:
  #   password: ENC[AES256_GCM,data:abc...,iv:def...]
  # api_key: ENC[...]

  # Decrypt em uso
  sops -d secrets/config.yaml | yq '.database.password'
  ```

- Pro: estrutura preservada (yaml/json), partial encryption, multi-backend cloud
- Con: mais complexo setup, dependência adicional (sops + yq/jq)
- Repo: https://github.com/getsops/sops

### Comparativo

| Critério | git-crypt | age | sops |
|---|---|---|---|
| Setup | médio (GPG) | simples | médio |
| File completo vs partial | completo | completo | partial (yaml/json) |
| Integração git | nativa | manual | manual (ou pre-commit hook) |
| Backend | GPG | ssh/X25519 | age/GPG/KMS/Vault |
| Cloud KMS | não | não | sim |
| Curva | alta (GPG) | baixa | média |
| Quando vence | time já usa GPG | dev solo, key-based | secrets estruturados, equipe DevOps |

### Integração com chezmoi
chezmoi tem encryption nativa (escolhe age ou gpg):
```toml
# ~/.config/chezmoi/chezmoi.toml
encryption = "age"
[age]
identity = "~/.age/key.txt"
recipient = "age1abc..."
```

```bash
chezmoi add --encrypt ~/.ssh/secret.txt
# Source: encrypted_dot_ssh/secret.txt.age (ciphertext)
```

### Integração com stow
Stow não tem encryption nativo. Opções:
- git-crypt no repo do stow
- Pasta `secrets-encrypted/` com files cifrados manualmente; `stow secrets-encrypted` cria symlinks, decryption fora do stow

### Integração com bare repo
- git-crypt funciona idêntico (filter de git é universal)
- age/sops manual antes de commit

### Pre-commit hook pra bloquear plaintext acidental
```bash
# .git/hooks/pre-commit
# Ou via pre-commit framework (galho 4 nota 06)
if git diff --cached | grep -iE "(api[_-]?key|password|token|secret).*=.*[a-z0-9]{16}"; then
  echo "ERRO: possível secret em plaintext"
  exit 1
fi
```

**Na prática** (H3s):

### Setup git-crypt do zero
```bash
# 1. Instalar
brew install git-crypt        # macOS
sudo apt install git-crypt    # Ubuntu

# 2. Gerar GPG key (se não tiver)
gpg --full-generate-key       # tipo RSA, 4096 bits

# 3. No repo dotfiles
cd ~/dotfiles
git-crypt init
git-crypt add-gpg-user $(gpg --list-keys --keyid-format LONG | grep alice@example.com | awk '{print $2}' | cut -d/ -f2)

# 4. .gitattributes
cat >> .gitattributes <<'EOF'
.env filter=git-crypt diff=git-crypt
secrets/** filter=git-crypt diff=git-crypt
EOF

# 5. Commitar key chain
git add .gitattributes
git commit -m "chore: setup git-crypt"
```

### Workflow age standalone
```bash
# Gerar key
mkdir -p ~/.age && age-keygen -o ~/.age/key.txt

# Encrypt
RECIPIENT=$(grep "^# public key:" ~/.age/key.txt | awk '{print $4}')
age -e -r "$RECIPIENT" -o ~/dotfiles/secrets/api.env.age ~/secrets/api.env

# Decrypt (em uso)
age -d -i ~/.age/key.txt ~/dotfiles/secrets/api.env.age > /tmp/api.env
source /tmp/api.env
rm /tmp/api.env
```

### Setup sops com age
```bash
# Gerar age key (se não tem)
age-keygen -o ~/.config/sops/age/keys.txt
export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt

# Config
cat > ~/dotfiles/.sops.yaml <<EOF
creation_rules:
  - path_regex: '\.sops\.yaml$|^secrets/.*'
    age: '$(grep "^# public key:" ~/.config/sops/age/keys.txt | awk "{print \$4}")'
EOF

# Encrypt
sops -e -i ~/dotfiles/secrets/config.yaml
```

**Armadilhas (≥5, 4 labels):**

1. **Commitar plaintext UMA vez = vazou pro history**
   - **Causa:** esqueceu setup git-crypt; arquivo foi pro repo plaintext.
   - **Sintoma:** `git log -p -- secrets/api.env` mostra plaintext.
   - **Como detectar:** auditar history; ou usar `gitleaks` / `trufflehog`.
   - **Solução:** **rotacionar o secret IMEDIATAMENTE** (assumir vazado). Depois `git filter-repo --invert-paths --path secrets/api.env` ou BFG; force-push (com aviso a colaboradores).

2. **git-crypt key path perdida = repo permanently locked**
   - **Causa:** perdeu GPG private key e não tem outra.
   - **Sintoma:** clone novo + `git-crypt unlock` falha.
   - **Como detectar:** ao tentar unlock.
   - **Solução:** sem key, sem decrypt — pra prevenir, backup do GPG key (em hardware key tipo YubiKey, ou impressão paperkey). Add múltiplos GPG users no `git-crypt add-gpg-user`.

3. **age key.txt commitado por engano**
   - **Causa:** key gerada em pasta no repo + add inadvertente.
   - **Sintoma:** private key no git history.
   - **Como detectar:** `git log --all -- '*.age'` ou similar.
   - **Solução:** revogar/regenerar key; todos os files encriptados com ela ficam comprometidos.

4. **sops decryption sem `SOPS_AGE_KEY_FILE` env**
   - **Causa:** age key file não setada via env.
   - **Sintoma:** sops -d falha "no age recipients available".
   - **Como detectar:** ler erro.
   - **Solução:** `export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt` no shell rc.

5. **Encryption em chezmoi sem `encryption =` config**
   - **Causa:** `chezmoi add --encrypt` sem encryption configurada em `chezmoi.toml`.
   - **Sintoma:** erro "no encryption method configured".
   - **Como detectar:** `chezmoi data | grep encryption`.
   - **Solução:** configurar `encryption = "age"` (ou `"gpg"`) + chave em `chezmoi.toml` antes.

**Em inglês (8-10 bullets bilíngues):**
Termos: encryption, decrypt, key, public key, private key, ciphertext, plaintext, transparent, backend, rotate.

**Veja também:**
- `[[05 - chezmoi — manager completo com templates]]` — encryption nativa
- `[[06 - Bare git repo — abordagem minimalista]]` — git-crypt funciona aqui também
- `[[08 - Bootstrap — máquina nova zero-to-ready]]` — bootstrap precisa cuidar de keys
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#git-crypt|git-crypt]]`, `[[Dicionário do Terminal#age|age]]`, `[[Dicionário do Terminal#sops|sops]]`, `[[Dicionário do Terminal#Secret (dotfiles)|secret]]`

**Referências:**
- git-crypt: https://github.com/AGWA/git-crypt
- age: https://github.com/FiloSottile/age
- sops: https://github.com/getsops/sops

- [ ] **Step 4: 4 verbetes pro Dicionário**

```markdown
### age
Ferramenta de encryption moderna (2019+) por Filippo Valsorda. Alternativa simples ao GPG, com ssh-key based (`-R ~/.ssh/id_ed25519.pub`) ou X25519 keys próprias. Comando: `age -e -r <recipient> -o out.age in.txt`. Decrypt: `age -d -i ~/.age/key.txt out.age`.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### git-crypt
Ferramenta que encripta transparentemente files no git, marcados em `.gitattributes` (`file filter=git-crypt diff=git-crypt`). GPG-based. Comandos: `git-crypt init`, `git-crypt add-gpg-user`, `git-crypt unlock`. Integra com workflow git normal — files plaintext localmente, ciphertext no repo.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### Secret (dotfiles)
Credencial ou informação sensível em arquivos de config: API tokens, SSH/GPG private keys, OAuth refresh tokens, DB credentials. Versionar plaintext = vazar. Soluções: encryption (git-crypt, age, sops), ou exclude do repo (`.gitignore`) + setup manual em cada máquina.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### sops
Secrets OPerationS (Mozilla, hoje CNCF) — encryption YAML/JSON-aware. Encripta VALORES preservando estrutura (chaves visíveis); permite multi-backend (age, GPG, AWS/GCP/Azure KMS, Vault). Comando: `sops -e -i file.yaml`. Config via `.sops.yaml` no repo.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].
```

Ordem alfabética: age (a), git-crypt (g), Secret (S), sops (s). Insertion:
- age — primeiro do bloco (a < B)
- git-crypt — após chezmoi, antes de Dotfile (g > c, g < d? não: g > d. então g vai depois de Dotfile). Wait: gerar ordem: a, B(are repo), c(hezmoi), D(otfile), g(it-crypt), S(ecret), s(tow), s(ymlink), s(ops)... Stow vs sops vs Symlink: pos 1 todos S. pos 2: t (Stow), o (sops), y (Symlink). Ordem: o < t < y, então sops < Stow < Symlink.

Ordem final esperada: age → Bare repo → chezmoi → Dotfile → git-crypt → Secret (dotfiles) → sops → Stow → Symlink → Template → Whitelist → WSL → XDG.

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/07 - Secrets em dotfiles — git-crypt, age, sops.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/07 - Secrets em dotfiles — git-crypt, age, sops.md"
grep -E "^### (age|git-crypt|Secret \(dotfiles\)|sops)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/07 - Secrets em dotfiles — git-crypt, age, sops.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 07 — Secrets (git-crypt, age, sops)"
```

---

## Task 10: Nota 08 — Bootstrap: máquina nova zero-to-ready

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/08 - Bootstrap — máquina nova zero-to-ready.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: Bootstrap, Idempotente, Provisioning)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/Homebrew/homebrew-bundle
WebFetch: https://www.passwordstore.org/ (passing reference)
```

Capturar: Brewfile syntax, padrões de script idempotente.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Bootstrap — máquina nova zero-to-ready"
created: 2026-05-22
updated: 2026-05-22
type: concept
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
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Bootstrap = script único que leva máquina nova de zero até dev-ready em 1 comando. Etapas típicas: detectar OS, instalar package manager (homebrew em macOS), instalar deps (Brewfile/apt), clonar dotfiles, aplicar (stow/chezmoi/bare). Propriedades essenciais: idempotente (rodar 2x não quebra), modular (skip etapa já completa), logged (`set -x`), falha rápida (`set -euo pipefail`). Alternativas pra orchestration: Ansible (overkill solo), justfile, Makefile."

**O que é / Como funciona** (H3s):

### O problema
- Máquina nova: laptop trocado, VM nova, container dev, server provisionado
- Setup manual: 1-3 horas (install brew, install N apps, copy dotfiles, configurar shell, ssh keys, etc.)
- Bootstrap automatiza: 1 comando, 5-20 min

### Etapas canônicas
1. **Detectar OS** — `uname -s`, `/etc/os-release`
2. **Instalar package manager** se faltar (Homebrew em macOS; geralmente Linux já tem apt/dnf/pacman)
3. **Instalar deps** — `brew bundle --file=Brewfile` ou equivalente
4. **Clonar dotfiles**
5. **Aplicar dotfiles** — `stow zsh nvim git` ou `chezmoi init --apply <repo>` ou `dotfiles checkout`
6. **Configs pós-apply** — shell default (`chsh`), git user.email, ssh keys
7. **(Opcional) Restart shell ou reload session**

### Propriedades essenciais

**Idempotente** = rodar N vezes produz mesmo resultado
```bash
# Mau (idempotente NÃO):
brew install bat                    # falha 2a vez "already installed"

# Bom (idempotente):
if ! command -v bat >/dev/null; then
  brew install bat
fi

# Melhor (homebrew lida bem com `install` em already installed):
brew install bat                    # 2026+ Homebrew não-fatal
```

**Modular** = skip etapa completa
```bash
# Bom: cada etapa em função, dispatchável
install_brew() { ... }
install_deps() { ... }
clone_dotfiles() { ... }

# main
install_brew
install_deps
clone_dotfiles
```

**Logged** = trace
```bash
set -x                              # echo cada comando
exec > >(tee -a bootstrap.log)      # tudo vai pro file
exec 2>&1
```

**Falha rápida** = aborta no primeiro erro
```bash
set -euo pipefail
# -e: exit on error
# -u: erro em var não-definida
# -o pipefail: erro em qualquer parte de pipe
```

### Estratégias de orchestration

#### Script shell direto
Pro: simples, sem deps; Con: cresce difícil de manter em ~500+ linhas

#### Brewfile (macOS + Linux brew)
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

cask "ghostty"          # macOS only
cask "raycast"
```

Run: `brew bundle --file=Brewfile`. Idempotente nativo. Deps de Linux: `apt`/`dnf` paralelo.

#### justfile (justice)
```just
# justfile
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

Run: `just bootstrap`. Pro: dependency graph (just bootstrap implica todas as deps na ordem); con: just precisa estar instalado primeiro (`cargo install just` ou similar).

#### Makefile (declarativo simples)
Mesma ideia do justfile, mas com a fricção de Make syntax (tabs).

#### chezmoi `run_once_*.sh` scripts
chezmoi automaticamente roda scripts uma vez na apply — bootstrap fica embutido nos dotfiles.

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

#### Ansible
Overkill pra single-machine; bom pra fleet (≥5 máquinas similares). Vale a pena se gerencia fleet de devs/servers.

### Cross-OS bootstrap exemplo end-to-end
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
    brew bundle --file="$HOME/dotfiles/Brewfile" 2>/dev/null || {
      [[ -d "$HOME/dotfiles" ]] || git clone https://github.com/alice/dotfiles "$HOME/dotfiles"
      brew bundle --file="$HOME/dotfiles/Brewfile"
    }
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

**Na prática** (H3s):

### Testar bootstrap em VM/container
```bash
# Docker (rápido pra testar)
docker run --rm -it -v "$(pwd):/dotfiles" ubuntu:22.04 bash
# Dentro do container:
apt update && apt install -y curl git sudo
useradd -m alice -s /bin/bash
su - alice -c "bash /dotfiles/bootstrap.sh"

# Multipass (macOS, VMs Ubuntu lightweight)
multipass launch --name test-bootstrap
multipass exec test-bootstrap -- bash -c "..."
```

### Bootstrap incremental — só missing
```bash
# Função idempotente
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

### Recovery — bootstrap parcial falhou no meio
```bash
# Re-rodar deve continuar de onde parou (porque é idempotente)
bash bootstrap.sh

# Ou rodar etapa específica
just install-deps    # se usa justfile
```

**Armadilhas (≥5, 4 labels):**

1. **Bootstrap destrutivo em máquina já configurada**
   - **Causa:** `rm`, `mv`, `chsh` sem verificação de estado.
   - **Sintoma:** perde shell config existente.
   - **Como detectar:** ler script antes de rodar; sempre testar em VM primeiro.
   - **Solução:** verificações `[[ -d ]]`/`[[ -f ]]` antes de cada destruição; backup com timestamp (`mv ~/.zshrc ~/.zshrc.bak-$(date +%s)`).

2. **`brew install` sem `Brewfile` cresce desorganizado**
   - **Causa:** comandos `brew install X` espalhados no script.
   - **Sintoma:** difícil ver lista de deps; sync entre máquinas inconsistente.
   - **Como detectar:** `brew leaves` lista; comparar entre máquinas.
   - **Solução:** centralizar em `Brewfile` versionado; `brew bundle --file=Brewfile`.

3. **Script falha silenciosa sem `set -e`**
   - **Causa:** sem `set -e`, comando falho continua.
   - **Sintoma:** bootstrap "completou" mas etapas falharam no meio.
   - **Como detectar:** ler logs cuidadosamente.
   - **Solução:** sempre `set -euo pipefail` no topo.

4. **`chsh` sem zsh em `/etc/shells` falha**
   - **Causa:** shell precisa estar listado em `/etc/shells` pra `chsh` permitir.
   - **Sintoma:** "chsh: <shell> is not a valid shell".
   - **Como detectar:** ler erro.
   - **Solução:** `echo $(which zsh) | sudo tee -a /etc/shells` antes de `chsh`.

5. **Bootstrap clona dotfiles e aplica antes de dependências instaladas**
   - **Causa:** ordem das etapas errada.
   - **Sintoma:** stow falha porque dir não existe; ou zshrc source plugins não instalados.
   - **Como detectar:** ler logs.
   - **Solução:** ordem canônica = package manager → deps → clone dotfiles → apply.

**Em inglês (8-10 bullets bilíngues):**
Termos: bootstrap, provisioning, idempotent, modular, recovery, dependency, package manager, fleet, declarative, automation.

**Veja também:**
- `[[04 - GNU stow — symlinks declarativos]]` — pré-req (stow no bootstrap)
- `[[05 - chezmoi — manager completo com templates]]` — alternativa com `run_once_`
- `[[06 - Bare git repo — abordagem minimalista]]` — alternativa
- `[[07 - Secrets em dotfiles — git-crypt, age, sops]]` — bootstrap cuida de keys
- `[[09 - Sync entre máquinas heterogêneas]]` — bootstrap branched por host
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Bootstrap|bootstrap]]`, `[[Dicionário do Terminal#Idempotente|idempotente]]`, `[[Dicionário do Terminal#Provisioning|provisioning]]`

**Referências:**
- Homebrew Bundle: https://github.com/Homebrew/homebrew-bundle
- just (command runner): https://github.com/casey/just

- [ ] **Step 4: 3 verbetes pro Dicionário**

```markdown
### Bootstrap
Script idempotente que provisiona máquina nova zero-to-ready em 1 comando. Etapas típicas: detectar OS, instalar package manager (homebrew em macOS), instalar deps (`brew bundle`/`apt`), clonar dotfiles, aplicar (stow/chezmoi/bare). Sempre com `set -euo pipefail` + verificações de estado.

Veja também: [[08 - Bootstrap — máquina nova zero-to-ready]].

### Idempotente
Propriedade de operação que produz o mesmo resultado se executada N vezes. Em bootstrap: rodar `bash bootstrap.sh` 2x não quebra (pula etapas já completas). Implementação: `if ! command -v ... >/dev/null; then ...`; ou ferramentas com idempotência nativa (`brew bundle`, chezmoi state machine).

Veja também: [[08 - Bootstrap — máquina nova zero-to-ready]].

### Provisioning
Automação de setup inicial de uma máquina (deps, configs, services). Pode ser single-machine (script bash) ou fleet (Ansible, Salt, Puppet). Pra dev individual no terminal, bootstrap em shell + Brewfile resolve sem overhead de Ansible.

Veja também: [[08 - Bootstrap — máquina nova zero-to-ready]].
```

Ordem alfabética: Bootstrap (B), Idempotente (I), Provisioning (P). Insert no bloco:
- Bootstrap entre age (a) e Bare repo (Ba). a < Bare < Bootstrap < c. Then: age → Bare repo → Bootstrap → chezmoi → ...
- Idempotente entre git-crypt (g) e Secret (S). g < I < S. Ordem: → git-crypt → Idempotente → Secret →
- Provisioning entre Idempotente (I) e Secret (S). I < P < S. Ordem: → Idempotente → Provisioning → Secret →

Ordem final completa: age → Bare repo → **Bootstrap** → chezmoi → Dotfile → git-crypt → **Idempotente** → **Provisioning** → Secret → sops → Stow → Symlink → Template → Whitelist → WSL → XDG.

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/08 - Bootstrap — máquina nova zero-to-ready.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/08 - Bootstrap — máquina nova zero-to-ready.md"
grep -E "^### (Bootstrap|Idempotente|Provisioning)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/08 - Bootstrap — máquina nova zero-to-ready.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-dotfiles): add nota 08 — Bootstrap"
```

---

## Task 11: Nota 09 — Sync entre máquinas heterogêneas

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/Dotfiles/09 - Sync entre máquinas heterogêneas.md`
- (Sem verbetes novos.)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://www.chezmoi.io/user-guide/machines/
WebFetch: https://man.openbsd.org/ssh_config.5  (Match patterns)
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Sync entre máquinas heterogêneas"
created: 2026-05-22
updated: 2026-05-22
type: concept
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
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Cenário comum: laptop pessoal + work + servidor cloud, cada um com requisitos diferentes (work tem secrets corp; server não tem GUI). 4 estratégias: (1) branches per-host, (2) conditional includes no shell, (3) chezmoi data por host (`.chezmoi.hostname`), (4) stow com pastas host-specific. Branches pra diferenças grandes/estruturais; condicionais pra diferenças pequenas/dinâmicas. Tradeoff: manutenibilidade (branches) vs flexibilidade (condicionais)."

**O que é / Como funciona** (H3s):

### O cenário
- Múltiplas máquinas, cada uma com setup parcialmente diferente
- Comum:
  - `personal-laptop` (macOS, brew, dev local)
  - `work-laptop` (Linux corporativo, restrições de install, secrets corp)
  - `cloud-server` (Ubuntu headless, sem GUI tools, simpler shell)
  - `dev-vm` (Linux full-feature)
- Cada um com:
  - Email diferente (`git config user.email`)
  - Aliases diferentes (`alias k=kubectl` só no work)
  - Plugins diferentes (TUIs heavy no laptop, minimal no server)
  - Secrets diferentes (AWS keys work vs personal)

### Estratégia 1: Branches per-host
- Master = baseline funcional em qualquer máquina
- Branch `work` = overrides do work
- Branch `server` = subset minimal

Workflow:
```bash
# Setup work
git clone <repo> ~/dotfiles
cd ~/dotfiles
git checkout work
stow zsh git

# Update work com mudanças do master
git checkout work
git merge master
```

**Pro:** clean separation, fácil ver "o que é diferente no work"
**Con:** 2x manutenção (merge regular master → work); divergência cresce com tempo

### Estratégia 2: Conditional includes no shell
```zsh
# ~/.zshrc (mesmo em todas as máquinas)
HOSTNAME_SHORT=$(hostname -s)

# Source host-specific se existir
[[ -f "$HOME/.config/zsh/host-$HOSTNAME_SHORT.zsh" ]] && \
  source "$HOME/.config/zsh/host-$HOSTNAME_SHORT.zsh"

# Source OS-specific
[[ -f "$HOME/.config/zsh/os-$DOTFILES_OS.zsh" ]] && \
  source "$HOME/.config/zsh/os-$DOTFILES_OS.zsh"
```

Files:
- `~/.config/zsh/host-work-laptop.zsh` — só carrega em work
- `~/.config/zsh/host-personal.zsh` — só carrega em personal
- `~/.config/zsh/os-darwin.zsh` — só macOS

**Pro:** single branch, sem merge; fácil adicionar nova máquina
**Con:** arquivos extras "host-XXX" precisam estar versionados (ou em pasta separada local-only)

### Estratégia 3: chezmoi data por host
chezmoi tem `.chezmoi.toml.tmpl` que define data específica por hostname:

```toml
# .chezmoi.toml.tmpl (source)
{{- if eq .chezmoi.hostname "work-laptop" -}}
email = "alice@bigcorp.com"
machine = "work"
{{- else -}}
email = "alice@personal.dev"
machine = "personal"
{{- end -}}
```

Templates usam:
```gitconfig
{{- /* dot_gitconfig.tmpl */ -}}
[user]
  name = Alice
  email = {{ .email }}
```

**Pro:** idiomático em chezmoi, mantém single source
**Con:** só funciona se você usa chezmoi

### Estratégia 4: Stow com pastas host-specific
```
~/dotfiles/
├── zsh-base/.zshrc            # comum
├── zsh-work/.config/zsh/local.zsh  # só work
└── zsh-personal/.config/zsh/local.zsh
```

Bootstrap por host:
```bash
case "$HOSTNAME_SHORT" in
  work-*)
    stow zsh-base zsh-work
    ;;
  *)
    stow zsh-base zsh-personal
    ;;
esac
```

**Pro:** flexibilidade total; explicit
**Con:** manutenção manual; sem mecanismo built-in pra escolha

### Quando branchar vs quando condicionar

| Tipo de diferença | Estratégia recomendada |
|---|---|
| OS diferente (linux vs macOS) | Condicional (env var `OS`) ou chezmoi template |
| Secret só em work | Encryption (nota 07) + condicional load |
| Workflow git diferente (email/signing) | chezmoi data ou conditional gitconfig include |
| Set de aliases muito diferente (k8s only no work) | Host-specific file (estratégia 2) |
| Plugins de shell muito diferentes | Host-specific file ou chezmoi template |
| Hardware muito diferente (server headless vs laptop) | Branch separada (estratégia 1) |

### git config conditional include
git tem suporte nativo:
```gitconfig
# ~/.gitconfig (base)
[user]
  name = Alice

[includeIf "gitdir:~/work/"]
  path = ~/.config/git/work.gitconfig

[includeIf "gitdir:~/personal/"]
  path = ~/.config/git/personal.gitconfig
```

E `work.gitconfig`:
```gitconfig
[user]
  email = alice@bigcorp.com
[commit]
  gpgsign = true
```

Conditional by path, hostname (git 2.13+), branch, etc.

### ssh Match patterns
Mesma ideia em ssh config:
```ssh
# ~/.ssh/config
Host *
  IdentityFile ~/.ssh/id_ed25519

Match host github.com Exec "[ -f ~/.ssh/work-key ]"
  IdentityFile ~/.ssh/work-key
```

(Match Exec é poderoso mas obscure; alternative: aliases `Host work-github` com IdentityFile específica.)

**Na prática** (H3s):

### Setup conditional por host (recomendado pra começar)
```bash
# 1. Estrutura
mkdir -p ~/.config/zsh

# 2. Base zshrc (~/.zshrc)
cat > ~/.zshrc <<'EOF'
HOSTNAME_SHORT=$(hostname -s)
[[ -f "$HOME/.config/zsh/host-$HOSTNAME_SHORT.zsh" ]] && \
  source "$HOME/.config/zsh/host-$HOSTNAME_SHORT.zsh"
EOF

# 3. Host-specific (cada máquina cria o seu)
cat > ~/.config/zsh/host-work-laptop.zsh <<'EOF'
alias k=kubectl
export AWS_PROFILE=work
EOF
```

### chezmoi por hostname
```bash
# Source file: ~/.local/share/chezmoi/.chezmoi.toml.tmpl
cat > ~/.local/share/chezmoi/.chezmoi.toml.tmpl <<'EOF'
{{- if eq .chezmoi.hostname "work-laptop" -}}
[data]
machine = "work"
email = "alice@bigcorp.com"
{{- else -}}
[data]
machine = "personal"
email = "alice@personal.dev"
{{- end -}}
EOF

# Source file: dot_gitconfig.tmpl
cat > ~/.local/share/chezmoi/dot_gitconfig.tmpl <<'EOF'
[user]
  name = Alice
  email = {{ .email }}
EOF
```

### Branches per-host workflow
```bash
# Setup
git clone <repo> ~/dotfiles
cd ~/dotfiles
git checkout -b work        # cria branch local

# Diverge work com mudanças
echo 'export AWS_PROFILE=work' >> zsh/.config/zsh/work-only.zsh
git add . && git commit -m "work: AWS_PROFILE"

# Periodicamente: pull master
git checkout main
git pull
git checkout work
git merge main              # ou rebase

# Push branches
git push origin main work
```

**Armadilhas (≥5, 4 labels):**

1. **Branches divergem demais — work nunca é mergeado**
   - **Causa:** trabalho em master sem fazer merge work; tempo passa.
   - **Sintoma:** merge `main → work` tem conflito grande.
   - **Como detectar:** `git log work..main --oneline` cresce.
   - **Solução:** disciplinar merge regular (1x semana ou em cada feature); ou trocar pra conditional approach (estratégia 2).

2. **`hostname -s` retorna diferente do esperado em macOS vs Linux**
   - **Causa:** macOS retorna nome com `.local` ou `.lan` sufixo às vezes; Linux retorna nome puro.
   - **Sintoma:** `host-work-laptop.zsh` não carrega em macOS porque hostname é `work-laptop.local`.
   - **Como detectar:** `hostname` (compara saídas).
   - **Solução:** `hostname -s` (short) já tira sufixo na maioria; ou `scutil --get LocalHostName` em macOS.

3. **`includeIf "gitdir:~/work/"` não inclui se `gitdir` tem barra final inconsistente**
   - **Causa:** git é exigente com trailing slash.
   - **Sintoma:** config work não aplica em repos `~/work/foo/`.
   - **Como detectar:** `git config --show-origin --get user.email`.
   - **Solução:** sempre incluir trailing slash no path do `gitdir:`.

4. **Files host-specific commitados em vez de gerados localmente**
   - **Causa:** se intenção era `host-XXX.zsh` ficar local-only, mas você comita.
   - **Sintoma:** secrets vazam ou configs work aparecem em personal.
   - **Como detectar:** revisar `git ls-files`.
   - **Solução:** decidir conscientemente — versionar (com encryption se tem secret) ou ignorar (`.gitignore`).

5. **chezmoi hostname template não funciona em containers (hostname genérico)**
   - **Causa:** containers Docker têm hostname tipo `abc123def` random.
   - **Sintoma:** template `if eq .chezmoi.hostname "..."` falha sempre.
   - **Como detectar:** `chezmoi data | grep hostname`.
   - **Solução:** usar outras vars (`chezmoi.username`, env var custom) em vez de hostname; ou setar `--hostname=work` no chezmoi.

**Em inglês (8-10 bullets bilíngues):**
Termos: sync, hostname, conditional, branch, merge, override, fleet, heterogeneous, divergence, single source.

**Veja também:**
- `[[04 - GNU stow — symlinks declarativos]]` — sync via stow + condicionais
- `[[05 - chezmoi — manager completo com templates]]` — sync via chezmoi data
- `[[06 - Bare git repo — abordagem minimalista]]` — sync via branches
- `[[08 - Bootstrap — máquina nova zero-to-ready]]` — bootstrap conhece host
- `[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]`
- `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#chezmoi|chezmoi]]`, `[[Dicionário do Terminal#Template (dotfiles)|template]]`

**Referências:**
- chezmoi machines: https://www.chezmoi.io/user-guide/machines/
- git includeIf: https://git-scm.com/docs/git-config#_conditional_includes
- ssh_config Match: https://man.openbsd.org/ssh_config.5

- [ ] **Step 4: Sem verbetes novos.**

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/09 - Sync entre máquinas heterogêneas.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/Dotfiles/09 - Sync entre máquinas heterogêneas.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/09 - Sync entre máquinas heterogêneas.md"
git commit -m "feat(terminal-dotfiles): add nota 09 — Sync máquinas heterogêneas"
```

---

## ✅ Checkpoint Magus

Após Task 11, todas as 9 notas escritas. Total: 9 notas + MOC.

---

## Task 12: Pass final no MOC do galho

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/Dotfiles/index.md`

- [ ] **Step 1: Substituir placeholders de versão**

`old_string`:
```markdown
- **GNU stow:** `<VERSAO_STOW>` (capturada no pré-flight)
- **chezmoi:** `<VERSAO_CHEZMOI>` (capturada no pré-flight)
- **git:** `<VERSAO_GIT>` (capturada no pré-flight)
- **OS de referência:** `<OS_REF>`
```

`new_string` (substituir pelos valores capturados em Task 0):
```markdown
- **GNU stow:** <VERSAO_REAL_STOW>
- **chezmoi:** <VERSAO_REAL_CHEZMOI>
- **git:** <VERSAO_REAL_GIT>
- **OS de referência:** <OS_REAL>
```

Se ferramenta não instalada, escrever "não instalada localmente (notas pesquisadas em docs oficiais)".

- [ ] **Step 2: Confirmar wikilinks**

```bash
for n in "01 - Princípios — o que são dotfiles e por que versionar" "02 - Anatomia — estrutura típica e XDG Base Directory" "03 - Cross-OS — Linux vs macOS vs WSL" "04 - GNU stow — symlinks declarativos" "05 - chezmoi — manager completo com templates" "06 - Bare git repo — abordagem minimalista" "07 - Secrets em dotfiles — git-crypt, age, sops" "08 - Bootstrap — máquina nova zero-to-ready" "09 - Sync entre máquinas heterogêneas"; do
  test -f "03-Dominios/Tecnologia/Terminal/Dotfiles/${n}.md" && echo "ok: $n" || echo "FALTA: $n"
done
```

Esperado: 9 `ok:`.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dotfiles/index.md"
git commit -m "$(cat <<'EOF'
docs(terminal-dotfiles): pass final no MOC do galho

Substitui placeholders <VERSAO_*> pelas versões reais capturadas no
pré-flight. Confirma que todos os 9 wikilinks de notas estão ativos.
EOF
)"
```

---

## Task 13: Pass final no Dicionário do Terminal

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Listar verbetes do bloco**

```bash
awk '/^## Dotfiles$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Verbetes esperados (16) em ordem alfabética case-insensitive:
1. age
2. Bare repo (dotfiles)
3. Bootstrap
4. chezmoi
5. Dotfile
6. git-crypt
7. Idempotente
8. Provisioning
9. Secret (dotfiles)
10. sops
11. Stow
12. Symlink
13. Template (dotfiles)
14. Whitelist (.gitignore)
15. WSL
16. XDG Base Directory

- [ ] **Step 2: Reordenar se necessário**

Use Edit pra mover blocos fora de ordem.

- [ ] **Step 3: Confirmar "Veja também"**

```bash
awk '/^## Dotfiles$/{f=1; next} /^## /{f=0}
     f && /^### / { v=$0; getline; getline; while(NF==0) getline; if ($0 !~ /^Veja também:/) print v " — sem Veja também" }' \
  "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: vazio.

- [ ] **Step 4: Contagem**

```bash
awk '/^## Dotfiles$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md" | wc -l
```

Esperado: 16.

- [ ] **Step 5: Commit (se houve mudança)**

```bash
git status --short "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Se modificado:
```bash
git add "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "$(cat <<'EOF'
docs(terminal): pass final no Dicionário (bloco Dotfiles)

Garante ordem alfabética case-insensitive no bloco Dotfiles; cada
verbete tem Veja também. Contagem final: 16 verbetes novos.
EOF
)"
```

Sem mudanças = pular.

---

## Task 14: Atualizar tronco — ativar wikilink

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/index.md`

- [ ] **Step 1: Edit tronco**

`old_string`:
```markdown
- Dotfiles — galho 5 (planejado): gerenciamento de configs e sync
```

`new_string`:
```markdown
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|Dotfiles]] — galho 5: princípios, ferramentas (stow/chezmoi/bare), secrets, bootstrap, sync
```

- [ ] **Step 2: `updated:` do tronco**

Edit pra `updated: 2026-05-22`.

- [ ] **Step 3: Confirmar**

```bash
grep -n "Dotfiles" "03-Dominios/Tecnologia/Terminal/index.md"
```

Esperado: wikilink ativo; `(planejado)` desaparece.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/index.md"
git commit -m "$(cat <<'EOF'
feat(terminal): tronco com wikilink ativo pro galho 5 (Dotfiles)

Substitui bullet "Dotfiles (planejado)" por wikilink ativo
[[03-Dominios/Tecnologia/Terminal/Dotfiles/index|Dotfiles]] após entrega do galho 5.
EOF
)"
```

---

## Task 15: Validação final

**Files:**
- (nenhum)

- [ ] **Step 1: verificar-wikilinks**

```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py "03-Dominios/Tecnologia/Terminal/Dotfiles/" --respect-public-only
```

Lê o JSON em `/tmp/wikilinks-report-*.json`. Esperado: `links_broken: 0`.

- [ ] **Step 2: Sanity check**

```bash
ls -1 "03-Dominios/Tecnologia/Terminal/Dotfiles/" | sort
git log --oneline | head -18
git log --format="%H %s" -18 | grep -i "co-authored" || echo "ok: nenhum commit com Co-Authored-By"
```

Esperado:
- 10 arquivos (9 notas + index)
- ~15-18 commits do galho
- Nenhum Co-Authored-By

- [ ] **Step 3: Contagem final do Dicionário**

```bash
awk '/^## Dotfiles$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md" | wc -l
```

Esperado: 16.

- [ ] **Step 4: Cross-task final review (recomendado)**

Dispatch reviewer subagent pro galho inteiro.

- [ ] **Step 5: Declarar galho fechado**

Reporte:
- 9 notas + MOC entregues
- 16 verbetes no Dicionário
- Tronco com wikilink ativo
- Zero wikilinks broken
- Zero commits com Co-Authored-By
- Próximo galho (6 — CLI Utils) quando o usuário quiser

---

## Self-review do plano

**Spec coverage:** todas seções 3.1-3.4, 4.1-4.3, 5 → tasks atribuídas. Critério de pronto seção 8 → Tasks 12-15.

**Placeholder scan:** placeholders `<VERSAO_*>` são intencionais (resolvidos no Task 12). Nenhum TBD/TODO no corpo dos specs de notas.

**Type consistency:** nomes de arquivos consistentes (Tasks 1, 3-11, 12). Verbetes consistentes (Tasks 3-10, 13).

**Cross-galho:** Task 4 e 7 referenciam outras notas existentes do mesmo galho — consistente.

Pronto pra execução.
