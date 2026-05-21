---
title: "Plano — Execução do Galho 2 da trilha Terminal (Shell / Zsh + OMZ + Powerlevel10k)"
date: 2026-05-19
status: ready
type: plan
publish: false
---

# Galho 2 da trilha Terminal (Shell) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir, em `03-Dominios/Terminal/Shell/`, **10 notas atômicas + 1 MOC do galho** (Iniciado 4 + Adepto 4 + Magus 2) cobrindo Zsh + Oh-My-Zsh + Powerlevel10k do "Zsh vs Bash" até "escrevendo seu plugin OMZ". Em paralelo, expandir `03-Dominios/Terminal/Dicionário do Terminal.md` com **≥30 verbetes novos** no bloco "Shell / Zsh / OMZ" e ativar o wikilink do Shell no tronco `03-Dominios/Terminal/index.md`. Todos os arquivos com `publish: true`, PT-BR, com seção "Em inglês" por nota (mini-glossário PT→EN).

**Architecture:** Galho atômico em pasta dedicada (`Terminal/Shell/`), com MOC interno + 10 notas numeradas (`NN - Título.md`). Dicionário do Terminal já existe (criado no galho 1) — adiciona-se bloco novo "Shell / Zsh / OMZ" após os blocos existentes, preservando wikilinks vivos. OMZ + P10k é o caminho primário em Iniciado/Adepto (porque é o setup real do usuário); Zsh puro aparece quando o conceito é universal (history, setopt, expansion) e domina em Magus. Cada nota segue template híbrido (TL;DR + corpo técnico + "Em inglês" + "Veja também" + "Referências"). Wikilinks densos: nota↔nota, nota→verbete, nota→tronco, MOC→todas as notas. Ordem de execução: por fase (01→04, 05→08, 09→10) com commit por nota.

**Tech Stack:** Markdown (Obsidian Flavored), wikilinks Obsidian, callouts, frontmatter YAML, Quartz para publicação. Sem código executável de sistema — code samples são snippets de `~/.zshrc`/`~/.p10k.zsh` (Zsh) ou comandos shell de uma linha. Testes locais ocasionais (`zsh -c '<snippet>'` ou `source ~/.zshrc` em sub-shell) em notas que mostram config (02, 03, 06, 08).

**Referências:**
- Spec: `docs/superpowers/specs/2026-05-19-terminal-shell-design.md`
- Roadmap macro: `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`
- Plano do galho 1 (formato análogo, proven): `docs/superpowers/plans/2026-05-19-terminal-editor-execution.md`
- Tronco Terminal a atualizar no fim: `03-Dominios/Terminal/index.md`
- Dicionário do Terminal (já existe, expandir): `03-Dominios/Terminal/Dicionário do Terminal.md`

---

## ⚠️ Restrições absolutas

### Fabricação de experiência

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável. **Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes ou casos não-vividos.**

Para a seção "Na prática" e exemplos:

- "Padrão observado na comunidade Zsh / OMZ" — OK
- "Caso típico em setups com OMZ + P10k" — OK
- "Armadilha comum reportada na issue tracker do OMZ / awesome-zsh-plugins" — OK
- Citações com fonte verificável (docs oficiais, Zsh manual, repos públicos) — OK
- Hipotéticos explícitos ("Imagine que você quer fazer X…") — OK
- Trechos do `~/.zshrc` real do usuário (com paths generalizados pra `~/...`) — OK como ilustração, **sem narrar** como pessoal ("o autor configura assim" é OK; "o autor usou isso pra resolver Y" é fabricação)
- "Eu uso isso no meu projeto X em Y empresa" — **PROIBIDO**

Quando faltar contexto factual ou houver dúvida sobre versão/comportamento de plugin, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

### Commits sem Co-Authored-By

A memória [Nao assinar commits](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_commits.md) é regra inegociável. **Nenhum commit deste plano leva `Co-Authored-By: Claude`.** Nem `--no-verify` nem `--no-gpg-sign` salvo pedido explícito.

### Isolamento público/apocrypha

Este galho é 100% público. **Nenhum arquivo aqui pode referenciar conteúdo do apocrypha** — sem wikilinks, paths ou menções. Tudo o que entra é citável publicamente.

### Não remover `index.md` do Quartz

A memória [Nunca remover index.md Quartz](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_quartz_index.md) é regra inegociável. **O `03-Dominios/Terminal/index.md` é editado, nunca removido.** A pasta `Shell/` recebe seu próprio `index.md` como MOC do galho — criar, não substituir nada.

### Paths em samples públicos

Generalizar **sempre**: `/home/josenaldo/repos/...` → `~/repos/...` (ou omitir). Aliases pessoais (e.g., `codemed`, `notify-waiting`, `notify-completed`) ficam como exemplo anonimizado ou opcional. Nada que vincule a um repo privado específico.

---

## File Structure

11 arquivos novos + 2 modificados:

```
03-Dominios/Terminal/
├── Dicionário do Terminal.md                                # MODIFICADO (Task 2 — bloco novo + verbetes; Task 8 — Keymap expandido; Task 14 — pass final)
├── index.md                                                  # MODIFICADO (Task 15 — ativa wikilink Shell)
└── Shell/
    ├── index.md                                              # MOC do galho — Task 1 (esqueleto), Task 13 (pass final)
    ├── 01 - Zsh vs Bash.md                                   # Task 3
    ├── 02 - Zsh essencial.md                                 # Task 4
    ├── 03 - History do Zsh.md                                # Task 5
    ├── 04 - Oh-My-Zsh — anatomia e plugins essenciais.md     # Task 6
    ├── 05 - Powerlevel10k.md                                 # Task 7
    ├── 06 - Keybindings práticos.md                          # Task 8
    ├── 07 - ZLE.md                                           # Task 9
    ├── 08 - Completion system (compsys).md                   # Task 10
    ├── 09 - Globbing avançado e parameter expansion.md       # Task 11
    └── 10 - Plugins, themes e custom no OMZ.md               # Task 12
```

**Tasks finais (13, 14, 15, 16):**
- Pass final no MOC do galho com wikilinks confirmados e versões exatas
- Pass final no Dicionário do Terminal (alfabetização dentro do bloco novo, "Veja também" por verbete)
- Atualização do tronco `Terminal/index.md` (bullet do Shell vira wikilink ativo)
- Validação final (`verificar-wikilinks` em `Shell/` + build Quartz local se disponível)

---

## Template padrão por nota

Definido uma vez, aplicado a todas as 10 notas. Variações permitidas estão na seção 6 do spec.

```markdown
---
title: "<título sem prefixo numérico>"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: <iniciado | adepto | magus>
tags:
  - terminal
  - shell
  - zsh
  - <fase>
  - <tag específica: oh-my-zsh, p10k, compsys, etc>
aliases:
  - <opcional>
---

# <Título>

> [!abstract] TL;DR
> 2-4 linhas em PT-BR. Conceito + regra prática + por que importa.

## O que é / Como funciona

<1-3 parágrafos. Definição precisa. Pressupõe leitura do MOC do galho ou consulta paralela ao Dicionário.>

## Na prática

<Exemplos concretos: trechos de ~/.zshrc, comandos Zsh executáveis, output esperado. Para 05 (P10k), sub-headings por área (Instant prompt, Wizard, Segmentos, Estilos). Para 08 (compsys) e 09 (globbing+expansion), sub-headings em "Na prática" pra blocos densos.>

## Armadilhas

<2+ armadilhas reais reportadas na comunidade ou observadas no setup do usuário (anonimizadas). Não genéricas — específicas do tema. Cada armadilha = causa + sintoma + como detectar.>

## Em inglês

<5-10 termos PT → EN. Cada termo com 1 frase curta de uso em contexto técnico (PR review, pair programming, docs).>

Ex:
- **shell interativo** — *interactive shell*. "Most shell configuration belongs in `.zshrc`, which is sourced only for interactive shells."
- **completar comando** — *complete a command*. "Hit `Tab` to complete the partial command name."

## Veja também

- [[<outra nota do galho>]] — relação
- [[03-Dominios/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]] (tronco)
- [[Dicionário do Terminal#<verbete relevante>|<verbete>]] — quando útil

## Referências

- <URL primária 1>
- <URL primária 2>
- <URL secundária 1>
- ...
```

### Critérios de qualidade por nota (rubrica)

Aplicar como checklist no Step de validação de cada task de nota:

- [ ] TL;DR em callout `[!abstract]`, 2-4 linhas, compreensível em <30s
- [ ] 2+ wikilinks pra outras notas do galho + 1+ wikilink pro MOC do galho ou tronco
- [ ] 2+ exemplos práticos concretos (trecho de `~/.zshrc`, comando, output esperado)
- [ ] Seção "Em inglês" com 5-10 termos PT→EN + 1 frase de uso por termo
- [ ] Seção "Armadilhas" com 2+ casos concretos (não genéricos, com causa+sintoma+como detectar)
- [ ] Wikilinks pros verbetes do Dicionário (lista por nota nas Tasks 3-12, alinhada ao spec §5)
- [ ] Frontmatter completo (`publish: true`, `status: seedling`, `fase: <fase>`, tags consistentes)
- [ ] PT-BR natural; termos técnicos em inglês mantidos (shell, prompt, widget, completion, glob, plugin, theme…)
- [ ] **Zero atribuição de experiência pessoal fabricada** ao autor (regra absoluta)
- [ ] Paths generalizados pra `~/...` (sem `/home/josenaldo/...`)
- [ ] Nenhuma alegação técnica não-trivial sem fonte ou exemplo que comprove

---

## Bibliografia centralizada

Consulta rápida durante a escrita. URLs verificadas no spec §5 e §9.

### Fontes canônicas globais

- **Zsh manual (completo):** `https://zsh.sourceforge.io/Doc/Release/`
- **Zsh FAQ:** `https://zsh.sourceforge.io/FAQ/`
- **A User's Guide to the Z-Shell (Peter Stephenson):** `https://zsh.sourceforge.io/Guide/zshguide.html`
- **Oh-My-Zsh wiki:** `https://github.com/ohmyzsh/ohmyzsh/wiki`
- **Powerlevel10k repo + README:** `https://github.com/romkatv/powerlevel10k`
- **awesome-zsh-plugins:** `https://github.com/unixorn/awesome-zsh-plugins`
- **zsh-users (org canônica de plugins):** `https://github.com/zsh-users`
- **/r/zsh:** `https://www.reddit.com/r/zsh/`

### Páginas específicas do Zsh manual

- **Options:** `https://zsh.sourceforge.io/Doc/Release/Options.html`
- **Shell Builtin Commands:** `https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html`
- **Expansion:** `https://zsh.sourceforge.io/Doc/Release/Expansion.html`
- **Zsh Line Editor (ZLE):** `https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html`
- **Completion System:** `https://zsh.sourceforge.io/Doc/Release/Completion-System.html`
- **Completion Widgets:** `https://zsh.sourceforge.io/Doc/Release/Completion-Widgets.html`
- **Prompt Expansion:** `https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html`

### Plugins externos referenciados

- **zsh-autosuggestions:** `https://github.com/zsh-users/zsh-autosuggestions`
- **zsh-syntax-highlighting:** `https://github.com/zsh-users/zsh-syntax-highlighting`
- **fast-syntax-highlighting:** `https://github.com/zdharma-continuum/fast-syntax-highlighting`
- **zsh-autocomplete:** `https://github.com/marlonrichert/zsh-autocomplete`
- **zsh-history-substring-search:** `https://github.com/zsh-users/zsh-history-substring-search`
- **fzf-tab:** `https://github.com/Aloxaf/fzf-tab`
- **softmoth/zsh-vim-mode:** `https://github.com/softmoth/zsh-vim-mode`

### Alternativas (citadas em "Veja também")

- **Starship:** `https://starship.rs/`
- **Pure prompt:** `https://github.com/sindresorhus/pure`
- **Oh-My-Posh:** `https://ohmyposh.dev/`
- **Atuin (history sync):** `https://docs.atuin.sh/`
- **Prezto (alternativa a OMZ):** `https://github.com/sorin-ionescu/prezto`
- **Zinit (plugin manager):** `https://github.com/zdharma-continuum/zinit`

### Configuração-âncora do usuário (referência local)

Setup real do usuário (verificado em 2026-05-19) — usado como caminho primário, com paths generalizados:

- Zsh 5.9 (Ubuntu/Linux bundle)
- OMZ master (~commit `a071263`, maio/2026)
- P10k master (commit `2b7da93`, 2024-07) instalado via git em `~/powerlevel10k/` (NÃO dentro de OMZ themes); style: rainbow + powerline, 2 linhas, nerdfont-v3, angled separators, sharp heads, instant_prompt configurado como `off` no `.zshrc`
- Plugins ativos: `git, zsh-autosuggestions, fast-syntax-highlighting, zsh-syntax-highlighting, zsh-autocomplete, direnv, yarn-autocompletions`
- Conflitos visíveis (mencionar como armadilhas em 04, 08): double-load `fast-syntax-highlighting` + `zsh-syntax-highlighting`; `zsh-autocomplete` vs OMZ completion default; NVM duplicado em `.zshenv` e `.zshrc`
- Customizações: bindkey Home/End (`bindkey '^[[H' beginning-of-line`, `bindkey '^[[F' end-of-line`), `DISABLE_MAGIC_FUNCTIONS=true`

---

## Task 0: Pré-flight

**Files:**
- Create: `03-Dominios/Terminal/Shell/` (diretório)

- [ ] **Step 1: Verificar contexto e memórias críticas**

Run:
```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -iE "fabrica|invent|assinar|commit|quartz|apocrypha"
```

Expected: pelo menos linhas referenciando `feedback_no_fabrication.md`, `feedback_commits.md`, `feedback_quartz_index.md`, `feedback_public_apocrypha_separation.md`. Se faltar alguma, **abortar e pedir reload de memória** antes de prosseguir.

- [ ] **Step 2: Confirmar que pré-requisitos existem (galho 1 entregue + spec)**

Run:
```bash
test -f "03-Dominios/Terminal/index.md" && echo "ok: tronco existe"
test -f "03-Dominios/Terminal/Dicionário do Terminal.md" && echo "ok: dicionário existe (galho 1)"
test -d "03-Dominios/Terminal/Editor" && echo "ok: galho 1 entregue"
test -f "docs/superpowers/specs/2026-05-19-terminal-shell-design.md" && echo "ok: spec existe"
test ! -d "03-Dominios/Terminal/Shell" && echo "ok: Shell/ ainda não existe" || echo "ATENÇÃO: Shell/ já existe — investigar"
```

Expected: 5 linhas `ok:`. Qualquer "ATENÇÃO" = parar e investigar (pode ser sessão anterior incompleta).

- [ ] **Step 3: Confirmar branch e working tree limpa**

Run:
```bash
git status --short
git rev-parse --abbrev-ref HEAD
```

Expected: branch `main` e working tree limpa (sem changes pendentes não relacionados). Se houver changes pendentes, decidir com o usuário se commita/stash antes de prosseguir.

- [ ] **Step 4: Capturar versões reais do setup do usuário**

Run:
```bash
zsh --version
(cd ~/.oh-my-zsh && git log -1 --format='%h %ad' --date=short)
(cd ~/powerlevel10k && git log -1 --format='%h %ad' --date=short)
```

Expected: 3 linhas com versões. **Anotar os outputs reais** — vão substituir os placeholders do MOC no Task 13 (pass final).

- [ ] **Step 5: Criar o diretório `Shell/`**

Run:
```bash
mkdir -p "03-Dominios/Terminal/Shell"
ls -la "03-Dominios/Terminal/Shell"
```

Expected: diretório vazio criado.

- [ ] **Step 6: Sanity check das fontes-âncora principais**

Disparar 3 WebFetch em paralelo para confirmar acessibilidade:

```
WebFetch: https://zsh.sourceforge.io/Doc/Release/
WebFetch: https://github.com/ohmyzsh/ohmyzsh/wiki
WebFetch: https://github.com/romkatv/powerlevel10k
```

Capturar páginas iniciais; se alguma estiver fora do ar, registrar e pesquisar fontes alternativas no momento da nota afetada (não bloquear o galho).

- [ ] **Step 7: Sem commit aqui**

Como o `mkdir` cria pasta vazia (git ignora), pular o commit nesta task. O primeiro commit do galho será do MOC esqueleto (Task 1).

---

## Task 1: MOC do galho Shell — esqueleto

**Files:**
- Create: `03-Dominios/Terminal/Shell/index.md`

**Objetivo:** Criar o MOC do galho com as 10 notas listadas como wikilinks (mesmo que ainda não existam — Obsidian aceita wikilinks pendentes; Quartz só renderiza os vivos). Estrutura segue o spec §5.

- [ ] **Step 1: Escrever o arquivo**

Criar `03-Dominios/Terminal/Shell/index.md` com **exatamente** o conteúdo abaixo (versões com placeholders — preenchidos no Task 13):

````markdown
---
title: "Shell"
type: moc
publish: true
created: 2026-05-19
updated: 2026-05-19
status: growing
progresso: andamento
tags:
  - terminal
  - shell
  - zsh
  - oh-my-zsh
  - powerlevel10k
  - moc
aliases:
  - Shell
  - Zsh
  - Oh-My-Zsh
  - Powerlevel10k
---
# Shell

> [!abstract] TL;DR
> Galho 2 da trilha Terminal. Domínio de Zsh + Oh-My-Zsh + Powerlevel10k como shell primário, em 3 fases (4 + 4 + 2 = 10 notas): do "Zsh vs Bash" ao escrever seu plugin OMZ e seu theme.

Esse galho cobre o shell end-to-end: fundamentos do Zsh e diferenças do Bash, history e plugins essenciais do OMZ (Iniciado), customização com Powerlevel10k, keybindings, ZLE e completion system (Adepto), e maestria com globbing avançado, parameter expansion e plugins/themes próprios (Magus). OMZ + P10k é o caminho primário porque é o setup real operado; Zsh puro aparece quando o conceito é universal.

## Conteúdo

### Iniciado

- [[01 - Zsh vs Bash]]
- [[02 - Zsh essencial]]
- [[03 - History do Zsh]]
- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]]

### Adepto

- [[05 - Powerlevel10k]]
- [[06 - Keybindings práticos]]
- [[07 - ZLE]]
- [[08 - Completion system (compsys)]]

### Magus

- [[09 - Globbing avançado e parameter expansion]]
- [[10 - Plugins, themes e custom no OMZ]]

## Rotas alternativas

- **Daily-driver enxuto** (Iniciado completa): `01` → `02` → `03` → `04`
- **Customização visual**: `04` → `05` → `10`
- **Domínio do motor**: `02` → `06` → `07` → `08` → `09`

## Versões assumidas

- **Zsh:** 5.9+ (Ubuntu/Linux bundle) — versão capturada no Task 0
- **Oh-My-Zsh:** `master` em ~maio/2026 (commit declarado em pass final)
- **Powerlevel10k:** `master` 2024-07 (commit declarado em pass final) — projeto em modo manutenção
- Plugins externos: versões `master` em 2026-05-19

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
````

Use `Write` com o conteúdo acima.

- [ ] **Step 2: Validar frontmatter e estrutura**

Run:
```bash
python3 -c "
import yaml
content = open('03-Dominios/Terminal/Shell/index.md').read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1])
assert fm.get('type') == 'moc', 'type não é moc'
assert fm.get('publish') is True, 'publish não é True'
assert fm.get('title') == 'Shell', 'title incorreto'
for t in ['terminal', 'shell', 'zsh', 'moc']:
    assert t in fm.get('tags', []), f'tag {t} ausente'
print('ok: frontmatter valid')
"
grep -c '^- \[\[' "03-Dominios/Terminal/Shell/index.md"
```

Expected: `ok: frontmatter valid` e contagem ≥ 12 (10 notas + Dicionário + tronco).

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Terminal/Shell/index.md"
git commit -m "$(cat <<'EOF'
feat(terminal-shell): scaffold MOC do galho Shell

Cria 03-Dominios/Terminal/Shell/index.md como MOC do galho 2 da trilha
Terminal. Lista as 10 notas planejadas (Iniciado 4 + Adepto 4 + Magus 2)
como wikilinks pendentes, mais 3 rotas alternativas (Daily-driver enxuto,
Customização visual, Domínio do motor) e versões assumidas (Zsh 5.9+,
OMZ master, P10k 2024-07).

Galho: docs/superpowers/specs/2026-05-19-terminal-shell-design.md
EOF
)"
```

---

## Task 2: Dicionário do Terminal — bloco "Shell / Zsh / OMZ" esqueleto

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (append do bloco novo)

**Objetivo:** Adicionar o bloco `## Shell / Zsh / OMZ` ao Dicionário do Terminal **após o último bloco existente** ("Avançado"), sem mexer nos verbetes já criados pelo galho 1. Verbetes individuais serão inseridos pelas Tasks 3-12 conforme cada nota usar o termo.

- [ ] **Step 1: Verificar estado atual do Dicionário**

Run:
```bash
grep -n "^## " "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: deve listar pelo menos 4 blocos do galho 1: `Vim / Neovim core`, `Ecossistema LazyVim`, `LSP & dev`, `Avançado`. Anotar o último — é onde o novo bloco será inserido **após**.

- [ ] **Step 2: Adicionar bloco "Shell / Zsh / OMZ" ao final**

Edit `03-Dominios/Terminal/Dicionário do Terminal.md` adicionando ao final do arquivo (após o último verbete do bloco "Avançado"):

```markdown

## Shell / Zsh / OMZ

```

(Linha em branco antes do `##`, depois `## Shell / Zsh / OMZ`, depois linha em branco final.)

Use `Edit` localizando o final do arquivo. Se o arquivo terminar em nova-linha sem conteúdo final, basta usar `Edit` com `old_string` = último verbete + sua "Veja também" + linha em branco, `new_string` = mesmo conteúdo + bloco novo.

- [ ] **Step 3: Atualizar `updated:` do dicionário**

Edit o frontmatter: `updated: 2026-05-19` (se já estiver, OK; se não, atualizar).

- [ ] **Step 4: Validar estrutura**

Run:
```bash
grep -n "^## " "03-Dominios/Terminal/Dicionário do Terminal.md"
grep -c "^### " "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: agora 5 blocos `##` (os 4 originais + "Shell / Zsh / OMZ"). Contagem de `###` igual ao número de verbetes existentes do galho 1 (≥ 30, ainda sem verbetes novos).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "$(cat <<'EOF'
feat(terminal): scaffold bloco Shell/Zsh/OMZ no Dicionário

Adiciona ## Shell / Zsh / OMZ ao Dicionário do Terminal (após bloco
Avançado), sem verbetes — serão preenchidos pelas notas do galho 2
conforme aparecem.

Verbetes existentes do galho 1 (Vim/Neovim core, Ecossistema LazyVim,
LSP & dev, Avançado) não tocados.

Galho: docs/superpowers/specs/2026-05-19-terminal-shell-design.md
EOF
)"
```

---

## Task 3: Nota 01 — Zsh vs Bash

**Files:**
- Create: `03-Dominios/Terminal/Shell/01 - Zsh vs Bash.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Shell, POSIX, Builtin)

**Conteúdo-chave do spec (§5, Iniciado):**

> O que é shell, shell interativo vs script. POSIX compliance. Diferenças sintáticas (arrays 1-indexed, `setopt` vs `shopt`, `${(L)var}` vs `${var,,}`, globbing). Por que migrar: interatividade rica, completion superior, extensibilidade. Custo: scripts Bash precisam de shebang ou `emulate bash`. Mito "Zsh é superset de Bash" — falso.

**Verbetes referenciados:** Shell, POSIX, Builtin.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Introduction.html
WebFetch: https://zsh.sourceforge.io/FAQ/zshfaq02.html
```

Capturar: definição precisa de shell, lista de diferenças canônicas Zsh vs Bash, history do Zsh.

- [ ] **Step 2: Criar frontmatter + esqueleto**

Criar `03-Dominios/Terminal/Shell/01 - Zsh vs Bash.md` com:

```yaml
---
title: "Zsh vs Bash"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - bash
aliases:
  - Zsh vs Bash
  - Por que Zsh
---
```

Seguido do esqueleto do template padrão.

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "Zsh é um shell interativo da família Bourne, parente próximo de Bash mas com escolhas diferentes — não é superset. Pra dev individual, o ganho está em completion programável superior, prompt rico, globbing avançado e extensibilidade via OMZ. Scripts Bash continuam rodando se você usar shebang `#!/usr/bin/env bash`."
- **O que é / Como funciona:**
  - Definição: shell = interpretador de comandos. Distinção interativo (`.zshrc` lê) vs não-interativo (script, `.zshrc` não lê).
  - Família Bourne (sh → ksh → bash → zsh). Linha do tempo curta (sh 1979, bash 1989, zsh 1990).
  - POSIX como mínimo comum; cada shell estende. Bash é "mais POSIX por default"; Zsh tem `emulate sh/bash/ksh` pra modo compat.
  - Mito "superset": Zsh NÃO roda todo script Bash sem ajuste. Diferenças sintáticas reais (próxima seção).
- **Na prática:**
  - Identificar shell atual: `echo $SHELL` (login shell), `ps -p $$` (shell atual em uso).
  - Trocar shell default: `chsh -s $(which zsh)` (precisa re-login).
  - Rodar script Bash em ambiente Zsh: shebang `#!/usr/bin/env bash` é obrigatório; ou `emulate bash` no topo do script.
  - **Diferenças sintáticas que mais aparecem:**
    - Arrays: Zsh 1-indexed (`arr[1]`), Bash 0-indexed (`arr[0]`)
    - Options: Zsh `setopt EXTENDED_GLOB`, Bash `shopt -s extglob`
    - Case conversion: Zsh `${(L)var}`/`${(U)var}`, Bash `${var,,}`/`${var^^}`
    - Globbing: Zsh `**/*.ts` recursivo nativo; Bash requer `shopt -s globstar`
    - Word splitting: Zsh NÃO faz split em `$var` por default; Bash faz (gera bugs ao migrar).
  - Block exemplo do `~/.zshrc` mostrando "isso aqui só roda em Zsh".
- **Armadilhas:**
  - (1) **Script Bash que assume word splitting**: `for x in $list; do ...` quebra silenciosamente em Zsh sem `setopt SH_WORD_SPLIT`. Sintoma: loop ignora itens. Detectar: rodar com `set -x`.
  - (2) **Migração de aliases que conflitam**: alias Bash usando `${var,,}` falha em Zsh com erro de parsing. Sintoma: `bad substitution`. Solução: reescrever com `${(L)var}` ou adicionar `emulate bash -c`.
  - (3) **Indexação 0 vs 1**: hábito Bash de `${arr[0]}` retorna vazio em Zsh (que começa em 1). Detectar: `echo $arr[1]` retorna o primeiro elemento.
- **Em inglês:** shell, shell interativo (interactive shell), shell de login (login shell), script, builtin, conformidade POSIX (POSIX compliance), indexação (indexing), expansão (expansion), divisão de palavras (word splitting), emular (emulate). Cada termo com 1 frase técnica.
- **Veja também:**
  - `[[02 - Zsh essencial]]`
  - `[[03 - History do Zsh]]`
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]`
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Shell|shell]]`, `[[Dicionário do Terminal#POSIX|POSIX]]`, `[[Dicionário do Terminal#Builtin|builtin]]`
- **Referências:** Zsh Introduction, Zsh FAQ — Differences from Bash, A User's Guide to the Z-Shell.

Tamanho-alvo: 250-350 linhas.

- [ ] **Step 4: Adicionar verbetes ao Dicionário (bloco "Shell / Zsh / OMZ")**

Inserir em ordem alfabética dentro do bloco `## Shell / Zsh / OMZ`:

```markdown
### Builtin
Comando implementado diretamente pelo shell (não é binário externo no `$PATH`). Em Zsh: `setopt`, `bindkey`, `zstyle`, `compinit`, `print`, `read`, `typeset`. Mais rápido que comando externo; semântica integrada ao shell.

Veja também: [[01 - Zsh vs Bash]], [[02 - Zsh essencial]].

### POSIX
Portable Operating System Interface — padrão IEEE que define APIs e comportamento de shell mínimos. Bash é mais próximo do POSIX por default; Zsh estende livremente mas oferece `emulate sh|bash|ksh` quando precisa de compat.

Veja também: [[01 - Zsh vs Bash]].

### Shell
Interpretador de comandos de um sistema Unix-like. Pode ser interativo (lê `.zshrc`, edita linha) ou não-interativo (script). A família Bourne agrupa sh, ksh, bash e zsh — sintaxe próxima mas extensões e defaults divergem.

Veja também: [[01 - Zsh vs Bash]].
```

Atualizar `updated:` do dicionário para `2026-05-19`.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/01 - Zsh vs Bash.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/01 - Zsh vs Bash.md"
grep -c '^## ' "03-Dominios/Terminal/Shell/01 - Zsh vs Bash.md"
grep -E "^### (Builtin|POSIX|Shell)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥6 wikilinks, ≥5 sub-headings na nota, 3 verbetes novos no Dicionário.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/01 - Zsh vs Bash.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 01 — Zsh vs Bash"
```

---

## Task 4: Nota 02 — Zsh essencial

**Files:**
- Create: `03-Dominios/Terminal/Shell/02 - Zsh essencial.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Alias, Function (shell), Setopt)

**Conteúdo-chave do spec (§5, Iniciado):**

> `alias` (regular, `-g` global, `-s` suffix). Funções: declaração, `local`, `return`, parâmetros. `setopt`/`unsetopt`. Opts essenciais (`AUTO_CD`, `EXTENDED_GLOB`, `INTERACTIVE_COMMENTS`, `NO_BEEP`, `CORRECT`). Variáveis vs env (`export`, `typeset`, `local`, `readonly`). Onde colocar tudo: `~/.zshrc` vs `~/.zshenv` vs `~/.zprofile`. Loading order: `.zshenv` → `.zprofile` (login) → `.zshrc` (interactive) → `.zlogin`.

**Verbetes referenciados:** Alias, Function (shell), Setopt.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Options.html
WebFetch: https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html
```

Capturar: lista canônica de opts, sintaxe `alias`/`function`/`setopt`, distinção `local`/`typeset`/`export`.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Zsh essencial"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - aliases
  - functions
  - setopt
aliases:
  - Zsh essencial
  - Aliases, funções e opts
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "Aliases viram comandos longos em curtos. Funções juntam várias linhas com parâmetros e return code. `setopt` muda comportamento do shell (case-insensitive, EXTENDED_GLOB, AUTO_CD). Onde colocar tudo: `~/.zshrc` (interativo) vs `~/.zshenv` (sempre)."
- **O que é / Como funciona:**
  - Aliases — 3 tipos:
    - Regular: `alias gco='git checkout'` (expansão só no início do comando)
    - Global (`-g`): `alias -g G='| grep'` (expansão em qualquer posição)
    - Suffix (`-s`): `alias -s md=nvim` (`./README.md` abre nvim)
  - Funções — declaração e mecânica:
    - `f() { ... }` vs `function f { ... }` (equivalentes)
    - Parâmetros: `$1`, `$2`, `$@` (todos), `$#` (contagem), `$0` (nome)
    - `local` (scope dentro da função), `return N` (exit code)
    - Quando alias vs função: alias = renomear; função = lógica/parâmetros
  - `setopt` — interface de opts:
    - `setopt EXTENDED_GLOB` (liga), `unsetopt EXTENDED_GLOB` (desliga)
    - `setopt` (lista todas ligadas), `setopt | grep <name>` (busca)
  - Variáveis vs env:
    - `var=val` (local à shell), `export var=val` (visível a subprocessos)
    - `typeset -r var=val` (readonly), `local var` (scope função)
    - `typeset -U PATH` (uniq — remove duplicatas; usado pra limpar PATH)
  - **Loading order** (CRÍTICO):
    - Sempre: `~/.zshenv` → `~/.zprofile` (se login) → `~/.zshrc` (se interactive) → `~/.zlogin` (se login, último)
    - **Onde colocar o quê:**
      - `~/.zshenv`: `EDITOR`, `PATH`, env vars que processos não-interativos precisam
      - `~/.zshrc`: aliases, funções interativas, `setopt`, plugins OMZ, prompt
      - `~/.zprofile`: comandos que rodam uma vez no login (NVM antes era aqui)
- **Na prática:**
  - **Bloco-exemplo de `~/.zshrc` (opts essenciais):**
    ```zsh
    # AUTO_CD: digite só o diretório (sem `cd`) e ele entra
    setopt AUTO_CD

    # Comentários inline no shell interativo
    setopt INTERACTIVE_COMMENTS  # agora `# isso é comentário` funciona

    # Globbing extended (necessário pra muito do que Zsh oferece de melhor)
    setopt EXTENDED_GLOB

    # Sem bipe ao errar
    setopt NO_BEEP

    # Sugere correção quando comando não existe
    setopt CORRECT

    # Substituição em prompt (necessário pra muitos temas)
    setopt PROMPT_SUBST
    ```
  - **Função de exemplo (mkcd):**
    ```zsh
    mkcd() {
      local dir="$1"
      [[ -z "$dir" ]] && { print -u2 "usage: mkcd <dir>"; return 1; }
      mkdir -p "$dir" && cd "$dir"
    }
    ```
  - **Alias útil que mostra global alias:**
    ```zsh
    alias -g L='| less'         # `ps aux L` → `ps aux | less`
    alias -g G='| grep'
    ```
- **Armadilhas:**
  - (1) **Alias que sobrescreve comando**: `alias ls='ls --color'` é benigno; `alias rm='rm -i'` muda semântica e quebra scripts (que assumem `rm` sem prompt). Sintoma: script chama `rm`, fica esperando input. Detectar: `\rm` ou `command rm` bypassa alias.
  - (2) **`export` em função pollui shell**: variável `export` dentro de função vaza pra subprocessos depois. Use `local` se for temporária.
  - (3) **`.zshenv` lê em TUDO**: comando lento ou interativo (NVM, completions) em `.zshenv` derruba performance de scripts. Mova pra `.zshrc` se só interativo precisa.
  - (4) **`setopt CORRECT` no contexto errado** sugere correções em loops/scripts. Desligar com `unsetopt CORRECT` antes de blocks sensíveis.
- **Em inglês:** alias, função (function), opt (option), shell interativo (interactive shell), exportar variável (export variable), escopo local (local scope), código de retorno (return code), variável de ambiente (environment variable), shell de login (login shell), ordem de carregamento (loading order).
- **Veja também:**
  - `[[01 - Zsh vs Bash]]`
  - `[[03 - History do Zsh]]`
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]`
  - `[[09 - Globbing avançado e parameter expansion]]` — `EXTENDED_GLOB` é pré-req
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Alias|alias]]`, `[[Dicionário do Terminal#Function (shell)|função]]`, `[[Dicionário do Terminal#Setopt|setopt]]`
- **Referências:** Zsh manual — Options, Shell Builtin Commands, Stephenson's guide.

Tamanho-alvo: 350-450 linhas.

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Alias
Atalho que expande pra outra string antes da execução. Zsh tem 3 tipos: regular (`alias gco='git checkout'`), global (`alias -g G='| grep'`, expande em qualquer posição), e suffix (`alias -s md=nvim`, dispara pelo sufixo do arquivo).

Veja também: [[02 - Zsh essencial]].

### Function (shell)
Bloco nomeado de comandos executável como se fosse comando. Sintaxe Zsh: `f() { ... }` ou `function f { ... }`. Aceita parâmetros (`$1`, `$@`), variáveis `local`, e `return <código>`. Diferente de alias: tem lógica.

Veja também: [[02 - Zsh essencial]].

### Setopt
Builtin do Zsh que ativa/desativa opções do shell. `setopt EXTENDED_GLOB` liga, `unsetopt` desliga, `setopt` sozinho lista as ativas. Opts comuns: `AUTO_CD`, `EXTENDED_GLOB`, `INTERACTIVE_COMMENTS`, `NO_BEEP`, `CORRECT`, `PROMPT_SUBST`, `SHARE_HISTORY`.

Veja também: [[02 - Zsh essencial]], [[03 - History do Zsh]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/02 - Zsh essencial.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/02 - Zsh essencial.md"
grep -c '^## ' "03-Dominios/Terminal/Shell/02 - Zsh essencial.md"
grep -E "^### (Alias|Function|Setopt)" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥6 wikilinks, ≥5 sub-headings, 3 verbetes novos visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/02 - Zsh essencial.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 02 — Zsh essencial"
```

---

## Task 5: Nota 03 — History do Zsh

**Files:**
- Create: `03-Dominios/Terminal/Shell/03 - History do Zsh.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: History, fc)

**Conteúdo-chave do spec (§5, Iniciado):**

> `HISTFILE`, `HISTSIZE`/`SAVEHIST`, opts (`SHARE_HISTORY`, `EXTENDED_HISTORY`, `HIST_IGNORE_ALL_DUPS`, `HIST_VERIFY`, `HIST_REDUCE_BLANKS`, `INC_APPEND_HISTORY`). Setup recomendado. `history` vs `fc` (`-l`, `-e`, `-ln`). Search incremental (`Ctrl-R`). History expansion (`!!`, `!$`, `!^`, `!*`, `^x^y^`).

**Verbetes referenciados:** History, fc.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Options.html#History
WebFetch: https://zsh.sourceforge.io/Doc/Release/Expansion.html#History-Expansion
WebFetch: https://docs.atuin.sh/
```

Capturar: opts canônicas de history (com defaults), sintaxe completa de history expansion, contexto de atuin (alternativa moderna).

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "History do Zsh"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - history
aliases:
  - History do Zsh
  - History
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "Zsh registra cada comando em `HISTFILE` (default `~/.zsh_history`). Configure opts de history (share entre sessões, sem duplicatas, com timestamp) e ganhe `Ctrl-R` (search incremental) + history expansion (`!!`, `!$`) + `fc` (editar comando como texto). É a ferramenta mais subutilizada do shell."
- **O que é / Como funciona:**
  - **Variáveis chave:**
    - `HISTFILE` (default `~/.zsh_history`) — arquivo onde history vai
    - `HISTSIZE` — quantas linhas mantidas em **memória** (recomendado: 50000)
    - `SAVEHIST` — quantas linhas mantidas no **disco** (recomendado: 50000)
  - **Opts essenciais (com explicação de cada uma):**
    - `SHARE_HISTORY` — múltiplas sessões compartilham history em tempo real
    - `EXTENDED_HISTORY` — grava timestamp + duração de cada comando
    - `HIST_IGNORE_ALL_DUPS` — remove duplicatas do history (mantém a mais recente)
    - `HIST_IGNORE_SPACE` — comando começando com espaço não vai pro history (útil pra `<space>secret-cmd`)
    - `HIST_REDUCE_BLANKS` — normaliza whitespace antes de salvar
    - `HIST_VERIFY` — `!!` expande pra linha visível antes de executar (não auto-executa)
    - `INC_APPEND_HISTORY` — escreve no `HISTFILE` imediatamente (não só ao sair)
  - **Comandos:**
    - `history` — lista últimos comandos
    - `history -i` — com timestamps (precisa de `EXTENDED_HISTORY`)
    - `fc -l N M` — list (range opcional)
    - `fc -e <editor>` — edita o último comando no editor
    - `fc <substring>` — executa último comando que casa com substring
  - **Search:**
    - `Ctrl-R` — search incremental backward (default)
    - `Ctrl-S` — forward (geralmente bloqueado pelo terminal — `stty -ixon` libera)
  - **History expansion** (do Zsh manual):
    - `!!` — último comando inteiro
    - `!$` — último argumento do último comando
    - `!^` — primeiro argumento
    - `!*` — todos os argumentos
    - `!:N` — argumento N
    - `^old^new` — substitui `old` por `new` no último comando
    - `!<prefix>` — último comando que começa com `<prefix>`
- **Na prática:**
  - **Bloco recomendado pra `~/.zshrc`:**
    ```zsh
    HISTFILE=~/.zsh_history
    HISTSIZE=50000
    SAVEHIST=50000

    setopt SHARE_HISTORY            # share entre sessões
    setopt EXTENDED_HISTORY         # timestamp + duração
    setopt HIST_IGNORE_ALL_DUPS     # sem duplicatas
    setopt HIST_IGNORE_SPACE        # comando com espaço inicial é privado
    setopt HIST_REDUCE_BLANKS       # normaliza whitespace
    setopt HIST_VERIFY              # !! não auto-executa
    setopt INC_APPEND_HISTORY       # escreve imediato
    ```
  - **Search prático:** `Ctrl-R` → digita parte do comando → `Ctrl-R` cicla matches → `Enter` executa, `Esc` cancela.
  - **Editar último comando longo:** `fc` (sem args) abre `$EDITOR` com o comando; salvar+sair executa.
  - **Re-executar com tweak:** `^ts^js` substitui `ts` por `js` no último comando.
  - **Skip history:** `<space>echo $SECRET` (com espaço inicial) não vai pro history (precisa `HIST_IGNORE_SPACE`).
- **Armadilhas:**
  - (1) **`HISTSIZE` < `SAVEHIST`** — comandos somem do arquivo. Regra: `HISTSIZE >= SAVEHIST` sempre.
  - (2) **`SHARE_HISTORY` + edição offline** — se você editar `.zsh_history` manualmente em uma sessão e outra estiver aberta, as duas brigam por overwrite. Solução: feche outras sessões antes.
  - (3) **`HIST_VERIFY` esquecido + `!!`** — sem `HIST_VERIFY`, `sudo !!` executa direto. Hábito perigoso em comando destrutivo. Default-on no setup.
  - (4) **Atuin "substituiu" history nativo** — atuin é alternativa popular, mas substitui `Ctrl-R` e tem DB próprio. Não rodar atuin + history-substring-search simultaneamente sem entender ordem de hooks.
- **Em inglês:** histórico do shell (shell history), expansão de histórico (history expansion), pesquisa incremental (incremental search), arquivo de histórico (history file), duplicata (duplicate), timestamp, comando privado (private command, no-history), `fc` (fix command).
- **Veja também:**
  - `[[02 - Zsh essencial]]` — `setopt` é pré-req
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]` — plugin `history-substring-search`
  - `[[06 - Keybindings práticos]]` — bindar `Ctrl-R` custom
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#History|history]]`, `[[Dicionário do Terminal#fc|fc]]`
- **Referências:** Zsh manual — Options (HIST_*), Shell Builtin (fc), Expansion (History Expansion), atuin docs.

Tamanho-alvo: 300-400 linhas.

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### fc
Builtin do Zsh ("fix command") que lista (`fc -l`) ou edita (`fc` puro abre $EDITOR com o último comando) entradas do history. `fc <substring>` re-executa o último comando que casa com a substring.

Veja também: [[03 - History do Zsh]].

### History
Registro persistente de comandos digitados, gravado em `HISTFILE` (default `~/.zsh_history`). Configurado por `HISTSIZE`/`SAVEHIST` + opts (`SHARE_HISTORY`, `EXTENDED_HISTORY`, `HIST_IGNORE_ALL_DUPS`, `HIST_VERIFY`). Acessado via `history`, `Ctrl-R`, `!!`, `!$`, `fc`.

Veja também: [[03 - History do Zsh]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/03 - History do Zsh.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/03 - History do Zsh.md"
grep -E "^### (History|fc)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥6 wikilinks, 2 verbetes novos visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/03 - History do Zsh.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 03 — History do Zsh"
```

---

## Task 6: Nota 04 — Oh-My-Zsh — anatomia e plugins essenciais

**Files:**
- Create: `03-Dominios/Terminal/Shell/04 - Oh-My-Zsh — anatomia e plugins essenciais.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Oh-My-Zsh, Plugin (OMZ), Zsh-autosuggestions, Zsh-syntax-highlighting)

**Conteúdo-chave do spec (§5, Iniciado):**

> Layout de `~/.oh-my-zsh/`. `oh-my-zsh.sh` loader. Array `plugins=(...)`. Plugins essenciais (git, autosuggestions, syntax-highlighting, direnv). Plugins debatíveis (fzf-tab, zsh-autocomplete). Update mode. Pitfalls: double-load de plugins ("syntax-highlighting" + "fast-syntax-highlighting"), ordem importa (syntax-highlight ÚLTIMO), `DISABLE_MAGIC_FUNCTIONS=true`.

**Verbetes referenciados:** Oh-My-Zsh, Plugin (OMZ), Zsh-autosuggestions, Zsh-syntax-highlighting.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins
WebFetch: https://github.com/zsh-users/zsh-autosuggestions
WebFetch: https://github.com/zsh-users/zsh-syntax-highlighting
WebFetch: https://github.com/marlonrichert/zsh-autocomplete
```

Capturar: lista canônica de plugins OMZ, README dos plugins externos com instruções de install + ordem de carregamento.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Oh-My-Zsh — anatomia e plugins essenciais"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - oh-my-zsh
  - plugins
aliases:
  - Oh-My-Zsh
  - OMZ
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "Oh-My-Zsh é um framework de config pra Zsh: você clona em `~/.oh-my-zsh/`, source no `.zshrc`, e ganha um loader que ativa plugins via array `plugins=(...)`. Plugins essenciais (git, autosuggestions, syntax-highlighting, direnv) cobrem 90% das necessidades. Ordem importa: syntax-highlighting DEVE ser o último."
- **O que é / Como funciona:**
  - OMZ ≠ Zsh. OMZ é overlay de config. Sem OMZ, Zsh funciona; com OMZ, ganha plugin loader + 300+ plugins + 150+ temas.
  - **Layout de `~/.oh-my-zsh/`:**
    - `oh-my-zsh.sh` — entrypoint, executa init (compinit, plugin loop, theme)
    - `lib/` — funções helper (history, theme-and-appearance, completion)
    - `plugins/` — plugins embarcados (git, kubectl, npm, …)
    - `themes/` — temas embarcados
    - `custom/` — *seu* terreno (plugins custom, themes custom, aliases, overrides)
    - `cache/` — completion cache, last-update
  - **`oh-my-zsh.sh` em ordem (simplificado):** check update → source lib/* → source completion-system (compinit) → loop sobre `plugins=(...)` → source theme → user customizations
  - **Array de plugins:**
    ```zsh
    plugins=(
      git
      zsh-autosuggestions
      zsh-syntax-highlighting   # SEMPRE último entre os syntax-related
    )
    ```
    OMZ procura `$ZSH/plugins/<nome>/<nome>.plugin.zsh` (embarcado), depois `$ZSH/custom/plugins/<nome>/<nome>.plugin.zsh` (custom). Plugins externos vão em `custom/plugins/`.
  - **Plugins essenciais (cada um vale 1 parágrafo curto):**
    - `git` — embarcado; aliases (`gst`, `gco`, `gp`, `glog`) + `current_branch` pra prompt
    - `zsh-autosuggestions` — externo (`zsh-users/zsh-autosuggestions`); sugestão cinza inline baseada em history; aceitar com `→` ou `Ctrl-F`
    - `zsh-syntax-highlighting` — externo (`zsh-users/zsh-syntax-highlighting`); colore comandos válidos/inválidos enquanto digita; DEVE ser último plugin
    - `direnv` — embarcado; integra `direnv` (env vars por diretório via `.envrc`)
  - **Plugins debatíveis (mencionar com tradeoff):**
    - `fast-syntax-highlighting` (zdharma-continuum) — alternativa mais rápida ao zsh-syntax-highlighting; NÃO usar os 2 juntos
    - `fzf-tab` (Aloxaf) — substitui menu de completion por interface fzf; muito popular; precisa source antes de syntax-highlighting
    - `zsh-autocomplete` (marlonrichert) — sobrepõe completion (mostra sugestões enquanto digita, sem Tab); muda fluxo significativamente; conflita com OMZ completion default
  - **Update mode:**
    ```zsh
    zstyle ':omz:update' mode reminder     # avisa quando tem update (default)
    zstyle ':omz:update' mode auto         # atualiza sem perguntar
    zstyle ':omz:update' mode disabled     # nunca
    zstyle ':omz:update' frequency 7       # de quantos em quantos dias
    ```
- **Na prática:**
  - **Instalar OMZ:** `sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
  - **Instalar plugin externo (zsh-autosuggestions):**
    ```bash
    git clone https://github.com/zsh-users/zsh-autosuggestions \
      ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    ```
    E adicionar `zsh-autosuggestions` ao array `plugins=(...)`.
  - **Ordem recomendada:**
    ```zsh
    plugins=(
      git
      direnv
      zsh-autosuggestions
      fzf-tab                       # se usar — antes do syntax-highlight
      zsh-syntax-highlighting       # ÚLTIMO
    )
    ```
  - **Inspecionar setup atual:**
    ```bash
    omz plugin list                 # lista plugins ativos
    omz plugin info git             # mostra README do plugin git
    omz update                      # roda update manual
    ```
- **Armadilhas:**
  - (1) **Double-load de syntax-highlight**: rodar `fast-syntax-highlighting` E `zsh-syntax-highlighting` juntos quebra cores ou degrada performance. Sintoma: sintaxe colorida estranha ou prompt lento ao digitar. Solução: escolher um, remover o outro do array.
  - (2) **Ordem errada: syntax-highlight ANTES de outros plugins**: precisa ser o último ou perde highlight de comandos adicionados depois. Sintoma: comandos definidos por plugin não coloridos.
  - (3) **`zsh-autocomplete` + completion default OMZ**: comportamento de Tab muda radicalmente; `_zsh-autocomplete` sobrepõe `_omz_completion`. Pode quebrar plugins que esperam o fluxo default. Se for adotar `zsh-autocomplete`, sair de plugins de completion competidores (incluindo `fzf-tab`).
  - (4) **`DISABLE_MAGIC_FUNCTIONS=true`**: necessário em alguns terminais quando paste de URL ou texto com aspas quebra (bracketed-paste-magic). Sintoma: paste lento ou caracteres extras. Solução documentada: adicionar `DISABLE_MAGIC_FUNCTIONS="true"` antes de source OMZ.
  - (5) **NVM/SDKMan em `.zshrc`** carregam função pesada na inicialização → shell lento. Padrões pra mitigar: lazy-load (carrega NVM só ao chamar `node` pela primeira vez).
- **Em inglês:** plugin manager, source (`source ~/.zshrc` — "source the file"), framework de shell (shell framework), customização (customization), atalho (shortcut), atualizar (update), conflito de plugins (plugin conflict), tema (theme), prompt.
- **Veja também:**
  - `[[02 - Zsh essencial]]` — `setopt`/aliases já vistos
  - `[[03 - History do Zsh]]` — plugin `history-substring-search`
  - `[[05 - Powerlevel10k]]` — theme primário (não-OMZ, sourced externamente)
  - `[[08 - Completion system (compsys)]]` — conflito `zsh-autocomplete` aprofundado
  - `[[10 - Plugins, themes e custom no OMZ]]` — escrever seu plugin
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Oh-My-Zsh|Oh-My-Zsh]]`, `[[Dicionário do Terminal#Plugin (OMZ)|plugin]]`, `[[Dicionário do Terminal#Zsh-autosuggestions|zsh-autosuggestions]]`, `[[Dicionário do Terminal#Zsh-syntax-highlighting|zsh-syntax-highlighting]]`
- **Referências:** Oh-My-Zsh wiki, plugin list, awesome-zsh-plugins, repos zsh-users/.

Tamanho-alvo: 400-500 linhas.

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Oh-My-Zsh
Framework de config pra Zsh: clonado em `~/.oh-my-zsh/`, sourced no `.zshrc`, fornece um loader de plugins (`plugins=(...)`) + 300+ plugins embarcados + 150+ temas. Não substitui o Zsh — é overlay. Pasta `custom/` é o terreno do usuário (plugins/themes próprios, overrides).

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]], [[10 - Plugins, themes e custom no OMZ]].

### Plugin (OMZ)
Unidade de funcionalidade para Oh-My-Zsh: pasta com `<nome>.plugin.zsh` em `~/.oh-my-zsh/plugins/<nome>/` (embarcado) ou `~/.oh-my-zsh/custom/plugins/<nome>/` (custom). Carregado adicionando `<nome>` ao array `plugins=(...)` no `.zshrc`. Pode trazer aliases, funções e completion (`_<comando>`).

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]], [[10 - Plugins, themes e custom no OMZ]].

### Zsh-autosuggestions
Plugin (`zsh-users/zsh-autosuggestions`) que sugere comandos enquanto você digita, em cinza inline, baseado no history. Aceitar com `→` (right-arrow) ou `Ctrl-F`. Frequentemente usado junto com history extended + `Ctrl-R`.

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]], [[03 - History do Zsh]].

### Zsh-syntax-highlighting
Plugin (`zsh-users/zsh-syntax-highlighting`) que colore comandos enquanto você digita: verde se válido, vermelho se inválido, amarelo pra aliases, azul pra paths. Alternativa mais rápida: `fast-syntax-highlighting`. **Regra crítica:** deve ser o último plugin no array `plugins=(...)` — senão perde highlight de comandos adicionados por plugins posteriores.

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/04 - Oh-My-Zsh — anatomia e plugins essenciais.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/04 - Oh-My-Zsh — anatomia e plugins essenciais.md"
grep -E "^### (Oh-My-Zsh|Plugin \(OMZ\)|Zsh-autosuggestions|Zsh-syntax-highlighting)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥8 wikilinks, 4 verbetes novos visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/04 - Oh-My-Zsh — anatomia e plugins essenciais.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 04 — Oh-My-Zsh anatomia e plugins"
```

---

## ✅ Checkpoint Iniciado

Após Task 6, a fase Iniciado está completa. Verificar:

```bash
ls -1 "03-Dominios/Terminal/Shell/" | sort
git log --oneline | head -7
```

Expected: 4 notas + `index.md`. Últimos 6 commits são do galho (MOC + Dicionário esqueleto + 4 notas).

Pausa pra revisão humana se executando em modo subagent-driven (ler 1-2 notas amostradas, confirmar tom e qualidade antes de seguir).

---

## Task 7: Nota 05 — Powerlevel10k

**Files:**
- Create: `03-Dominios/Terminal/Shell/05 - Powerlevel10k.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Powerlevel10k, Prompt, Instant prompt, Transient prompt, Nerdfont)

**Conteúdo-chave do spec (§5, Adepto):**

> Instalação canônica (`git clone ~/powerlevel10k`). Instant prompt (off/quiet/verbose). `p10k configure` wizard. Estrutura do `.p10k.zsh`. Modos visuais (rainbow, lean, classic, pure). Segmentos left/right. Customização. Transient prompt. Nerdfont. Troubleshooting (`p10k diagnose`). Armadilha: P10k congelado em 2024-07 (Roman saiu da Google).

**Verbetes referenciados:** Powerlevel10k, Prompt, Instant prompt, Transient prompt, Nerdfont.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://github.com/romkatv/powerlevel10k
WebFetch: https://github.com/romkatv/powerlevel10k#configuration
WebFetch: https://starship.rs/
WebFetch: https://github.com/sindresorhus/pure
```

Capturar: README do P10k (seções configuration, fonts, performance), informação sobre status do projeto (issues recentes, mensagens de Roman), alternativas (starship, pure).

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Powerlevel10k"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - powerlevel10k
  - prompt
aliases:
  - Powerlevel10k
  - P10k
---
```

- [ ] **Step 3: Escrever a nota completa**

Esta é uma nota Adepto densa — usar sub-headings em "O que é / Como funciona" e "Na prática" (Instalação, Instant prompt, Wizard, Segmentos, Estilos, Troubleshooting).

**Cobrir obrigatoriamente:**

- **TL;DR:** "Powerlevel10k é um theme externo pra Zsh com prompt rico (status git, tempo de comando, exit code, etc.) e o famoso `instant prompt`. Configurado pelo wizard `p10k configure` ou editando `~/.p10k.zsh`. Em modo manutenção desde 2024 (autor saiu da Google), mas plugin segue funcional."
- **O que é / Como funciona:**

  ### Instalação canônica

  P10k é instalado via `git clone` direto em `~/powerlevel10k/` (não dentro de OMZ themes) e sourced explicitamente no `.zshrc`:

  ```zsh
  # Clone (uma vez)
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k

  # No .zshrc, source no final (depois de OMZ)
  source ~/powerlevel10k/powerlevel10k.zsh-theme

  # Wizard cria ~/.p10k.zsh
  [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
  ```

  Alternativa via OMZ theme (`ZSH_THEME="powerlevel10k/powerlevel10k"`) existe mas é menos flexível.

  ### Instant prompt

  Mecanismo que cacheia o prompt rendered e mostra ANTES de o `.zshrc` terminar de carregar (acelera startup percebido). Bloco DEVE ficar no topo do `.zshrc`:

  ```zsh
  # No início do .zshrc
  if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
  fi
  ```

  Valores de `POWERLEVEL9K_INSTANT_PROMPT`:
  - `verbose` (default) — avisa se algo no `.zshrc` produz output antes do prompt
  - `quiet` — usa instant prompt mas não avisa
  - `off` — desliga (use quando init produz output legítimo que deve aparecer antes do prompt)

  ### Wizard `p10k configure`

  Roda interativamente. Sequência (resumo):
  1. Charset: Unicode? Nerd Font v3?
  2. Style: rainbow (background colorido), lean (minimalista), classic, pure
  3. Time format: 12h / 24h / nenhum
  4. Separators: angled / vertical / slanted
  5. Heads / tails: sharp / flat / blurred
  6. Lines: 1 ou 2
  7. Prompt frame, spacing, icons
  8. Transient prompt: same-dir / always / off

  Output: `~/.p10k.zsh` (~1800 linhas comentadas).

  ### Estrutura do `~/.p10k.zsh`

  - Header: gerado pelo wizard, contém data + preset base usado
  - `POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(...)` — segmentos da esquerda (dir, vcs, prompt_char, …)
  - `POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(...)` — segmentos da direita (status, command_execution_time, time, …)
  - Por segmento: cores (`POWERLEVEL9K_<SEG>_BACKGROUND/FOREGROUND`), visibilidade condicional, separadores
  - Funções custom `prompt_<nome>` quando precisa de segmento próprio

  ### Modos visuais

  | Modo | Característica |
  |---|---|
  | **rainbow** | Backgrounds coloridos por segmento, máxima distinção visual |
  | **lean** | Sem backgrounds, texto colorido apenas |
  | **classic** | Único background neutro, texto colorido |
  | **pure** | Imita o tema `pure` (Sindresorhus) — minimal e silencioso |

  ### Transient prompt

  Quando você executa um comando, o prompt anterior pode "encolher" pra liberar espaço. Controlado por `POWERLEVEL9K_TRANSIENT_PROMPT`:
  - `same-dir` — encolhe se próximo prompt no mesmo dir
  - `always` — sempre encolhe
  - `off` — nunca (default)

  Útil em sessões longas — reduz scroll noise.

  ### Nerdfont

  Fonts patched com glyphs adicionais (ícones de branch, Linux distros, dev tools). P10k recomenda **MesloLGS NF** (já patch'd, fornecido pelo P10k). Instalar a font no SO + configurar terminal pra usá-la. Sem nerdfont, P10k mostra `□` ou `?` no lugar de ícones.

- **Na prática:**
  - **Editar segmento (exemplo: mudar cor do dir):** localize `POWERLEVEL9K_DIR_BACKGROUND` em `~/.p10k.zsh`, mude o número (0-255 ANSI 256-color), `source ~/.p10k.zsh` ou abra novo shell.
  - **Adicionar segmento custom:** function `prompt_<nome>` + adicionar `<nome>` ao array de elements.
  - **Trocar de modo sem rodar wizard:** `p10k configure` é o caminho oficial; alternativa é editar a constante de preset no top do `~/.p10k.zsh` ou simplesmente rodar wizard.
  - **Troubleshooting prompt lento:** `p10k diagnose` (gera reportório + dica). Causas comuns: comando lento dentro de segmento custom (e.g., `npm version` em cada prompt).
  - **Trocar font no terminal:** depende do terminal — em GNOME Terminal vai em Preferences → Profile → Custom Font.
- **Armadilhas:**
  - (1) **P10k congelado em 2024-07**: último release pelo autor original; projeto mantido por contributors apenas pra fixes críticos. Plugin segue funcional, mas não evolui. Se quer prompt em evolução ativa, considere **Starship** (cross-shell, Rust) ou **Pure** (mínimo).
  - (2) **`INSTANT_PROMPT=verbose` reclama de output no init**: comum quando NVM/SDKMan/etc. printam mensagens durante carregamento. Soluções: (a) mover essas linhas pra ANTES do bloco de instant prompt; (b) silenciar a fonte; (c) `INSTANT_PROMPT=off` (não recomendado — perde a UX).
  - (3) **Nerdfont não configurada**: ícones viram `□`. Fix: instalar MesloLGS NF, apontar o terminal pra ela.
  - (4) **`POWERLEVEL9K_TRANSIENT_PROMPT=always` confunde scroll-back**: prompts antigos perdem info ao retroceder. Use `same-dir` se quer experimentar sem perder histórico visual.
  - (5) **Migrar tema dentro do OMZ** (`ZSH_THEME="powerlevel10k/powerlevel10k"`) vs source externo: misturar (declarar tema E sourcear externamente) pode duplicar carregamento. Decidir um e remover o outro.
- **Em inglês:** prompt, instant prompt, transient prompt, theme, segmento (segment), font patched, ícone (icon), Unicode, glyph, atalho visual (visual shortcut), customização (customization).
- **Veja também:**
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]` — OMZ vs theme externo
  - `[[10 - Plugins, themes e custom no OMZ]]` — escrever theme próprio
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Powerlevel10k|Powerlevel10k]]`, `[[Dicionário do Terminal#Prompt|prompt]]`, `[[Dicionário do Terminal#Instant prompt|instant prompt]]`, `[[Dicionário do Terminal#Transient prompt|transient prompt]]`, `[[Dicionário do Terminal#Nerdfont|nerdfont]]`
- **Referências:** P10k README, P10k configuration section, Starship, Pure.

Tamanho-alvo: 450-550 linhas.

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Instant prompt
Mecanismo do Powerlevel10k que cacheia o prompt renderizado e o exibe ANTES de `~/.zshrc` terminar de carregar. Acelera startup percebido. Configurado por `POWERLEVEL9K_INSTANT_PROMPT` (`verbose`/`quiet`/`off`). O bloco do instant prompt deve ficar no TOPO do `.zshrc`.

Veja também: [[05 - Powerlevel10k]].

### Nerdfont
Família de fonts patched (Nerd Fonts) com glyphs adicionais — ícones de Git, Linux distros, dev tools, devicons. Powerlevel10k recomenda **MesloLGS NF**. Sem nerdfont configurada no terminal, ícones do prompt aparecem como `□` ou `?`.

Veja também: [[05 - Powerlevel10k]].

### Powerlevel10k
Theme externo pra Zsh por Roman Perepelitsa (romkatv/powerlevel10k). Oferece prompt rico configurável (status git, exit code, tempo de comando), `instant prompt` pra startup rápido, wizard `p10k configure`. Em modo manutenção desde 2024-07 — funcional, mas não evolui ativamente.

Veja também: [[05 - Powerlevel10k]].

### Prompt
Texto exibido pelo shell antes de aceitar comando, configurado pelas variáveis `PROMPT` (left) e `RPROMPT` (right). Suporta sequências de escape (`%n` user, `%~` cwd, `%F{color}` cor). Themes (Powerlevel10k, Starship, Pure) substituem `PROMPT` com lógica rica.

Veja também: [[05 - Powerlevel10k]], [[10 - Plugins, themes e custom no OMZ]].

### Transient prompt
Recurso do Powerlevel10k que "encolhe" prompts antigos quando você executa novos comandos, liberando espaço visual. Configurado por `POWERLEVEL9K_TRANSIENT_PROMPT` (`same-dir`/`always`/`off`).

Veja também: [[05 - Powerlevel10k]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/05 - Powerlevel10k.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/05 - Powerlevel10k.md"
grep -E "^### (Powerlevel10k|Prompt|Instant prompt|Transient prompt|Nerdfont)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥8 wikilinks, 5 verbetes novos.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/05 - Powerlevel10k.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 05 — Powerlevel10k"
```

---

## Task 8: Nota 06 — Keybindings práticos

**Files:**
- Create: `03-Dominios/Terminal/Shell/06 - Keybindings práticos.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Bindkey, Widget; expansão de Keymap)

**Conteúdo-chave do spec (§5, Adepto):**

> `bindkey` (listar, definir, remover). Modo emacs (default) vs vi (`bindkey -e`/`-v`). Keymaps por modo (`main`, `viins`, `vicmd`, `emacs`, `command`). Descobrir código de tecla (`cat -v`, `Ctrl-V`). Fix de Home/End/Ctrl-Arrows. Bindings úteis (history-substring-search, sudo-toggle, edit-command-line).

**Verbetes referenciados:** Bindkey, Widget; **expansão** de Keymap (adicionar sub-sessão Zsh).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html
WebFetch: https://github.com/zsh-users/zsh-history-substring-search
```

Capturar: sintaxe completa de `bindkey`, lista de keymaps, exemplos de fix Home/End.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Keybindings práticos"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - keybindings
  - zle
aliases:
  - Keybindings práticos
  - Bindkey
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "`bindkey` mapeia sequências de tecla a widgets do ZLE. Modo emacs (default) ou vi. Setup comum: fix de Home/End/Ctrl-Arrows pra funcionar no seu terminal. Combine com plugins (history-substring-search, edit-command-line) pra ganhos imediatos."
- **O que é / Como funciona:**
  - `bindkey` é o builtin que registra binding. Sem ele, Zsh tem só os defaults da emacs-mode (ou vi-mode).
  - **Comandos básicos:**
    - `bindkey` — lista TODOS os bindings ativos
    - `bindkey '<seq>'` — mostra widget bound para `<seq>`
    - `bindkey '<seq>' <widget>` — define binding
    - `bindkey -r '<seq>'` — remove binding
    - `bindkey -l` — lista keymaps disponíveis
    - `bindkey -M <keymap> '<seq>' <widget>` — binda em keymap específico
  - **Modo emacs vs vi:**
    - Default: emacs-mode (`bindkey -e`) — atalhos GNU Readline (Ctrl-A, Ctrl-E, etc.)
    - Vi-mode: `bindkey -v` — comandos vim no shell (i/Esc, modo normal/insert)
  - **Keymaps (lista):**
    - `main` — alias pro keymap default (`emacs` ou `viins`)
    - `emacs` — atalhos emacs
    - `viins` — modo insert do vi
    - `vicmd` — modo normal do vi
    - `command` — para `:` em modo vi (raramente customizado)
  - **Descobrir código de tecla**:
    - `cat -v` + apertar a tecla → mostra escape sequence (e.g., `^[[H` pra Home)
    - `Ctrl-V` no Zsh + tecla → insere literal a sequência no shell
    - Plugin `bindkey` de OMZ lista mapeamentos comuns
- **Na prática:**
  - **Fix de Home/End (frequente em terminais Linux):**
    ```zsh
    bindkey '^[[H' beginning-of-line   # Home
    bindkey '^[[F' end-of-line         # End
    ```
  - **Ctrl-Arrows (mover por palavra):**
    ```zsh
    bindkey '^[[1;5C' forward-word     # Ctrl-Right
    bindkey '^[[1;5D' backward-word    # Ctrl-Left
    ```
  - **Ctrl-Delete / Ctrl-Backspace (deletar palavra):**
    ```zsh
    bindkey '^[[3;5~' kill-word         # Ctrl-Delete
    bindkey '^H' backward-kill-word     # Ctrl-Backspace (alguns terminais)
    ```
  - **History-substring-search (após install do plugin):**
    ```zsh
    bindkey '^[[A' history-substring-search-up      # Up
    bindkey '^[[B' history-substring-search-down    # Down
    ```
  - **Sudo-toggle (OMZ plugin `sudo`):**
    ```zsh
    # Após `plugins=(... sudo)`: Esc-Esc adiciona `sudo` ao início do comando
    bindkey '\e\e' sudo-command-line
    ```
  - **Editar comando longo no $EDITOR (built-in):**
    ```zsh
    autoload -U edit-command-line
    zle -N edit-command-line
    bindkey '^X^E' edit-command-line    # Ctrl-X Ctrl-E
    ```
  - **Trocar pra vi-mode:**
    ```zsh
    bindkey -v
    # Adicionar indicador visual no prompt (function que detecta keymap atual)
    # Cf. zsh-vim-mode plugin pra setup completo
    ```
- **Armadilhas:**
  - (1) **Binding feito em `~/.zshrc` antes de OMZ load**: OMZ pode resetar keymap depois → seu binding some. Solução: bindings no FINAL do `.zshrc`, depois de source OMZ + plugins.
  - (2) **Escape sequences diferem por terminal**: Home/End varia entre GNOME Terminal, iTerm2, Alacritty, tmux/Zellij dentro de SSH. Quando portar config pra outra máquina, re-descobrir sequências com `cat -v`.
  - (3) **`stty -ixon` esquecido**: sem isso, `Ctrl-S` (forward-search) é capturado pelo terminal (flow control). Adicionar `stty -ixon` no `.zshrc`.
  - (4) **Vi-mode sem indicador visual**: muda de modo silenciosamente, fácil errar. Plugin `zsh-vim-mode` ou função custom em `zle-keymap-select` resolve.
- **Em inglês:** atalho de teclado (keybinding), tecla (key), sequência de escape (escape sequence), keymap, modo emacs (emacs mode), modo vi (vi mode), tecla modificadora (modifier key), descobrir sequência (find sequence), bindar tecla (bind a key).
- **Veja também:**
  - `[[07 - ZLE]]` — sistema por trás dos widgets
  - `[[08 - Completion system (compsys)]]` — Tab e completion-related bindings
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]` — plugins com bindings (sudo, history-substring-search)
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Bindkey|bindkey]]`, `[[Dicionário do Terminal#Widget|widget]]`, `[[Dicionário do Terminal#Keymap|keymap]]`
- **Referências:** Zsh manual — Zsh Line Editor, bindkey, zsh-history-substring-search README.

Tamanho-alvo: 350-450 linhas.

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Bindkey
Builtin do Zsh que mapeia sequências de tecla a widgets do ZLE. Sintaxe: `bindkey '<seq>' <widget>` (define), `bindkey -r '<seq>'` (remove), `bindkey -M <keymap> ...` (em keymap específico). Aceita modo emacs (`bindkey -e`, default) ou vi (`bindkey -v`).

Veja também: [[06 - Keybindings práticos]], [[07 - ZLE]].

### Widget
Função registrada no ZLE (`zle -N <name>`) que pode ser bindada a uma sequência de tecla via `bindkey`. Widgets builtin: `self-insert`, `beginning-of-line`, `backward-kill-word`, `history-incremental-search-backward`. Custom: função Zsh + `zle -N`.

Veja também: [[06 - Keybindings práticos]], [[07 - ZLE]].
```

**Expandir verbete existente "Keymap"** — adicionar sub-sessão "Em Zsh (ZLE)" mantendo o conteúdo Neovim atual:

```markdown
### Keymap
**Em Neovim:** mapeamento de uma sequência de teclas pra uma ação. Em Neovim moderno: `vim.keymap.set(mode, lhs, rhs, opts)`. Opções comuns: `desc` (descrição visível em which-key), `silent`, `noremap` (default true em vim.keymap.set).

**Em Zsh (ZLE):** conjunto nomeado de bindings de tecla → widget. Keymaps disponíveis: `main` (alias do default), `emacs`, `viins` (vi insert), `vicmd` (vi normal), `command` (vi `:`). Selecionado por `bindkey -e` (emacs, default) ou `bindkey -v` (vi). Binding em keymap específico: `bindkey -M vicmd '<seq>' <widget>`.

Veja também: [[06 - Estrutura de config]], [[06 - Keybindings práticos]].
```

(Use `Edit` no arquivo do dicionário pra substituir o verbete existente — `old_string` = todo o bloco atual de Keymap, `new_string` = bloco expandido acima.)

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/06 - Keybindings práticos.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/06 - Keybindings práticos.md"
grep -E "^### (Bindkey|Widget)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
grep -A 3 "^### Keymap$" "03-Dominios/Terminal/Dicionário do Terminal.md" | grep -E "(Neovim|Zsh)"
```

Expected: arquivo existe, ≥7 wikilinks, 2 verbetes novos, Keymap mostra ambas as sub-sessões.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/06 - Keybindings práticos.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 06 — Keybindings práticos (Keymap expandido)"
```

---

## Task 9: Nota 07 — ZLE

**Files:**
- Create: `03-Dominios/Terminal/Shell/07 - ZLE.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: ZLE)

**Conteúdo-chave do spec (§5, Adepto):**

> ZLE = editor de linha do Zsh. Modelo (input → widget → buffer). Widgets builtin (categorias). `BUFFER`, `CURSOR`, `LBUFFER`, `RBUFFER`. Criar widget custom (`zle -N`). Exemplos concretos (expand-or-complete-with-dots; widget escapando ao Esc). Hooks (`zle-line-init`, `zle-keymap-select`, `zle-line-finish`). Relação com bindkey.

**Verbetes referenciados:** ZLE (widget já criado em Task 8).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#Widgets
WebFetch: https://github.com/softmoth/zsh-vim-mode
```

Capturar: categorias de widgets builtin, variáveis especiais (BUFFER etc.), exemplos canônicos de widget custom.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "ZLE"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - zle
  - widgets
aliases:
  - ZLE
  - Zsh Line Editor
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "ZLE (Zsh Line Editor) é o editor de linha do Zsh — o motor que interpreta cada tecla, mantém um buffer e dispatcha widgets (ações). Tudo que `bindkey` mapeia, ZLE executa. Escrever widget próprio é como criar comando do editor sob medida."
- **O que é / Como funciona:**
  - **Modelo:**
    - Input (tecla pressionada) → keymap atual lookup → widget associado → widget muda o buffer → display atualiza
    - O "buffer" é o texto que você está editando antes de pressionar Enter
  - **Categorias de widgets builtin:**
    - Inserção: `self-insert` (cada char), `accept-line` (Enter)
    - Movimentação: `beginning-of-line`, `end-of-line`, `forward-word`, `backward-word`
    - Edição: `delete-char`, `backward-delete-char`, `kill-word`, `kill-line`, `transpose-chars`
    - History: `up-history`, `down-history`, `history-incremental-search-backward`
    - Buffer: `clear-screen`, `push-line`, `pop-line`, `quoted-insert`
    - Completion: `expand-or-complete`, `_complete`, `complete-word`
  - **Variáveis especiais (acessíveis em widget custom):**
    - `BUFFER` — todo o texto do buffer
    - `LBUFFER` — texto à esquerda do cursor
    - `RBUFFER` — texto à direita
    - `CURSOR` — posição do cursor (numérica, 0-indexed)
    - `KEYS` — sequência de tecla que disparou o widget
    - `WIDGET` — nome do widget atual (útil em widgets que se referenciam)
  - **Criar widget custom:**
    1. Definir função Zsh: `my-widget() { ... }`
    2. Registrar: `zle -N my-widget`
    3. Bindar: `bindkey '<seq>' my-widget`
  - **Hooks ZLE** (widgets especiais disparados em eventos):
    - `zle-line-init` — chamado ao começar nova linha (útil pra reset de estado)
    - `zle-keymap-select` — chamado ao trocar de keymap (vi mode change)
    - `zle-line-finish` — chamado ao Enter (antes de exec)
    - Usar: `zle -N zle-line-init my-init-function`
- **Na prática:**
  - **Widget 1: expand-or-complete-with-dots** (mostra "..." enquanto completion processa):
    ```zsh
    expand-or-complete-with-dots() {
      echo -n "\e[31m...\e[0m"     # imprime "..." vermelho
      zle expand-or-complete       # dispara completion normal
      zle redisplay                # redesenha (limpa o "...")
    }
    zle -N expand-or-complete-with-dots
    bindkey '^I' expand-or-complete-with-dots   # Tab
    ```
  - **Widget 2: insert-sudo** (toggle `sudo` no início do buffer):
    ```zsh
    insert-sudo() {
      if [[ $BUFFER == sudo\ * ]]; then
        BUFFER="${BUFFER#sudo }"
      else
        BUFFER="sudo $BUFFER"
        CURSOR=$((CURSOR + 5))
      fi
    }
    zle -N insert-sudo
    bindkey '\e\e' insert-sudo
    ```
  - **Widget 3: clear-and-history** (limpa tela e mostra last 10 commands):
    ```zsh
    clear-and-history() {
      clear
      print -l ${(@)history[1,10]}
      zle reset-prompt
    }
    zle -N clear-and-history
    bindkey '^X^H' clear-and-history
    ```
  - **Hook: indicador de modo vi no prompt:**
    ```zsh
    function zle-keymap-select {
      case $KEYMAP in
        vicmd) PROMPT="[N] $PROMPT" ;;
        main|viins) PROMPT="[I] $PROMPT" ;;
      esac
      zle reset-prompt
    }
    zle -N zle-keymap-select
    ```
- **Armadilhas:**
  - (1) **Esqueceu `zle -N` antes de bindkey**: `bindkey '<seq>' minha-func` falha silenciosamente se `minha-func` não foi registrada como widget. Sintoma: tecla não faz nada. Solução: `zle -N minha-func` antes.
  - (2) **`zle reset-prompt` em hook errado** pode causar redraws infinitos. Use só em `zle-line-init` ou eventos discretos (não em `self-insert`).
  - (3) **Alterar `BUFFER` em widget de inserção** rompe completion (que assume buffer estável). Faça mods em widgets explícitos chamados pelo usuário, não em hooks de inserção.
  - (4) **Mistura de `vim.keymap.set` (Neovim) e `bindkey` (Zsh) na cabeça**: a sintaxe é diferente; em Zsh sempre `bindkey -M <keymap>` pra escolher escopo, em Neovim `vim.keymap.set` aceita arrays de modos.
- **Em inglês:** widget, buffer, cursor position, line editor, dispatch (de comando), gancho (hook), evento (event), re-renderizar (redisplay), redefinir prompt (reset prompt).
- **Veja também:**
  - `[[06 - Keybindings práticos]]` — onde widgets viram bindings
  - `[[08 - Completion system (compsys)]]` — completion é categoria de widget
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#ZLE|ZLE]]`, `[[Dicionário do Terminal#Widget|widget]]`
- **Referências:** Zsh manual — Zsh Line Editor (completo), Widgets, zsh-vim-mode README.

Tamanho-alvo: 350-450 linhas.

- [ ] **Step 4: Adicionar verbete ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### ZLE
Zsh Line Editor — o editor de linha embutido no Zsh, responsável por receber teclas, manter o buffer da linha sendo editada, e dispatchar widgets (ações). Tudo que `bindkey` mapeia é executado pelo ZLE. Hooks: `zle-line-init`, `zle-keymap-select`, `zle-line-finish`.

Veja também: [[06 - Keybindings práticos]], [[07 - ZLE]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/07 - ZLE.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/07 - ZLE.md"
grep -E "^### ZLE$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥6 wikilinks, verbete ZLE visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/07 - ZLE.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 07 — ZLE"
```

---

## Task 10: Nota 08 — Completion system (compsys)

**Files:**
- Create: `03-Dominios/Terminal/Shell/08 - Completion system (compsys).md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Compsys, Compinit, Compdef, Fpath, Zstyle)

**Conteúdo-chave do spec (§5, Adepto):**

> Modelo (compsys, widgets de completion). `compinit` (init, fpath, gera `~/.zcompdump`). `compdef`. `fpath`. Como Zsh decide o que completar. `zstyle` essenciais (matcher, menu select, format, group-name). Troubleshooting (`compaudit`, rebuild de zcompdump). Conflitos `zsh-autocomplete`, `fzf-tab`.

**Verbetes referenciados:** Compsys, Compinit, Compdef, Fpath, Zstyle.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Completion-System.html
WebFetch: https://github.com/Aloxaf/fzf-tab
```

Capturar: arquitetura do compsys (compinit, compdef, fpath), exemplos de zstyle, README do fzf-tab.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Completion system (compsys)"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - compsys
  - completion
aliases:
  - Compsys
  - Completion system
---
```

- [ ] **Step 3: Escrever a nota completa**

Esta é a nota mais densa do galho. Use sub-headings em "O que é / Como funciona" e "Na prática".

**Cobrir obrigatoriamente:**

- **TL;DR:** "Compsys é o sistema de completion programável do Zsh. `compinit` inicializa, lê `fpath` pra encontrar funções `_<comando>`, e gera `~/.zcompdump` (cache). `compdef` registra função pra comando. `zstyle` customiza apresentação. Quando completion 'não funciona': geralmente é `.zcompdump` velho ou fpath errado."
- **O que é / Como funciona:**

  ### Modelo

  - Completion = "Tab autocompleta comando, argumento, path, …"
  - Sistema programável: cada comando pode ter função `_<comando>` que diz "como completar" — argumentos esperados, sub-comandos, flags válidas
  - Funções vivem em arquivos no `fpath` (search path de funções), nomes começando com `_`
  - Ao primeiro Tab num comando, Zsh autoload da função e executa

  ### `compinit`

  Builtin que inicializa o compsys:
  - Lê `fpath`, indexa funções `_<*>`
  - Gera/atualiza `~/.zcompdump` (cache binário compilado)
  - Roda em modo "security check" por default (verifica permissões dos dirs em fpath)

  Setup canônico (já feito por OMZ; documentar pra contexto):
  ```zsh
  autoload -Uz compinit
  compinit
  ```

  Variações:
  - `compinit -i` — ignora arquivos inseguros (não fail)
  - `compinit -C` — pula security check (mais rápido, menos seguro)
  - `compinit -d <path>` — alternativa ao `~/.zcompdump` default

  ### `compdef`

  Registra função de completion pra um comando:
  ```zsh
  compdef _git mygit              # mygit completa como git
  compdef '_files -g "*.log"' tail # tail completa só .log
  ```

  Útil pra binários novos que não trazem completion, ou aliases que precisam de completion específica.

  ### `fpath`

  Array com diretórios onde Zsh procura funções autoload (incluindo `_<comando>`). OMZ adiciona `$ZSH/plugins/*/` e `$ZSH/completions/` ao fpath.

  ```zsh
  # Ver fpath
  print -l $fpath

  # Adicionar custom completion
  fpath=(~/.zsh-custom-completions $fpath)
  autoload -Uz compinit && compinit
  ```

  ### Como Zsh decide o que completar

  1. Você digita `git ch<Tab>`
  2. ZLE dispatchá widget `expand-or-complete`
  3. Widget chama compsys, que parseia o command-line: comando = `git`, argumento atual = `ch`
  4. Compsys busca `_git` no fpath, carrega
  5. `_git` define: "primeiro arg de `git` é sub-comando, lista X opções"
  6. Compsys filtra opções que começam com `ch` (case insensitive se zstyle assim)
  7. Mostra menu ou completa direto

  ### `zstyle` — customização

  `zstyle '<context>' '<style>' '<value>'` — controla aspectos do compsys (e de outros sistemas Zsh).

  Configs essenciais:
  ```zsh
  # Case-insensitive (m: minúscula casa com Minúscula/Maiúscula)
  zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

  # Menu navegável com setas (sem isso, Tab só lista)
  zstyle ':completion:*' menu select

  # Cabeçalho indicando o que está completando
  zstyle ':completion:*' format 'Completing %d'

  # Agrupar matches por tipo (commands, options, files)
  zstyle ':completion:*' group-name ''

  # Cores no menu (precisa LS_COLORS exportado)
  zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

  # Não dar match a comandos ocultos por default
  zstyle ':completion:*:functions' ignored-patterns '_*'
  ```
- **Na prática:**

  ### Setup mínimo manual (sem OMZ)

  ```zsh
  autoload -Uz compinit
  compinit
  zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
  zstyle ':completion:*' menu select
  ```

  ### Troubleshooting

  **Completion para um comando "sumiu":**
  - `which _<comando>` — verifica se função existe
  - `whence -v <comando>` — mostra origem
  - `compaudit` — lista dirs com permissões suspeitas em fpath

  **`.zcompdump` corrompido (mudança de plugins, atualização):**
  ```bash
  rm ~/.zcompdump*
  compinit
  ```

  **`compinit` lento na startup:**
  - `zsh -i -c exit` (mede tempo total de startup)
  - `compinit -C` — pula security check (ganha ~200ms; aceitar tradeoff)
  - Plugin `zsh-defer` pra adiar compinit pós-prompt

  **`compaudit` reclamando de permissões:**
  ```bash
  compaudit | xargs chmod g-w,o-w
  ```

  ### Plugins que mexem em completion

  - **fzf-tab** (Aloxaf/fzf-tab): substitui o menu builtin por fzf — UX moderna. Source ANTES de syntax-highlighting. Compatível com `compsys` default.
  - **zsh-autocomplete** (marlonrichert): mostra sugestões enquanto digita, sem Tab. **Sobrepõe** o fluxo default — incompatível com `fzf-tab` simultâneo; modifica zstyle agressivamente.
- **Armadilhas:**
  - (1) **`.zcompdump` órfão**: instala plugin novo, completion não aparece. Causa: cache do compinit. Sintoma: `_<comando>` existe no fpath mas Tab não faz nada. Solução: `rm ~/.zcompdump* && compinit`.
  - (2) **Fpath ordem importa**: dois plugins com `_<comando>` competem; o que carregou primeiro vence (entra primeiro no fpath). Verifique com `print -l $fpath`.
  - (3) **`compaudit` no install novo de OMZ**: dirs criados com permissões 755 (group-writable) disparam erro. Fix: `compaudit | xargs chmod g-w`.
  - (4) **`compinit` rodando 2 vezes**: OMZ roda no source dele; se você adicionar `compinit` no `.zshrc` depois, runs duplicados degradam startup. Não chame `compinit` manualmente se já usa OMZ.
  - (5) **`zsh-autocomplete` + OMZ completion default**: o plugin redefine vários zstyles e widgets de completion. Não roda bem ao lado de `fzf-tab`. Decidir uma estratégia (default OMZ, fzf-tab, ou zsh-autocomplete) e remover as concorrentes do `.zshrc`.
- **Em inglês:** completar (complete), sistema de completion (completion system), inicializar (initialize), função de completion (completion function), arquivo de cache (cache file), reconstruir (rebuild), permissão insegura (insecure permission), match (match), agrupar (group).
- **Veja também:**
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]` — OMZ já chama `compinit`
  - `[[06 - Keybindings práticos]]` — Tab é binding
  - `[[07 - ZLE]]` — widgets de completion vivem aqui
  - `[[10 - Plugins, themes e custom no OMZ]]` — escrever `_<comando>` próprio
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Compsys|compsys]]`, `[[Dicionário do Terminal#Compinit|compinit]]`, `[[Dicionário do Terminal#Compdef|compdef]]`, `[[Dicionário do Terminal#Fpath|fpath]]`, `[[Dicionário do Terminal#Zstyle|zstyle]]`
- **Referências:** Zsh manual — Completion System, Completion Widgets, fzf-tab README, zsh-autocomplete README.

Tamanho-alvo: 500-600 linhas. Aceitar essa densidade — compsys é uma coisa só, dividir confunde.

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Compdef
Builtin do Zsh (`compdef <function> <command>`) que registra uma função de completion para um comando. Exemplo: `compdef _git mygit` faz `mygit` completar com a lógica de `_git`. Útil pra binários sem completion própria ou aliases.

Veja também: [[08 - Completion system (compsys)]].

### Compinit
Builtin do Zsh que inicializa o completion system. Lê `fpath`, indexa funções `_<comando>`, gera `~/.zcompdump` (cache compilado). Setup canônico: `autoload -Uz compinit && compinit`. Variações: `-i` (ignora arquivos inseguros), `-C` (pula security check, mais rápido).

Veja também: [[08 - Completion system (compsys)]].

### Compsys
Sistema de completion programável do Zsh. Cada comando pode ter função `_<comando>` no `fpath` que define como completar. Inicializado por `compinit`; customizado por `zstyle`; troubleshooting com `compaudit`.

Veja também: [[08 - Completion system (compsys)]].

### Fpath
Array com diretórios onde Zsh procura funções autoload — incluindo funções de completion (`_<comando>`). OMZ adiciona `$ZSH/plugins/*/` e `$ZSH/completions/`. Ordem importa: primeiro no fpath, primeiro encontrado.

Veja também: [[08 - Completion system (compsys)]].

### Zstyle
Builtin do Zsh que customiza estilos de subsistemas (completion, prompts, vcs_info, etc.). Sintaxe: `zstyle '<context>' '<style>' '<value>'`. No completion: `zstyle ':completion:*' menu select` ativa menu navegável; `matcher-list 'm:{a-z}={A-Za-z}'` ativa case-insensitive.

Veja também: [[08 - Completion system (compsys)]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/08 - Completion system (compsys).md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/08 - Completion system (compsys).md"
grep -E "^### (Compsys|Compinit|Compdef|Fpath|Zstyle)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥8 wikilinks, 5 verbetes novos.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/08 - Completion system (compsys).md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 08 — Completion system (compsys)"
```

---

## ✅ Checkpoint Adepto

Após Task 10, a fase Adepto está completa. Verificar:

```bash
ls -1 "03-Dominios/Terminal/Shell/" | sort
git log --oneline | head -10
```

Expected: 8 notas + `index.md`. Últimos 9 commits do galho.

Pausa pra revisão humana (se subagent-driven): amostrar 1 nota Adepto (recomendo 08 - compsys, a mais densa) e validar tom + densidade técnica.

---

## Task 11: Nota 09 — Globbing avançado e parameter expansion

**Files:**
- Create: `03-Dominios/Terminal/Shell/09 - Globbing avançado e parameter expansion.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Globbing, Extended glob, Glob qualifier, Parameter expansion)

**Conteúdo-chave do spec (§5, Magus):**

> Globbing (EXTENDED_GLOB, qualifiers, patterns avançados). Parameter expansion (`${var:-default}`, `${(L)var}`, `${var//pat/repl}`, flags `(L)`, `(U)`, `(s:x:)`, `(@)`).

**Verbetes referenciados:** Globbing, Extended glob, Glob qualifier, Parameter expansion.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zsh.sourceforge.io/Doc/Release/Expansion.html#Filename-Generation
WebFetch: https://zsh.sourceforge.io/Doc/Release/Expansion.html#Parameter-Expansion
```

Capturar: tabela completa de glob qualifiers, lista completa de parameter expansion flags, exemplos canônicos.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Globbing avançado e parameter expansion"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - shell
  - zsh
  - magus
  - globbing
  - expansion
aliases:
  - Globbing
  - Parameter expansion
---
```

- [ ] **Step 3: Escrever a nota completa**

Nota densa (Magus). Use sub-headings em "O que é / Como funciona" e "Na prática" pra blocos (Globbing essencial / Extended glob / Qualifiers / Parameter expansion / Flags).

**Cobrir obrigatoriamente:**

- **TL;DR:** "Globbing avançado do Zsh substitui dezenas de `find -X` por one-liners. EXTENDED_GLOB liga negação (`^`), exclusão (`~`), e qualifiers `(.)/(/)/(N)/(L+N)/(om[N])`. Parameter expansion vai além de `${var:-default}` com flags `(L)/(U)/(s:.:)/(@)` que evitam pipe pra `sed`/`awk`. Use diariamente."
- **O que é / Como funciona:**

  ### Globbing essencial (compatível com Bash + sh)

  - `*` — zero ou mais chars (exceto `/`)
  - `?` — exatamente 1 char
  - `[abc]` — char em set
  - `[a-z]` — char em range
  - `[^abc]` — char NÃO em set
  - `**/` — recursivo (subdirs); Zsh tem nativo, Bash precisa `shopt -s globstar`

  ### Extended glob (Zsh)

  Requer `setopt EXTENDED_GLOB`.

  - `^pattern` — negação: `*^.bak` = tudo que não termina em `.bak`
  - `~pattern` — exclusão: `*.txt~README*` = .txt files exceto README.*
  - `(p1|p2)` — alternation
  - `pattern#` — zero ou mais
  - `pattern##` — um ou mais

  ### Glob qualifiers `(...)`

  Pós-fixados ao padrão; filtram por atributo do arquivo.

  | Qualifier | Match |
  |---|---|
  | `(.)` | arquivos regulares |
  | `(/)` | diretórios |
  | `(@)` | symlinks |
  | `(*)` | executáveis |
  | `(N)` | null glob (sem match = vazio, não erro) |
  | `(L+N)` | tamanho > N (bytes; `Lk`/`Lm`/`Lg` pra kB/MB/GB) |
  | `(L-N)` | tamanho < N |
  | `(mh-N)` | modificado nas últimas N horas |
  | `(mm-N)` | modificado nos últimos N minutos |
  | `(md-N)` | modificado nos últimos N dias |
  | `(om)` | ordenar por mtime (mais recente primeiro) |
  | `(Om)` | ordenar por mtime (mais antigo primeiro) |
  | `(om[N,M])` | ordenar por mtime, pegar índices N a M |
  | `(.U)` | owned by you |
  | `(.G)` | owned by your group |
  | `(F)` | non-empty dirs |

  Combinar: `(.NL+1k.om[1,5])` = arquivos regulares, não-erro-se-vazio, >1kB, 5 mais recentes.

  ### Parameter expansion essencial

  **Defaults e checks** (compatíveis com Bash):
  - `${var:-default}` — `var` se setado, senão `default`
  - `${var:+alt}` — `alt` se `var` setado, senão vazio
  - `${var:=default}` — atribui `default` se `var` não setado
  - `${var:?error}` — exit + msg se `var` não setado

  **Substring e length:**
  - `${var:offset:length}` — Bash-compat
  - `${var[start,end]}` — Zsh: indexação 1-based, end inclusivo
  - `${#var}` — comprimento da string ou array

  **Match e replace:**
  - `${var#prefix}` — remove prefix mais curto
  - `${var##prefix}` — remove prefix mais longo
  - `${var%suffix}` — remove suffix mais curto
  - `${var%%suffix}` — remove suffix mais longo
  - `${var/pat/repl}` — substitui primeira ocorrência
  - `${var//pat/repl}` — substitui todas
  - `${var/#pat/repl}` — só no início
  - `${var/%pat/repl}` — só no fim

  ### Flags Zsh `${(<flags>)var}`

  - `(L)` — lowercase: `${(L)var}`
  - `(U)` — uppercase
  - `(C)` — capitalize
  - `(s:sep:)` — split por separador (resultado: array)
  - `(j:sep:)` — join array com separador
  - `(@)` — preservar como array (não join automático)
  - `(P)` — indireção: `${(P)name}` = valor da variável cujo NOME está em `$name`
  - `(k)` — keys de hash, `(v)` — values

  Combinar: `${(j:,:)array}` = junta com vírgula; `${(s:.:)hostname}` = split por ponto.
- **Na prática:**

  ### Globbing — one-liners reais

  ```zsh
  # Os 5 logs mais antigos
  rm **/*.log(.om[-5,-1])

  # Arquivos .ts não-vazios
  print -l **/*.ts(.L+1)

  # Diretórios modificados nas últimas 24h
  print -l **/(/mh-24)

  # Arquivos > 10MB
  print -l **/*(.Lm+10)

  # Tudo em ~/Downloads exceto .iso
  ls ~/Downloads/*^*.iso

  # Sem erro se não houver match (útil em scripts)
  print -l **/*.tmp(N)
  ```

  ### Parameter expansion — one-liners reais

  ```zsh
  # Extension de um arquivo
  file="report.tar.gz"
  echo ${file##*.}            # gz

  # Basename sem extension
  echo ${file%.*}             # report.tar

  # Replace path separator
  path="a/b/c/d"
  echo ${path//\//-}          # a-b-c-d

  # Uppercase
  name="josenaldo"
  echo ${(U)name}             # JOSENALDO

  # Split hostname em array
  print -l ${(s:.:)HOST}      # cada parte em sua linha

  # Default com env
  echo ${EDITOR:-vim}         # vim se EDITOR não setado

  # Indireção (dispatch dinâmico)
  greeting="Hello"
  varname="greeting"
  echo ${(P)varname}          # Hello
  ```
- **Armadilhas:**
  - (1) **`EXTENDED_GLOB` esquecido**: `^pattern` vira erro. Sintoma: `zsh: bad pattern`. Solução: `setopt EXTENDED_GLOB` no `.zshrc`.
  - (2) **`(N)` faltando em script**: padrão sem match em script com `setopt NO_NOMATCH` aborta. `(N)` retorna vazio em vez de erro.
  - (3) **`om` order é decrescente** (mais recente primeiro); confuso quem espera ordem alfabética. Use `Om` se quiser ordem crescente, ou outro qualifier.
  - (4) **Parameter expansion em string com aspas duplas**: `"${(L)var}"` funciona; sem aspas, word splitting pode quebrar. Aspas duplas SEMPRE em expansion não-array.
  - (5) **`(s:.:)` em string vazia**: retorna array vazio; código que assume `${(s:.:)var[1]}` sempre existe quebra.
- **Em inglês:** glob/globbing, expansão (expansion), substituição (substitution), case-insensitive, default value, separator, split, join, indireção (indirection).
- **Veja também:**
  - `[[02 - Zsh essencial]]` — `setopt EXTENDED_GLOB` pré-req
  - `[[10 - Plugins, themes e custom no OMZ]]` — globbing em scripts de plugin
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Globbing|globbing]]`, `[[Dicionário do Terminal#Extended glob|extended glob]]`, `[[Dicionário do Terminal#Glob qualifier|glob qualifier]]`, `[[Dicionário do Terminal#Parameter expansion|parameter expansion]]`
- **Referências:** Zsh manual — Expansion (Filename Generation, Parameter Expansion).

Tamanho-alvo: 500-600 linhas. Densa por design (Magus).

- [ ] **Step 4: Adicionar verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Extended glob
Padrões adicionais de globbing do Zsh ativados por `setopt EXTENDED_GLOB`: `^pat` (negação), `~pat` (exclusão), `(p1|p2)` (alternation), `pat#`/`pat##` (zero/um ou mais). Pré-requisito pra usar glob qualifiers.

Veja também: [[09 - Globbing avançado e parameter expansion]], [[02 - Zsh essencial]].

### Glob qualifier
Sufixo entre parênteses pós-fixado a um glob, filtra por atributo do arquivo. Exemplos: `(.)` (regular files), `(/)` (dirs), `(N)` (null glob), `(L+N)` (size > N), `(mh-N)` (modificado em N horas), `(om[1,5])` (ordenar por mtime, 5 mais recentes). Requer `EXTENDED_GLOB`.

Veja também: [[09 - Globbing avançado e parameter expansion]].

### Globbing
Geração de nomes de arquivo a partir de padrões (`*`, `?`, `[abc]`, `**/`). Zsh tem extensões poderosas (EXTENDED_GLOB) que substituem dezenas de combinações `find`/`grep` por one-liners. Apoiado por glob qualifiers pra filtrar por atributos do arquivo.

Veja também: [[09 - Globbing avançado e parameter expansion]].

### Parameter expansion
Expansão do valor de variáveis com transformações inline. Sintaxe: `${var:-default}` (default), `${var//pat/repl}` (replace global), `${var##pre}` (remove prefix longo), `${(L)var}` (lowercase), `${(s:.:)var}` (split). Zsh estende a sintaxe de Bash com flags `(L)/(U)/(C)/(s:x:)/(j:x:)/(@)/(P)/(k)/(v)`.

Veja também: [[09 - Globbing avançado e parameter expansion]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/09 - Globbing avançado e parameter expansion.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/09 - Globbing avançado e parameter expansion.md"
grep -E "^### (Globbing|Extended glob|Glob qualifier|Parameter expansion)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥6 wikilinks, 4 verbetes novos.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/09 - Globbing avançado e parameter expansion.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 09 — Globbing avançado e parameter expansion"
```

---

## Task 12: Nota 10 — Plugins, themes e custom no OMZ

**Files:**
- Create: `03-Dominios/Terminal/Shell/10 - Plugins, themes e custom no OMZ.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: Theme (custom OMZ))

**Conteúdo-chave do spec (§5, Magus):**

> Estrutura de plugin custom (`~/.oh-my-zsh/custom/plugins/<nome>/<nome>.plugin.zsh`). Naming convention. Conteúdo (aliases, functions, completions). Theme custom (`~/.oh-my-zsh/custom/themes/<nome>.zsh-theme`). PROMPT/RPROMPT, color codes (`%F{...}`, `%K{...}`, `%B`, `%U`). Git info. Por que P10k é prompt externo (não theme tradicional). Publicação (custom local / PR upstream / repo próprio).

**Verbetes referenciados:** Theme (custom OMZ) — Plugin (OMZ) já criado em Task 6.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://github.com/ohmyzsh/ohmyzsh/wiki/Customization
WebFetch: https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html
```

Capturar: convenções OMZ pra plugin/theme custom, lista completa de prompt escape sequences.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Plugins, themes e custom no OMZ"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - shell
  - zsh
  - magus
  - oh-my-zsh
  - plugins
  - themes
aliases:
  - Plugins custom OMZ
  - Themes custom OMZ
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "Plugin custom OMZ = pasta `~/.oh-my-zsh/custom/plugins/<nome>/<nome>.plugin.zsh`. Theme custom = `~/.oh-my-zsh/custom/themes/<nome>.zsh-theme` com `PROMPT`/`RPROMPT`. Tudo em Zsh — sem build, sem manifest. Adicionar ao array `plugins=(...)` ou setar `ZSH_THEME` e source. Publicar = mover pra repo git e instruir clone."
- **O que é / Como funciona:**

  ### Plugin custom OMZ

  **Estrutura mínima:**
  ```
  ~/.oh-my-zsh/custom/plugins/<nome>/
  └── <nome>.plugin.zsh
  ```

  Naming convention (obrigatório): nome da pasta = nome do arquivo (sem extensão) + `.plugin.zsh`.

  **Conteúdo do `.plugin.zsh`** pode incluir:
  - Aliases: `alias gst='git status'`
  - Funções: `myfunc() { ... }`
  - Plugin completion: `_<comando>` em arquivo separado dentro da pasta + `fpath+=(${0:h})` no topo do `.plugin.zsh`
  - Inicialização: source de configs, registro de widgets, bindkey

  **Loading:** adicionar `<nome>` ao array `plugins=(...)` no `.zshrc`. OMZ procura primeiro em `$ZSH/plugins/<nome>/` (embarcado), depois em `$ZSH/custom/plugins/<nome>/` (custom) — custom **vence** se nomes coincidem (override).

  ### Theme custom OMZ

  **Estrutura mínima:**
  ```
  ~/.oh-my-zsh/custom/themes/<nome>.zsh-theme
  ```

  **Variáveis chave:**
  - `PROMPT` — prompt da esquerda (multilinha permitido com `\n`)
  - `RPROMPT` — prompt da direita (alinha à direita do terminal)
  - `PS2` — continuation prompt (`>` quando comando incompleto)

  **Prompt escape sequences (Zsh):**
  - `%n` — username
  - `%m` — hostname (sem domain)
  - `%M` — hostname completo
  - `%~` — cwd (contrai `$HOME` pra `~`)
  - `%/` — cwd absoluto
  - `%#` — `%` (user) ou `#` (root)
  - `%?` — exit code do último comando
  - `%j` — número de jobs
  - `%(?.<true>.<false>)` — conditional (exit code 0 ou não)

  **Color codes:**
  - `%F{color}...%f` — foreground colorida (`color` = nome ou 0-255)
  - `%K{color}...%k` — background colorida
  - `%B...%b` — bold
  - `%U...%u` — underline
  - `%S...%s` — standout (reverse video)

  **Git info no prompt** (via plugin OMZ `git` ou `vcs_info`):
  ```zsh
  # PROMPT que mostra branch atual
  PROMPT='%F{cyan}%~%f $(git_prompt_info)%# '

  # git_prompt_info é função do plugin git
  ```

  **Loading:** setar `ZSH_THEME="<nome>"` no `.zshrc` (sem `.zsh-theme`). OMZ procura primeiro em `$ZSH/themes/`, depois em `$ZSH/custom/themes/` — custom **vence**.

  ### Por que Powerlevel10k é prompt e não theme tradicional

  P10k é mais que um `.zsh-theme` — tem instant prompt (precisa estar no TOPO do `.zshrc`), wizard, segments programáveis, hooks de redisplay. Por isso o setup recomendado é **clone direto + source manual**, não `ZSH_THEME`. P10k pode ser usado como OMZ theme (`ZSH_THEME="powerlevel10k/powerlevel10k"`), mas perde instant prompt.

  ### Publicação

  - **Custom local**: fica em `~/.oh-my-zsh/custom/`. Vincular ao seu repo de dotfiles (symlink ou stow).
  - **PR upstream pro OMZ**: se for útil pra muitos, abrir PR em `ohmyzsh/ohmyzsh` seguindo `CONTRIBUTING.md`.
  - **Repo próprio**: criar repo git `<usuario>/<plugin-name>` com README explicando install (`git clone ... custom/plugins/<nome>`).
  - **Plugin managers que entendem repos**: zinit, antibody, zplug — permitem source de plugins direto do GitHub sem clone manual (galho 5 — Dotfiles).
- **Na prática:**

  ### Exemplo: plugin custom `notify` (avisar quando comando longo termina)

  Estrutura:
  ```
  ~/.oh-my-zsh/custom/plugins/notify/
  └── notify.plugin.zsh
  ```

  Conteúdo de `notify.plugin.zsh`:
  ```zsh
  # Avisar via notify-send quando comando que demorou >10s termina
  # Uso: prefixar comando com `notify-long`
  # Ex: notify-long npm install

  notify-long() {
    local start end elapsed
    start=$EPOCHSECONDS
    "$@"
    local exit_code=$?
    end=$EPOCHSECONDS
    elapsed=$((end - start))

    if (( elapsed >= 10 )); then
      if (( exit_code == 0 )); then
        notify-send "Comando terminou" "$*\nTempo: ${elapsed}s"
      else
        notify-send "Comando falhou" "$*\nExit: $exit_code"
      fi
    fi
    return $exit_code
  }
  ```

  Ativar:
  ```zsh
  # No ~/.zshrc, adicionar `notify` ao array
  plugins=(... notify)
  ```

  Source novo shell, testar com `notify-long sleep 15`.

  ### Exemplo: theme custom minimalista `tiny`

  Estrutura:
  ```
  ~/.oh-my-zsh/custom/themes/tiny.zsh-theme
  ```

  Conteúdo de `tiny.zsh-theme`:
  ```zsh
  # Prompt minimalista de 1 linha
  # Formato: cwd colorida + git branch (se em repo) + caractere de prompt

  setopt PROMPT_SUBST

  function tiny_git_branch() {
    local branch
    branch=$(git symbolic-ref --short HEAD 2>/dev/null)
    [[ -n "$branch" ]] && echo " %F{yellow}(${branch})%f"
  }

  PROMPT='%F{cyan}%~%f$(tiny_git_branch) %# '
  RPROMPT='%(?..%F{red}[%?]%f)'   # exit code se != 0
  ```

  Ativar:
  ```zsh
  ZSH_THEME="tiny"
  ```

  Source novo shell.

  ### Exemplo: completion custom dentro do plugin

  Plugin `mytool` com completion próprio:
  ```
  ~/.oh-my-zsh/custom/plugins/mytool/
  ├── mytool.plugin.zsh
  └── _mytool
  ```

  `mytool.plugin.zsh`:
  ```zsh
  # Adiciona a pasta do plugin ao fpath pra `_mytool` ser encontrado
  fpath+=(${0:h})
  ```

  `_mytool` (função de completion):
  ```zsh
  #compdef mytool

  _mytool() {
    local -a subcommands
    subcommands=('init:Initialize project' 'build:Build project' 'serve:Serve dev')
    _describe 'subcommand' subcommands
  }
  ```

  Ativar adicionando `mytool` ao array `plugins=(...)`, rebuild: `rm ~/.zcompdump*; compinit`.
- **Armadilhas:**
  - (1) **Nome de arquivo errado**: pasta `mytool/` com arquivo `my_tool.plugin.zsh` não é encontrado. Convenção: nome da pasta = nome do arquivo.
  - (2) **Custom override silencioso**: se você criar `~/.oh-my-zsh/custom/plugins/git/git.plugin.zsh`, OMZ usa o seu em vez do embarcado — pode causar conflitos sutis se o seu não replicar tudo.
  - (3) **Theme custom esquecendo `setopt PROMPT_SUBST`**: funções dentro de `PROMPT` (como `$(git_branch)`) não expandem. Adicionar `setopt PROMPT_SUBST` no theme ou no `.zshrc`.
  - (4) **Custom completion sem rebuild de `.zcompdump`**: completion não aparece. Sintoma: Tab não completa novo comando. Solução: `rm ~/.zcompdump*; compinit`.
  - (5) **Source de `.plugin.zsh` antes de OMZ load**: variáveis OMZ ainda não definidas (`$ZSH`, `$ZSH_CUSTOM`). Adicionar ao array `plugins=(...)` é o caminho — não source manual.
- **Em inglês:** plugin, theme, customizar (customize), sobrescrever (override), publicar (publish), repositório (repository), contribuir (contribute upstream).
- **Veja também:**
  - `[[04 - Oh-My-Zsh — anatomia e plugins essenciais]]` — pré-req
  - `[[05 - Powerlevel10k]]` — caso de theme externo
  - `[[08 - Completion system (compsys)]]` — completion custom pré-req
  - `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Plugin (OMZ)|plugin]]`, `[[Dicionário do Terminal#Theme (custom OMZ)|theme]]`
- **Referências:** OMZ Customization wiki, Zsh manual — Prompt Expansion.

Tamanho-alvo: 400-500 linhas.

- [ ] **Step 4: Adicionar verbete ao Dicionário**

Inserir em ordem alfabética no bloco `## Shell / Zsh / OMZ`:

```markdown
### Theme (custom OMZ)
Theme próprio de Oh-My-Zsh, arquivo `~/.oh-my-zsh/custom/themes/<nome>.zsh-theme`. Define `PROMPT` (left) e `RPROMPT` (right) usando prompt expansion (`%F{...}`, `%K{...}`, `%n`, `%~`, `%#`). Ativado com `ZSH_THEME="<nome>"` no `.zshrc`. Powerlevel10k é theme externo (não-OMZ-customizado) — vive em `~/powerlevel10k/` e é sourced direto.

Veja também: [[10 - Plugins, themes e custom no OMZ]], [[05 - Powerlevel10k]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar a rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Shell/10 - Plugins, themes e custom no OMZ.md"
grep -c '\[\[' "03-Dominios/Terminal/Shell/10 - Plugins, themes e custom no OMZ.md"
grep -E "^### Theme \(custom OMZ\)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥6 wikilinks, verbete Theme visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Shell/10 - Plugins, themes e custom no OMZ.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-shell): add nota 10 — Plugins, themes e custom no OMZ"
```

---

## ✅ Checkpoint Magus

Após Task 12, todas as 10 notas estão escritas. Verificar:

```bash
ls -1 "03-Dominios/Terminal/Shell/" | sort
git log --oneline | head -12
```

Expected: 10 notas + `index.md`. Últimos 11 commits do galho (esqueleto MOC + dicionário + 10 notas).

---

## Task 13: Pass final no MOC do galho

**Files:**
- Modify: `03-Dominios/Terminal/Shell/index.md` (preencher versões exatas; confirmar wikilinks)

**Objetivo:** trocar placeholders de "Versões assumidas" pelos commits/datas reais capturados no Task 0; confirmar que todos os 10 wikilinks de notas estão ativos (vivos).

- [ ] **Step 1: Substituir placeholders de versões**

Recuperar versões capturadas no Task 0 (Zsh `--version`, OMZ git log, P10k git log). Editar `Shell/index.md`:

`old_string`:
```markdown
## Versões assumidas

- **Zsh:** 5.9+ (Ubuntu/Linux bundle) — versão capturada no Task 0
- **Oh-My-Zsh:** `master` em ~maio/2026 (commit declarado em pass final)
- **Powerlevel10k:** `master` 2024-07 (commit declarado em pass final) — projeto em modo manutenção
- Plugins externos: versões `master` em 2026-05-19
```

`new_string` (substituir `<COMMIT_OMZ>`, `<DATA_OMZ>`, `<COMMIT_P10K>`, `<DATA_P10K>` pelos valores reais):
```markdown
## Versões assumidas

- **Zsh:** 5.9 (Ubuntu/Linux bundle)
- **Oh-My-Zsh:** `master` commit `<COMMIT_OMZ>` (<DATA_OMZ>)
- **Powerlevel10k:** `master` commit `<COMMIT_P10K>` (<DATA_P10K>) — projeto em modo manutenção desde 2024-07
- Plugins externos: versões `master` em 2026-05-19
```

- [ ] **Step 2: Confirmar wikilinks ativos**

Run:
```bash
for n in "01 - Zsh vs Bash" "02 - Zsh essencial" "03 - History do Zsh" \
         "04 - Oh-My-Zsh — anatomia e plugins essenciais" "05 - Powerlevel10k" \
         "06 - Keybindings práticos" "07 - ZLE" "08 - Completion system (compsys)" \
         "09 - Globbing avançado e parameter expansion" "10 - Plugins, themes e custom no OMZ"; do
  test -f "03-Dominios/Terminal/Shell/${n}.md" && echo "ok: $n" || echo "FALTA: $n"
done
```

Expected: 10 linhas `ok:`. Qualquer "FALTA" = nota não foi criada — voltar à task correspondente.

- [ ] **Step 3: Atualizar `updated:` do MOC**

```bash
# Garantir que updated: 2026-05-19 reflita o pass final
```

Edit pra confirmar `updated: 2026-05-19` no frontmatter do MOC.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Shell/index.md"
git commit -m "$(cat <<'EOF'
docs(terminal-shell): pass final no MOC do galho Shell

Substitui placeholders de Versões assumidas pelos commits reais
(Zsh, OMZ, P10k) capturados no pré-flight. Confirma que todos os
10 wikilinks de notas estão ativos.

Galho: docs/superpowers/specs/2026-05-19-terminal-shell-design.md
EOF
)"
```

---

## Task 14: Pass final no Dicionário do Terminal

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (alfabetização + "Veja também" por verbete + confirmar contagem)

**Objetivo:** Garantir que o bloco "Shell / Zsh / OMZ" está em ordem alfabética; que cada verbete tem "Veja também:" apontando pra nota(s) relevante(s); que a contagem de verbetes novos ≥ 30.

- [ ] **Step 1: Validar contagem de verbetes novos**

Run:
```bash
# Lista verbetes do bloco "Shell / Zsh / OMZ"
awk '/^## Shell \/ Zsh \/ OMZ$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md" | sort
awk '/^## Shell \/ Zsh \/ OMZ$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md" | wc -l
```

Expected: contagem ≥ 30; lista em ordem alfabética. Se desordenada, reordenar manualmente com `Edit` (escolher pares `### Termo\n<def>\n\nVeja também: ...\n\n` e movê-los).

**Verbetes esperados no bloco** (em ordem alfabética):
1. Alias
2. Bindkey
3. Builtin
4. Compdef
5. Compinit
6. Compsys
7. Extended glob
8. fc
9. Fpath
10. Function (shell)
11. Glob qualifier
12. Globbing
13. History
14. Instant prompt
15. Nerdfont
16. Oh-My-Zsh
17. Parameter expansion
18. Plugin (OMZ)
19. POSIX
20. Powerlevel10k
21. Prompt
22. Setopt
23. Shell
24. Theme (custom OMZ)
25. Transient prompt
26. Widget
27. ZLE
28. Zsh-autosuggestions
29. Zsh-syntax-highlighting
30. Zstyle

Total esperado: **30 verbetes novos** no bloco Shell/Zsh/OMZ + expansão do Keymap (no bloco Vim/Neovim core).

- [ ] **Step 2: Confirmar expansão do verbete Keymap**

Run:
```bash
sed -n '/^### Keymap$/,/^###/p' "03-Dominios/Terminal/Dicionário do Terminal.md" | head -20
```

Expected: bloco Keymap mostra "Em Neovim" + "Em Zsh (ZLE)", ambas as definições.

- [ ] **Step 3: Confirmar que cada verbete novo tem "Veja também:"**

Run:
```bash
# Contar verbetes do bloco que não têm "Veja também:" logo após a definição
awk '/^## Shell \/ Zsh \/ OMZ$/{f=1; next} /^## /{f=0}
     f && /^### / { v=$0; getline; getline; while(NF==0) getline; if ($0 !~ /^Veja também:/) print v " — sem Veja também" }' \
  "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: nenhuma linha de output. Qualquer linha = verbete sem "Veja também" — adicionar manualmente apontando pra nota correspondente.

- [ ] **Step 4: Atualizar `updated:` do dicionário**

Edit do frontmatter pra `updated: 2026-05-19`.

- [ ] **Step 5: Commit (se houve mudanças)**

```bash
git status --short "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Se houve mudanças (reordenação ou "Veja também" adicionado):
```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "$(cat <<'EOF'
docs(terminal): pass final no Dicionário (bloco Shell/Zsh/OMZ)

Alfabetiza verbetes do bloco Shell/Zsh/OMZ, garante Veja também
em cada verbete novo, atualiza updated. Contagem final: 30 verbetes
novos no bloco + verbete Keymap expandido com sub-sessões Neovim/Zsh.

Galho: docs/superpowers/specs/2026-05-19-terminal-shell-design.md
EOF
)"
```

Se não houve mudanças, pular o commit.

---

## Task 15: Atualizar tronco — ativar wikilink do Shell

**Files:**
- Modify: `03-Dominios/Terminal/index.md` (transformar bullet do Shell em wikilink ativo)

**Objetivo:** Trocar a linha do Shell de `- Shell — galho 2 (planejado): ...` para `- [[03-Dominios/Terminal/Shell/index|Shell]] — galho 2: ...`.

- [ ] **Step 1: Edit do tronco**

Use `Edit` em `03-Dominios/Terminal/index.md`:

`old_string`:
```markdown
- Shell — galho 2 (planejado): Zsh + Oh-My-Zsh + Powerlevel10k
```

`new_string`:
```markdown
- [[03-Dominios/Terminal/Shell/index|Shell]] — galho 2: Zsh + Oh-My-Zsh + Powerlevel10k (config, plugins, completion, ZLE)
```

- [ ] **Step 2: Atualizar `updated:` do tronco**

Edit do frontmatter pra `updated: 2026-05-19`.

- [ ] **Step 3: Confirmar mudança**

Run:
```bash
grep -n "Shell" "03-Dominios/Terminal/index.md"
```

Expected: aparece `[[03-Dominios/Terminal/Shell/index|Shell]]` (wikilink ativo). Bullet antigo `(planejado)` removido.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/index.md"
git commit -m "$(cat <<'EOF'
feat(terminal): tronco com wikilink ativo pro galho 2 (Shell)

Substitui bullet "Shell (planejado)" por wikilink ativo
[[Terminal/Shell/index|Shell]] após entrega do galho 2.

Galho: docs/superpowers/specs/2026-05-19-terminal-shell-design.md
EOF
)"
```

---

## Task 16: Validação final

**Files:**
- (nenhum — só validação)

**Objetivo:** Rodar `verificar-wikilinks` no galho recém-criado + sanity check geral.

- [ ] **Step 1: Verificar wikilinks na pasta Shell/**

Se a skill `/verificar-wikilinks` estiver disponível:

```
Skill: verificar-wikilinks
Args: 03-Dominios/Terminal/Shell/
```

Expected: zero broken links. Qualquer broken link = corrigir antes de seguir.

Se a skill não estiver disponível, fallback manual:

```bash
# Extrai wikilinks de todos os md em Shell/ e verifica se o target existe
python3 <<'PY'
import os, re, sys
from pathlib import Path

root = Path("03-Dominios")
shell = root / "Terminal" / "Shell"

# Coleta nomes de arquivo md em todo o vault (sem extensão)
md_files = {p.stem for p in root.rglob("*.md")}
md_files.update({p.stem for p in Path(".").rglob("*.md") if "node_modules" not in str(p)})

broken = []
for f in shell.rglob("*.md"):
    content = f.read_text()
    # Wikilinks: [[Target]] ou [[Target|alias]] ou [[path/to/Target]]
    for m in re.finditer(r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]', content):
        target = m.group(1).strip()
        # Stem do target (último segmento se for path)
        stem = target.split("/")[-1].replace(".md", "")
        if stem not in md_files:
            broken.append((str(f), target))

if broken:
    print(f"FALTA: {len(broken)} wikilinks quebrados")
    for f, t in broken[:20]:
        print(f"  {f}: [[{t}]]")
    sys.exit(1)
else:
    print(f"ok: nenhum wikilink quebrado em {shell}")
PY
```

Expected: `ok: nenhum wikilink quebrado em 03-Dominios/Terminal/Shell`.

- [ ] **Step 2: Sanity check geral**

Run:
```bash
echo "=== Contagem de arquivos no Shell/ ==="
ls -1 "03-Dominios/Terminal/Shell/" | wc -l    # esperado: 11 (10 notas + index)

echo ""
echo "=== Frontmatter publish: true em todos? ==="
for f in "03-Dominios/Terminal/Shell/"*.md; do
  head -20 "$f" | grep -q "publish: true" && echo "ok: $(basename "$f")" || echo "FALTA publish: $(basename "$f")"
done

echo ""
echo "=== Tronco com wikilink ativo? ==="
grep -q "\[\[03-Dominios/Terminal/Shell/index|Shell\]\]" "03-Dominios/Terminal/index.md" \
  && echo "ok: wikilink Shell ativo no tronco" \
  || echo "FALTA: wikilink ainda inativo"

echo ""
echo "=== Verbetes novos no Dicionário ==="
awk '/^## Shell \/ Zsh \/ OMZ$/{f=1; next} /^## /{f=0} f && /^### /' \
  "03-Dominios/Terminal/Dicionário do Terminal.md" | wc -l    # esperado: ≥ 30

echo ""
echo "=== Commits do galho ==="
git log --oneline | grep -i "terminal-shell\|terminal): scaffold\|terminal): tronco\|terminal): pass" | wc -l
```

Expected:
- 11 arquivos em `Shell/`
- todas as 11 com `publish: true`
- wikilink ativo no tronco
- ≥30 verbetes novos no bloco do Dicionário
- ≥14 commits do galho (1 esqueleto MOC + 1 esqueleto dicionário + 10 notas + 1 pass MOC + 0-1 pass dicionário + 1 tronco)

- [ ] **Step 3: Build local Quartz (se setup disponível)**

Se houver setup Quartz local:
```bash
# Substitua pelo path real do Quartz
cd ~/repos/personal/josenaldo.github.io && npx quartz build && cd -
```

Expected: build conclui sem warnings sobre os arquivos novos do Shell/ ou sobre o Dicionário expandido.

Se Quartz não estiver local, anotar pra rodar manualmente após o galho ser pushed.

- [ ] **Step 4: Sem commit aqui** (apenas validação)

---

## Self-review checklist final

Após Task 16 completar, conferir:

- [ ] **Spec coverage:** cada item de `## 12. Critérios de aprovação` do spec (`docs/superpowers/specs/2026-05-19-terminal-shell-design.md`) tem evidência. Em caso de gap, voltar à task correspondente.
- [ ] **Placeholders:** zero ocorrências de `TBD`, `TODO`, `FIXME` ou `<COMMIT_*>` nos arquivos finais.
- [ ] **Wikilinks:** `verificar-wikilinks` passa em `Shell/`.
- [ ] **Commits:** nenhum tem `Co-Authored-By: Claude`; nenhum usou `--no-verify`.
- [ ] **Tronco:** wikilink do Shell ativo, `(planejado)` removido.
- [ ] **Dicionário:** ≥30 verbetes novos no bloco "Shell / Zsh / OMZ"; Keymap expandido com Neovim + Zsh.
- [ ] **Paths:** nenhum arquivo em `Shell/` contém `/home/josenaldo/...` (todos generalizados pra `~/...`).
- [ ] **Sem fabricação:** nenhuma nota atribui experiência pessoal/profissional ao autor (memória `feedback_no_fabrication`).

Comando final pra confirmar:
```bash
echo "=== /home/josenaldo nos arquivos do Shell? ==="
grep -rn "/home/josenaldo" "03-Dominios/Terminal/Shell/" && echo "REVISAR" || echo "ok: nenhum"

echo ""
echo "=== Co-Authored-By Claude nos commits do galho? ==="
git log --grep="terminal-shell\|terminal): scaffold bloco\|terminal): pass\|terminal): tronco" --format='%H %s' | head -20
git log --grep="terminal-shell\|terminal): scaffold bloco\|terminal): pass\|terminal): tronco" --pretty=full | grep -i "Co-Authored-By: Claude" && echo "REVISAR" || echo "ok: nenhum"
```

---

## Resumo de tasks

| Task | Output | Commits |
|---|---|---|
| 0 | Pré-flight (verificações + mkdir Shell/) | 0 |
| 1 | MOC do galho (esqueleto) | 1 |
| 2 | Bloco "Shell / Zsh / OMZ" no Dicionário (esqueleto) | 1 |
| 3 | Nota 01 — Zsh vs Bash + 3 verbetes | 1 |
| 4 | Nota 02 — Zsh essencial + 3 verbetes | 1 |
| 5 | Nota 03 — History do Zsh + 2 verbetes | 1 |
| 6 | Nota 04 — Oh-My-Zsh + 4 verbetes | 1 |
| 7 | Nota 05 — Powerlevel10k + 5 verbetes | 1 |
| 8 | Nota 06 — Keybindings + 2 verbetes + Keymap expandido | 1 |
| 9 | Nota 07 — ZLE + 1 verbete | 1 |
| 10 | Nota 08 — Compsys + 5 verbetes | 1 |
| 11 | Nota 09 — Globbing + 4 verbetes | 1 |
| 12 | Nota 10 — Plugins/themes custom + 1 verbete | 1 |
| 13 | Pass final MOC | 1 |
| 14 | Pass final Dicionário | 0-1 |
| 15 | Tronco — wikilink ativo | 1 |
| 16 | Validação final (verificar-wikilinks + sanity) | 0 |
| **Total** | **11 arquivos novos + 2 modificados** | **14-15 commits** |

**Verbetes novos totais:** 3 + 3 + 2 + 4 + 5 + 2 + 1 + 5 + 4 + 1 = **30** ✅ (mais expansão do verbete Keymap existente).
