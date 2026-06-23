# Galho 6 — CLI Utils — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar o galho 6 da trilha Terminal — 13 notas atômicas (4 Iniciado + 4 Adepto + 5 Magus) sobre CLI utils modernos em `03-Dominios/Tecnologia/Terminal/CLI Utils/`, MOC do galho, expansão do Dicionário com bloco `## CLI Utils` (~40 verbetes), e ativação do wikilink no tronco.

**Architecture:** Mesmo padrão consolidado nos galhos 2-5. Estrutura H2 fixa. Tom pedagógico — user em adoção zero das 14 ferramentas. Exemplos sempre neutros (`alice`, `myproj`, `example.com`) ou hipotéticos explícitos. Fluxo SDD: implementer → reviewer combinado → fix se Critical/Important. Pesquisa-âncora em docs oficiais antes de cada nota.

**Tech Stack:** Obsidian + Quartz, Markdown + frontmatter YAML, wikilinks. Ferramentas-alvo das notas: fzf, ripgrep, fd, bat, eza, zoxide, atuin, jq, yq (Go + Python), tldr, cheat, delta, btop, htop, dust.

---

## Spec de referência

`docs/superpowers/specs/2026-05-22-terminal-cli-utils-design.md`

## Restrições absolutas (em TODOS os subagent prompts)

1. **Sem fabricação** de uso pessoal. Exemplos neutros (`alice`, `myproj`, `example.com`) ou hipotéticos explícitos (`# hipotético: ...`). NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de comandos/flags. Verificar via doc oficial (WebFetch obrigatório).
3. **Sem `Co-Authored-By: Claude`**. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em `## Veja também`.
6. **Tronco wikilink obrigatório**: `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`.
7. **MOC wikilink** em "Veja também": `[[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]`.
8. **≥5 armadilhas** por nota, **formato bold-label** com `### (N) Título` + 4 labels (`**Causa:**`, `**Sintoma:**`, `**Como detectar:**`, `**Solução:**`). NUNCA callouts.
9. **"Em inglês" em bullets bilíngues** `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
10. **Code fences corretos** e SEMPRE fechadas: ` ```bash `, ` ```json `, ` ```yaml `, ` ```toml `, ` ```text `.
11. **Tom pedagógico** — assume zero conhecimento prévio. Framing "ao adotar X, o ganho é Y" (NUNCA "no meu setup").
12. **Comparações justas** — quando comparar com clássico (rg vs grep, eza vs ls), listar "quando X vence" E "quando clássico vence".
13. **Versões hedged** — "0.4x+; verifique localmente" em vez de pin específico.
14. **Stage explícito por arquivo** — `git add <path>` nominal; NUNCA `git add -A` (working tree tem mudanças não-relacionadas).

---

## Task 0: Pré-flight

**Files:** (nenhum — captura + WebFetch)

- [ ] **Step 1: Capturar versões instaladas localmente**

```bash
for t in fzf rg bat eza zoxide atuin jq yq tldr cheat fd delta dust btop htop; do
  printf "%-10s " "$t"
  command -v $t >/dev/null && $t --version 2>/dev/null | head -1 || echo "(não instalado)"
done
echo "---"
uname -a
echo "---"
cat /etc/os-release 2>/dev/null | head -5
```

Anotar versões — informam o bloco "Versões assumidas" do MOC (Task 1) e versões hedged nas notas.

- [ ] **Step 2: Verificar binários Debian/Ubuntu alternate names**

```bash
command -v fdfind && echo "fd = fdfind (Debian/Ubuntu)"
command -v batcat && echo "bat = batcat (Debian/Ubuntu)"
command -v yq && yq --version 2>&1  # detectar Go vs Python
```

Anotar — informa armadilhas das notas 02 (fd/fdfind), 03 (bat/batcat), 08 (yq Go vs Python).

- [ ] **Step 3: WebFetch das docs oficiais (paralelo)**

Lista de URLs (executar em paralelo via múltiplos WebFetch numa mesma resposta):

- https://github.com/junegunn/fzf
- https://github.com/junegunn/fzf/blob/master/CHANGELOG.md
- https://github.com/BurntSushi/ripgrep
- https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md
- https://github.com/sharkdp/fd
- https://github.com/sharkdp/bat
- https://github.com/eza-community/eza
- https://github.com/ajeetdsouza/zoxide
- https://docs.atuin.sh/
- https://jqlang.github.io/jq/manual/
- https://mikefarah.gitbook.io/yq/
- https://github.com/kislyuk/yq
- https://tldr.sh/
- https://github.com/cheat/cheat
- https://github.com/dandavison/delta
- https://github.com/aristocratos/btop
- https://htop.dev/
- https://github.com/bootandy/dust

Capturar pra cada ferramenta: flags principais, defaults, env vars, exemplos canônicos.

- [ ] **Step 4: Verificar comportamento .gitignore do dust**

Pesquisa específica: dust 1.x respeita `.gitignore` por padrão? Se sim, armadilha da nota 11 vira "dust pode pular files relevantes em projetos com gitignore agressivo"; se não, "dust não respeita .gitignore — node_modules infla output".

```
WebFetch: https://github.com/bootandy/dust
```

Procurar: `--ignore-directory`, `--filter`, comportamento default em diretório com .gitignore. Anotar pra nota 11.

- [ ] **Step 5: Confirmar estrutura do tronco**

```bash
grep -n "galho 6\|CLI Utils" "03-Dominios/Tecnologia/Terminal/index.md"
```

Esperado: linha 32 com `- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…`. Confirmar texto exato pro Task 18.

---

## Task 1: MOC do galho CLI Utils — esqueleto

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/index.md`

- [ ] **Step 1: Criar pasta**

```bash
mkdir -p "03-Dominios/Tecnologia/Terminal/CLI Utils"
```

- [ ] **Step 2: Escrever MOC**

Use `Write` em `03-Dominios/Tecnologia/Terminal/CLI Utils/index.md`:

```markdown
---
title: "CLI Utils"
type: moc
publish: true
created: 2026-05-22
updated: 2026-05-22
status: growing
tags:
  - terminal
  - cli-utils
  - moc
aliases:
  - MOC CLI Utils
  - Galho 6
---
# CLI Utils

> [!abstract] TL;DR
> Galho 6 da trilha Terminal. Ferramentas pequenas e modernas que substituem ou complementam utilitários UNIX clássicos (`cat`, `ls`, `grep`, `find`, `du`, `top`) e elevam o fluxo interativo (`fzf`, `zoxide`, `atuin`) e o processamento de dados (`jq`, `yq`). 13 notas (4 Iniciado + 4 Adepto + 5 Magus), incluindo 2 capstones de composição (stack interativo + pipeline JSON/YAML).

Galho parte do zero (sem assumir uso prévio) até workflows compostos. Iniciado cobre as 4 ferramentas que mais mudam o dia-a-dia. Adepto adiciona produtividade interativa e processamento estruturado. Magus traz capstones de composição e ferramentas operacionais (docs em fluxo, git diff moderno, monitores).

## Conteúdo

### Iniciado

- [[01 - fzf — fuzzy finder universal]]
- [[02 - ripgrep e fd — buscar conteúdo e nomes]]
- [[03 - bat — cat moderno com syntax highlight]]
- [[04 - eza — ls moderno]]

### Adepto

- [[05 - zoxide — cd inteligente com frecency]]
- [[06 - atuin — history shell com SQLite e sync]]
- [[07 - jq — processor JSON com DSL]]
- [[08 - yq — processor YAML e as duas implementações]]

### Magus

- [[09 - tldr e cheat — docs práticas em fluxo]]
- [[10 - delta — pager moderno pra git diff]]
- [[11 - Monitores e disco — btop htop dust]]
- [[12 - Stack interativo — fzf zoxide atuin]]
- [[13 - Pipeline JSON e YAML — jq yq fzf]]

## Mapa de substituições clássicas → modernas

| Clássico | Moderno | Nota |
|---|---|---|
| `cat` | `bat` | [[03 - bat — cat moderno com syntax highlight\|03]] |
| `ls` | `eza` | [[04 - eza — ls moderno\|04]] |
| `grep` | `rg` | [[02 - ripgrep e fd — buscar conteúdo e nomes\|02]] |
| `find` | `fd` | [[02 - ripgrep e fd — buscar conteúdo e nomes\|02]] |
| `cd` (com frecency) | `zoxide` | [[05 - zoxide — cd inteligente com frecency\|05]] |
| `history` / Ctrl-R | `atuin` | [[06 - atuin — history shell com SQLite e sync\|06]] |
| `du` | `dust` | [[11 - Monitores e disco — btop htop dust\|11]] |
| `top` | `btop` / `htop` | [[11 - Monitores e disco — btop htop dust\|11]] |
| `man` (rápido) | `tldr`, `cheat` | [[09 - tldr e cheat — docs práticas em fluxo\|09]] |
| `git diff` / pager | `delta` | [[10 - delta — pager moderno pra git diff\|10]] |

## Rotas alternativas

- **Substituições UNIX mais comuns:** `01` → `02` → `03` → `04`
- **Fluxo interativo moderno:** `01` → `05` → `06` → `12`
- **Processamento estruturado:** `07` → `08` → `13`
- **Git e revisão:** `02` → `10`
- **Observabilidade local:** `11` + tldr (`09`) pra explorar flags rapidamente

## Versões assumidas

Capturadas no pré-flight da execução (Task 0):

- **fzf:** `<VERSAO_FZF>`
- **ripgrep:** `<VERSAO_RG>`
- **fd:** `<VERSAO_FD>` (binário `fdfind` em Debian/Ubuntu)
- **bat:** `<VERSAO_BAT>` (binário `batcat` em Debian/Ubuntu)
- **eza:** `<VERSAO_EZA>`
- **zoxide:** `<VERSAO_ZOXIDE>`
- **atuin:** `<VERSAO_ATUIN>`
- **jq:** `<VERSAO_JQ>`
- **yq:** `<VERSAO_YQ>` (especificar Go ou Python)
- **delta:** `<VERSAO_DELTA>`
- **btop:** `<VERSAO_BTOP>`
- **htop:** `<VERSAO_HTOP>`
- **dust:** `<VERSAO_DUST>`
- **OS de referência:** `<OS_REF>`

Versões nas notas são hedged ("0.4x+; verifique localmente") pra envelhecer bem.

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Tecnologia/Terminal/Shell/index|Shell (galho 2)]] — Zsh + integrações pra muitas dessas ferramentas
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|Dotfiles (galho 5)]] — versionar configs dessas ferramentas
```

Placeholders `<VERSAO_*>` serão substituídos no Task 16 com versões reais capturadas no pré-flight.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/index.md"
git commit -m "feat(terminal-cli-utils): MOC do galho 6 — esqueleto"
```

---

## Task 2: Dicionário — bloco "CLI Utils" esqueleto

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Localizar fim do bloco Dotfiles**

Use `Read` no final do Dicionário pra confirmar último verbete do bloco `## Dotfiles` (deve ser `### XDG Base Directory`).

- [ ] **Step 2: Inserir header novo**

Use `Edit` no Dicionário:
- `old_string`: bloco final do verbete `### XDG Base Directory` (3-4 linhas finais incluindo o "Veja também")
- `new_string`: mesmo + `\n## CLI Utils\n`

Resultado esperado: novo H2 `## CLI Utils` vazio após `## Dotfiles`.

- [ ] **Step 3: Confirmar `updated:` no frontmatter**

Frontmatter deve ter `updated: 2026-05-22`. Se não, Edit pra atualizar.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): adiciona bloco 'CLI Utils' ao Dicionário"
```

---

## Task 3: Nota 01 — fzf: fuzzy finder universal

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/01 - fzf — fuzzy finder universal.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: fuzzy finder, extended search syntax, preview window (fzf), FZF_DEFAULT_OPTS)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/junegunn/fzf
WebFetch: https://github.com/junegunn/fzf/blob/master/CHANGELOG.md
WebFetch: https://github.com/junegunn/fzf/wiki/examples
```

Capturar: algoritmo fuzzy + extended syntax exata (`^`, `$`, `'`, `!`, `|`), env vars (`FZF_DEFAULT_OPTS`, `FZF_DEFAULT_COMMAND`, `FZF_CTRL_R_OPTS`, `FZF_CTRL_T_OPTS`, `FZF_ALT_C_OPTS`), bindings padrão.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "fzf — fuzzy finder universal"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - fzf
  - fuzzy
aliases:
  - fzf
  - Fuzzy finder
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR (callout `> [!abstract] TL;DR`):**
"fzf é um fuzzy finder universal que lê stdin e devolve a seleção no stdout. Vira motor de seleção pra qualquer pipeline: history (Ctrl-R), files (Ctrl-T), cd (Alt-C), branches git, processos. Extended search syntax (`^prefix`, `suffix$`, `'exato`, `!negar`) afina matching. Configurável via `FZF_DEFAULT_OPTS` e `FZF_DEFAULT_COMMAND`. Ao adotar, o ganho é trocar `find ... | grep ...` por seleção interativa com preview."

**O que é / Como funciona** (H3s):

### Filosofia: filtro genérico stdin→stdout
- fzf não é uma ferramenta de busca de arquivos — é um **filtro interativo de listas**
- Lê linhas do stdin; mostra TUI com fuzzy matching; emite linha selecionada no stdout
- Compõe com qualquer comando que produza lista: `git branch | fzf`, `kubectl get pods | fzf`, `ps aux | fzf`

### Algoritmo fuzzy
- Default: matching aproximado por caracteres ordenados (`fmgo` casa `from_go`, `formula_path`, etc.)
- Pontuação combina: caracteres consecutivos, início de palavra, case match
- Resultado: lista ordenada por relevância

### Extended search syntax
Modificadores no input filtram precisamente:
- `^foo` — começa com `foo`
- `foo$` — termina com `foo`
- `'foo` — substring exata `foo` (sem fuzzy)
- `!foo` — NÃO contém `foo`
- `foo bar` — contém `foo` E `bar` (ordem livre)
- `foo | bar` — contém `foo` OU `bar`

### Preview window
- Flag `--preview '<cmd>'` mostra preview do item highlighted no painel lateral
- `{}` é substituído pelo item; `{1}` por primeiro campo, etc.
- Exemplo: `--preview 'bat --color=always {}'` pra preview de arquivos com syntax highlight
- Customizar layout: `--preview-window=right:60%:wrap`

### Integração com shell (Zsh / Bash / Fish)
Install do fzf adiciona bindings:
- **Ctrl-R** — fuzzy search no history
- **Ctrl-T** — fuzzy paste de path no comando atual
- **Alt-C** — fuzzy cd em subdiretório
- **`**<TAB>`** — completion expansion (fuzzy directory/file)

Comportamento Ctrl-T depende de `FZF_CTRL_T_COMMAND` (que comando produz a lista).

**Na prática** (H3s):

### Setup básico (assumindo install via brew/apt/pacman)
```bash
# Ativar bindings no Zsh (idempotente)
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Ou install integration manualmente
$(brew --prefix)/opt/fzf/install --key-bindings --completion --no-update-rc
```

### Env vars úteis
```bash
# Listar com fd em vez de find (respeita .gitignore)
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# Layout padrão
export FZF_DEFAULT_OPTS="--height 60% --layout=reverse --border --preview-window=right:50%:wrap"
```

### Receitas comuns
```bash
# Selecionar branch
git checkout "$(git branch --format='%(refname:short)' | fzf)"

# Kill processo
ps aux | fzf | awk '{print $2}' | xargs -r kill

# Buscar arquivo com preview (bat) e abrir no editor
nvim "$(fd -t f | fzf --preview 'bat --color=always {}')"
```

### Integração com Neovim (Telescope é separado)
- `Telescope` (plugin Neovim) é fuzzy finder embebido no editor — usa lua, não fzf
- `fzf.vim` (plugin) integra fzf externo direto no Neovim
- Em LazyVim, Telescope é default; fzf.vim é opcional pra quem prefere

**Armadilhas (≥5, formato bold-label):**

### (1) Extended search syntax confusa
**Causa:** confundir `'exato` (substring exata) com `^prefix` (começa com).
**Sintoma:** filtro não casa o que esperava.
**Como detectar:** ler doc; testar com input controlado.
**Solução:** lembrar que `'` desativa fuzzy mas não ancora; use `^` pra prefixo, `$` pra sufixo, `'` pra match exato em qualquer posição.

### (2) FZF_DEFAULT_COMMAND ignorando .gitignore
**Causa:** default fallback é `find` cru, que lista `node_modules/`, `.git/`, etc.
**Sintoma:** Ctrl-T mostra milhares de files irrelevantes.
**Como detectar:** `echo $FZF_DEFAULT_COMMAND` vazio ou `find ...`.
**Solução:** setar `FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'` (ou `rg --files`).

### (3) Preview lento (cat de arquivo binário, ou comando custoso)
**Causa:** `--preview 'cat {}'` em binários trava terminal; `--preview 'curl {}'` é lento.
**Sintoma:** UI lagada, terminal corrompido.
**Como detectar:** highlight em binário ou URL deixa fzf travado.
**Solução:** usar `bat` (detecta binário) ou wrapper: `--preview 'file {} | head -1; bat --color=always {} 2>/dev/null || echo binary'`.

### (4) Bindings conflitando com multiplexer (Zellij/tmux)
**Causa:** Ctrl-T ou Alt-C reservados em layout do Zellij.
**Sintoma:** atalho do fzf não aciona; multiplexer consome.
**Como detectar:** Ctrl-T no terminal nu funciona; dentro de Zellij não.
**Solução:** rebindar atalhos no fzf (env vars `FZF_CTRL_T_OPTS` não rebinda a tecla — precisa wrapper) OU rebindar no multiplexer pra liberar a tecla.

### (5) `**<TAB>` completion falhando em PATH/comando específico
**Causa:** completion expansion do fzf não é universal — depende de wrappers por comando.
**Sintoma:** `ssh **<TAB>` ou `kill **<TAB>` não popula.
**Como detectar:** testar com vários comandos; alguns funcionam, outros não.
**Solução:** ver `_fzf_compgen_path`, `_fzf_compgen_dir`, `_fzf_complete_<cmd>` no doc; definir wrapper custom pra comando-alvo.

### (6) Output com aspas/quebras de linha quebrando consumidores
**Causa:** fzf emite raw string; comando consumidor (cd, ssh) pode receber path com espaço/aspas.
**Sintoma:** `cd $(fzf)` falha com "path com espaço".
**Como detectar:** selecionar item com espaço no nome.
**Solução:** usar aspas duplas no command substitution: `cd "$(fzf)"`. Pra múltiplos itens, considerar `--print0` + `xargs -0`.

**Em inglês (8-10 bullets bilíngues, formato `- **PT** — *EN*. "frase técnica curta em PT."`):**

Termos: fuzzy finder, extended search syntax, preview window, key binding, env var, completion, pipe, stdin/stdout, command substitution.

**Veja também:**
- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — fd como fonte default pra `FZF_DEFAULT_COMMAND`
- [[03 - bat — cat moderno com syntax highlight]] — bat como preview de arquivos
- [[12 - Stack interativo — fzf zoxide atuin]] — composição capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#fuzzy finder|fuzzy finder]]
- [[Dicionário do Terminal#extended search syntax (fzf)|extended search syntax]]
- [[Dicionário do Terminal#preview window (fzf)|preview window]]
- [[Dicionário do Terminal#FZF_DEFAULT_OPTS|FZF_DEFAULT_OPTS]]
- [[Dicionário do Terminal#Telescope|Telescope]] — contraponto no Neovim

**Referências:**
- GitHub fzf: https://github.com/junegunn/fzf
- fzf wiki examples: https://github.com/junegunn/fzf/wiki/examples
- fzf changelog: https://github.com/junegunn/fzf/blob/master/CHANGELOG.md

- [ ] **Step 4: 4 verbetes pro Dicionário**

Inserir no bloco `## CLI Utils` em ordem alfabética:

```markdown
### extended search syntax (fzf)
Linguagem de filtro do fzf que estende fuzzy match com âncoras e operadores: `^prefix` (começa com), `suffix$` (termina com), `'exato` (substring exata sem fuzzy), `!negar` (exclui), `a b` (E lógico), `a | b` (OU lógico). Combina com fuzzy default quando não há modificador.

Veja também: [[01 - fzf — fuzzy finder universal]].

### fuzzy finder
Ferramenta interativa de match aproximado em listas — recebe linhas pelo stdin, mostra TUI com filtro em tempo real, emite seleção no stdout. fzf é o canônico no shell; Telescope é o equivalente integrado ao Neovim. Foco no fluxo: substitui `grep | head | escolher` por seleção visual rápida.

Veja também: [[01 - fzf — fuzzy finder universal]], [[12 - Stack interativo — fzf zoxide atuin]].

### FZF_DEFAULT_OPTS
Env var com flags default aplicadas em toda invocação do fzf (a menos que sobrescritas localmente). Lugar típico pra configurar layout (`--height`, `--layout=reverse`), bordas (`--border`), preview default (`--preview-window`). Aplicar também em `FZF_CTRL_R_OPTS`, `FZF_CTRL_T_OPTS`, `FZF_ALT_C_OPTS` pra customizar por binding.

Veja também: [[01 - fzf — fuzzy finder universal]], [[12 - Stack interativo — fzf zoxide atuin]].

### preview window (fzf)
Painel auxiliar do fzf que renderiza preview do item highlighted (arquivo, branch, processo). Configurado via `--preview '<cmd>'` com substituições `{}` (item inteiro), `{1}` (campo 1), etc. Layout via `--preview-window=right:60%:wrap`. Comum usar `bat --color=always {}` pra arquivos.

Veja também: [[01 - fzf — fuzzy finder universal]], [[03 - bat — cat moderno com syntax highlight]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/01 - fzf — fuzzy finder universal.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/01 - fzf — fuzzy finder universal.md"
grep -cE "^### (extended search syntax|fuzzy finder|FZF_DEFAULT_OPTS|preview window)" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥9 wikilinks, 4 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/01 - fzf — fuzzy finder universal.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 01 — fzf"
```

---

## Task 4: Nota 02 — ripgrep e fd: buscar conteúdo e nomes

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: ripgrep, fd, fdfind, smart-case, gitignore-aware)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/BurntSushi/ripgrep
WebFetch: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md
WebFetch: https://github.com/sharkdp/fd
```

Capturar: flags principais de rg (`-t`, `-A/-B/-C`, `--json`, `-F`, `-P`, `--no-ignore`), flavor regex (Rust default; PCRE2 via `-P` se compilado), comportamento smart-case; flags principais de fd (`-t`, `-e`, `-H`, `-x`, `-X`), default ignora hidden e .gitignore.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "ripgrep e fd — buscar conteúdo e nomes"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - ripgrep
  - fd
  - rust
aliases:
  - ripgrep
  - rg
  - fd
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"ripgrep (`rg`) e fd são ferramentas irmãs em Rust (filosofia burntsushi-style): rg busca **conteúdo** recursivamente; fd busca **nomes de arquivo**. Ambas respeitam `.gitignore` por padrão, usam regex Rust (não PCRE), suportam smart-case e são massivamente paralelas. Substituem `grep -r` e `find` em fluxos modernos. Em Debian/Ubuntu o binário do fd se chama `fdfind` (colisão com daemon antigo)."

**O que é / Como funciona** (H3s):

### Filosofia compartilhada
- Defaults pragmáticos pra dev: respeita `.gitignore`, pula `node_modules/`, `.git/`, etc.
- Output colorido e human-readable por padrão; structured (`--json`) quando preciso
- Paralelismo nativo: usa múltiplos threads automaticamente
- Substituições diretas de grep -r / find — sintaxe mais simples no caso comum

### ripgrep (rg) — buscar conteúdo
- Argumento principal: regex pattern
- Flag `-t <tipo>` filtra por tipo de arquivo (`rg -t py`, `rg -t md`)
- Flag `-F` desativa regex (busca literal — útil pra strings com chars regex)
- Flag `-P` ativa PCRE2 (se rg compilado com PCRE2) — necessário pra look-around
- Flags `-A N`, `-B N`, `-C N` mostram N linhas after/before/context
- Output JSON com `--json` pra integração (`rg --json | jq`)
- Smart-case: query lowercase = case-insensitive; query com qualquer maiúscula = case-sensitive
- `--no-ignore` ignora `.gitignore` (busca em tudo, incluindo `node_modules/`)

### fd — buscar nomes
- Argumento principal: substring/regex de nome
- Flag `-t f` só files, `-t d` só dirs, `-t l` só symlinks
- Flag `-e <ext>` filtra extensão (`fd -e py`)
- Flag `-H` inclui hidden (default ignora)
- Flag `-I` ignora `.gitignore` (default respeita)
- Flag `-x <cmd>` executa por item (`fd -e py -x rg 'pdb.set_trace'`)
- Flag `-X <cmd>` executa com TODOS items de uma vez (mais rápido)

### Sinergia rg + fd
- fd filtra arquivos por nome/tipo → rg busca conteúdo dentro deles
- Pipeline canônico: `fd -t f -e py | xargs rg 'def test_'`
- Ou via fd próprio: `fd -t f -e py -x rg 'def test_'`

**Na prática** (H3s):

### Receitas ripgrep
```bash
# Busca simples (smart-case)
rg "TODO"

# Filtrar por tipo
rg -t py "import requests"
rg -t md -t txt "deprecation"

# Match literal (sem regex)
rg -F "function(x, y)"

# Context lines
rg -A 3 -B 3 "panic!"

# Saída estruturada pra jq
rg --json "error" | jq -c 'select(.type == "match")'

# Ignorar .gitignore (busca em node_modules etc.)
rg --no-ignore "TODO"

# Listar arquivos que dão match (sem mostrar matches)
rg -l "FIXME"
```

### Receitas fd
```bash
# Buscar arquivo por substring de nome
fd config

# Só files com extensão
fd -e ts -t f

# Hidden incluso
fd -H '.env'

# Executar por arquivo
fd -t f -e py -x black

# Executar em batch
fd -t f -e py -X wc -l

# Listar pastas (não files)
fd -t d 'tests'
```

### Composição rg + fd
```bash
# Buscar pdb em arquivos Python apenas
fd -t f -e py -x rg 'pdb.set_trace'

# Renomear extensão em batch
fd -e jpeg -x sh -c 'mv "$1" "${1%.jpeg}.jpg"' _ {}

# Listar TODOs em projeto, agrupado por arquivo
rg --files-with-matches 'TODO' | fd -e py
```

### Versões hedged
- ripgrep 14+; verifique `rg --version`
- fd 9+; verifique `fd --version`

**Armadilhas (≥5, bold-label):**

### (1) `.gitignore` comendo arquivos esperados
**Causa:** rg e fd respeitam `.gitignore` por padrão; se você quer buscar em `node_modules/`, `vendor/`, `build/`, eles pulam.
**Sintoma:** "sei que o arquivo existe mas rg não acha".
**Como detectar:** `ls <pasta>` mostra o arquivo; rg/fd não.
**Solução:** flag `--no-ignore` (rg) ou `-I` (fd) pra desativar respeito a gitignore. Combinar com `-H/--hidden` se também precisar de hidden.

### (2) Regex Rust ≠ PCRE (sem look-around por default)
**Causa:** rg usa Rust regex engine por padrão; não tem look-behind (`(?<=...)`) nem look-ahead complexo.
**Sintoma:** regex que funciona em grep -P ou perl falha em rg.
**Como detectar:** mensagem "look-around, including look-ahead and look-behind, is not supported".
**Solução:** usar `-P` (PCRE2) se rg foi compilado com suporte (`rg -P --version` mostra `+pcre2`). Senão, reformular o regex em Rust syntax.

### (3) smart-case surpreendendo com maiúscula
**Causa:** query com qualquer letra maiúscula vira case-sensitive automaticamente.
**Sintoma:** `rg "TODO"` casa só TODO maiúsculo; `rg "todo"` casa também `Todo`, `TODO`.
**Como detectar:** match conta diferente do esperado.
**Solução:** forçar com `-i` (case-insensitive) ou `-s` (case-sensitive) quando precisa controle explícito.

### (4) fd hidden ignorados por padrão
**Causa:** `fd` esconde arquivos começando com `.` (`.env`, `.gitignore`, `.config/`).
**Sintoma:** `fd '.env'` não retorna nada num projeto que tem `.env`.
**Como detectar:** `ls -la` mostra o arquivo; fd não.
**Solução:** flag `-H/--hidden`. Combinar com `-I` se também respeita `.gitignore` em pasta hidden.

### (5) fdfind vs fd em Debian/Ubuntu
**Causa:** pacote `fd-find` no apt instala binário como `fdfind` (colisão com daemon antigo `fd` do bind).
**Sintoma:** `fd` retorna "command not found" mas `fdfind` funciona.
**Como detectar:** `which fd` falha; `which fdfind` resolve.
**Solução:** alias no shell: `alias fd=fdfind` (ou symlink em `~/.local/bin/fd`). Ao copiar receitas pra script, usar nome real em ambos os casos.

### (6) `rg -F` esquecido em string com chars regex
**Causa:** procurar literal `function(x, y)` interpreta `(` como grupo regex.
**Sintoma:** erro de regex ou match estranho.
**Como detectar:** `rg "function(x, y)"` falha; `rg -F "function(x, y)"` funciona.
**Solução:** sempre usar `-F` quando o padrão tem `(`, `)`, `[`, `]`, `.`, `*`, `?`, `+` literais.

**Em inglês (8-10):**
Termos: search, content, filename, recursive, gitignore-aware, smart-case, parallel, regex flavor, look-around, paralelismo.

**Veja também:**
- [[01 - fzf — fuzzy finder universal]] — fzf usa `rg --files` ou `fd` como source
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — `rg --json | jq` pra análise estruturada
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#ripgrep|ripgrep]]
- [[Dicionário do Terminal#fd|fd]]
- [[Dicionário do Terminal#fdfind|fdfind]]
- [[Dicionário do Terminal#smart-case|smart-case]]
- [[Dicionário do Terminal#gitignore-aware|gitignore-aware]]
- [[Dicionário do Terminal#Whitelist (.gitignore)|Whitelist (.gitignore)]] — conceito relacionado em dotfiles

**Referências:**
- ripgrep: https://github.com/BurntSushi/ripgrep
- ripgrep GUIDE: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md
- fd: https://github.com/sharkdp/fd

- [ ] **Step 4: 5 verbetes pro Dicionário**

```markdown
### fd
find moderno escrito em Rust por sharkdp. Respeita `.gitignore` por padrão, ignora hidden por padrão, paralelo, output colorido. Flags principais: `-t f` (só files), `-e <ext>` (extensão), `-H` (hidden), `-I` (ignora gitignore), `-x <cmd>` (executa por item), `-X <cmd>` (batch).

Veja também: [[02 - ripgrep e fd — buscar conteúdo e nomes]].

### fdfind
Nome do binário do fd em Debian/Ubuntu (pacote `fd-find`), por colisão com daemon antigo `fd` do BIND. Solução comum: alias `alias fd=fdfind` ou symlink em `~/.local/bin/fd`. Scripts portáveis devem detectar ambos via `command -v fd || command -v fdfind`.

Veja também: [[02 - ripgrep e fd — buscar conteúdo e nomes]].

### gitignore-aware
Comportamento de ferramentas modernas (rg, fd, eza --git) que respeitam `.gitignore` por padrão, pulando arquivos ignorados pelo git. Vantagem: output focado em código relevante. Armadilha: pode esconder arquivos que você quer ver (use `--no-ignore` em rg, `-I` em fd).

Veja também: [[02 - ripgrep e fd — buscar conteúdo e nomes]], [[04 - eza — ls moderno]].

### ripgrep
grep moderno em Rust por BurntSushi. Recursivo por padrão, gitignore-aware, smart-case, regex Rust (não PCRE), paralelo. Flags principais: `-t <tipo>`, `-F` (literal), `-P` (PCRE2 se compilado), `-A/-B/-C` (context), `--json` (saída estruturada), `--no-ignore`.

Veja também: [[02 - ripgrep e fd — buscar conteúdo e nomes]], [[13 - Pipeline JSON e YAML — jq yq fzf]].

### smart-case
Modo de matching onde query lowercase vira case-insensitive automaticamente; query com qualquer maiúscula vira case-sensitive. Usado por ripgrep, fzf, atuin. Atalho ergonômico — você só especifica `-s`/`-i` quando precisa override.

Veja também: [[02 - ripgrep e fd — buscar conteúdo e nomes]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes.md"
grep -cE "^### (fd|fdfind|gitignore-aware|ripgrep|smart-case)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥9 wikilinks, 5 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 02 — ripgrep e fd"
```

---

## Task 5: Nota 03 — bat: cat moderno com syntax highlight

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/03 - bat — cat moderno com syntax highlight.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: bat, BAT_THEME, batcat, MANPAGER, TTY detection, syntax pager)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/sharkdp/bat
WebFetch: https://github.com/sharkdp/bat#customization
```

Capturar: flags principais (`-n`, `-p`, `--plain`, `-A`, `--diff`, `-l`/`--language`), env vars (`BAT_THEME`, `BAT_PAGER`, `BAT_PAGING`, `BAT_STYLE`), TTY detection behavior, integração com MANPAGER.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "bat — cat moderno com syntax highlight"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - bat
aliases:
  - bat
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"bat é cat moderno com syntax highlight, line numbers, integração git (changes inline). Detecta TTY: em pipe vira cat puro (preserva scripts); em terminal mostra highlight + paginação. Configurável via `BAT_THEME`, `BAT_PAGER`, `BAT_STYLE`. Usado como preview do fzf e como `MANPAGER`. Em Debian/Ubuntu o binário se chama `batcat`."

**O que é / Como funciona** (H3s):

### Filosofia: cat com superpoderes, mas compatível
- Default é "cat melhor": output é colorido em terminal, plano em pipe
- TTY detection: `bat file | grep ...` funciona como `cat file | grep ...` (sem cores, sem header)
- `--plain` ou `-p` força modo cat-puro mesmo em terminal

### Features principais
- **Syntax highlighting** via syntect (engine do Sublime); 150+ linguagens detectadas
- **Line numbers** por padrão (em modo terminal)
- **Git diff inline**: linhas modificadas marcadas com `+`/`-`/`~` na margem
- **Paginação** via `less` (chamado automaticamente em arquivos grandes ou múltiplos)
- **Themes** customizáveis (`bat --list-themes`)

### Env vars relevantes
- `BAT_THEME` — tema (ex: `Dracula`, `Monokai Extended`, `GitHub`); ver `bat --list-themes`
- `BAT_PAGER` — pager usado (default `less -R` se cores; `less` se não); precisa `-R` pra cores ANSI
- `BAT_STYLE` — controla quais elementos mostrar (`numbers,changes,grid` etc.)
- `BAT_PAGING` — `always` / `never` / `auto`

### TTY detection
- Default `--paging=auto` + `--color=auto`: usa stdout TTY check
- Em pipe (`bat foo | head`): vira cat puro, sem cores, sem header
- Em terminal direto: cores + header + numbers
- Pra forçar comportamento de terminal em pipe: `--color=always`

### Integração com MANPAGER
Manpages com syntax highlight:
```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
```
Agora `man find` renderiza com highlight.

### Integração com fzf
```bash
fzf --preview 'bat --color=always --style=numbers --line-range=:500 {}'
```

**Na prática** (H3s):

### Setup básico
```bash
# Listar temas e escolher
bat --list-themes | fzf --preview "bat --theme={} README.md"

# Persistir tema favorito
export BAT_THEME="Dracula"

# Numerar linhas + grid sempre
export BAT_STYLE="numbers,changes,grid"
```

### Receitas comuns
```bash
# Ver arquivo com highlight
bat src/main.rs

# Comparar dois arquivos
bat --diff file_a file_b

# Forçar linguagem (extension ambígua)
bat -l json config.txt

# Modo plano (igual cat) sem header/numbers
bat -p arquivo

# Highlight em pipe (forçar cores)
echo '{"a": 1}' | bat -l json --color=always

# Manpages com highlight (depois de setar MANPAGER)
man find
```

### Aliases sugeridos
```bash
# Não aliasing cat=bat por padrão (TTY detection já cuida)
# Aliasing pra preview rápido com paging custom
alias batp='bat --paging=always --style=plain'
```

### Versão hedged
- bat 0.24+; verifique `bat --version`

**Armadilhas (≥5, bold-label):**

### (1) Aliasing `cat=bat` quebra scripts que dependem de cat-strict
**Causa:** TTY detection do bat é boa mas não perfeita — alguns scripts shell em CI ou ambientes não-TTY podem detectar TTY falsamente, ou esperar EXATAMENTE cat (binário POSIX).
**Sintoma:** script funciona local, falha em container/CI; ou output inesperado em redirecionamento sutil.
**Como detectar:** `[ -t 1 ]` em script revela se stdout é TTY.
**Solução:** evitar `alias cat=bat` global; usar `alias bat=batcat` (Debian) ou função wrapper `bcat()`. Reserve `cat` puro pra scripts.

### (2) `BAT_PAGER=less` sem `-R` perde cores
**Causa:** less por padrão NÃO interpreta ANSI escape; cores viram `^[[31m...` literal.
**Sintoma:** paginação com lixo visual em vez de cores.
**Como detectar:** `echo $BAT_PAGER` mostra `less` sem `-R`.
**Solução:** `export BAT_PAGER="less -R"` (ou `--RAW-CONTROL-CHARS`). Default do bat já faz isso, mas customização manual quebra.

### (3) Binários abrindo no pager e travando terminal
**Causa:** bat detecta arquivo como binário e mostra warning, mas se você forçar `bat -A` (mostrar tudo) em binário grande, vira bagunça.
**Sintoma:** terminal cheio de chars de controle; precisa `reset` pra recuperar.
**Como detectar:** rodar `bat` em `.png`, `.zip`, `.o` sem precaução.
**Solução:** confiar no warning default ("Binary content, use `--show-all` to print"). Se precisar inspeção, usar `xxd` ou `hexdump` em vez.

### (4) `batcat` vs `bat` em Debian/Ubuntu
**Causa:** pacote `bat` no apt instala binário como `batcat` (colisão com `bacula-console` antigo).
**Sintoma:** `bat` retorna "command not found" mas `batcat` funciona.
**Como detectar:** `which bat` falha; `which batcat` resolve.
**Solução:** alias no shell: `alias bat=batcat` (ou symlink em `~/.local/bin/bat`). Verificar com `command -v bat || command -v batcat`.

### (5) Tema escuro/claro descalibrado com o terminal
**Causa:** terminal com fundo escuro + tema bat claro = letras claras sobre fundo claro (ilegível).
**Sintoma:** texto quase invisível ao usar bat.
**Como detectar:** abrir arquivo conhecido e checar legibilidade.
**Solução:** combinar tema bat com tema do terminal. Default `Monokai Extended` funciona bem em fundo escuro; pra fundo claro use `GitHub` ou `OneHalfLight`.

### (6) `MANPAGER` configurado errado quebra `man`
**Causa:** copiar receita errada (sem `col -bx`) deixa backspaces literais (formatação man antiga) corrompendo output.
**Sintoma:** `man find` mostra `_b___b_o___o_l___l_d` em vez de **bold**.
**Como detectar:** texto com underscores excessivos.
**Solução:** receita oficial: `export MANPAGER="sh -c 'col -bx | bat -l man -p'"`. O `col -bx` remove os backspaces antes do bat.

**Em inglês (8-10):**
Termos: syntax highlighting, pager, TTY, env var, theme, line numbers, paging, binary content, escape sequence.

**Veja também:**
- [[01 - fzf — fuzzy finder universal]] — bat como preview default
- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — pipeline com bat preview
- [[10 - delta — pager moderno pra git diff]] — delta usa engine similar (syntect)
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#bat|bat]]
- [[Dicionário do Terminal#BAT_THEME|BAT_THEME]]
- [[Dicionário do Terminal#batcat|batcat]]
- [[Dicionário do Terminal#MANPAGER|MANPAGER]]
- [[Dicionário do Terminal#TTY detection|TTY detection]]
- [[Dicionário do Terminal#syntax pager|syntax pager]]

**Referências:**
- bat repo: https://github.com/sharkdp/bat
- bat customization: https://github.com/sharkdp/bat#customization

- [ ] **Step 4: 6 verbetes pro Dicionário**

```markdown
### bat
cat moderno em Rust por sharkdp, com syntax highlight (engine syntect), line numbers, integração git (changes inline), paginação automática via less. TTY-aware: em pipe vira cat puro. Configurável via `BAT_THEME`, `BAT_PAGER`, `BAT_STYLE`. Comum como preview do fzf e como `MANPAGER`.

Veja também: [[03 - bat — cat moderno com syntax highlight]].

### BAT_THEME
Env var pra tema de syntax highlight do bat. Lista temas disponíveis com `bat --list-themes`. Defaults úteis: `Monokai Extended` (fundo escuro), `GitHub` (fundo claro), `Dracula`, `OneHalfDark`/`OneHalfLight`. Compatível com temas customizados de Sublime/TextMate.

Veja também: [[03 - bat — cat moderno com syntax highlight]].

### batcat
Nome do binário do bat em Debian/Ubuntu (pacote `bat`), por colisão com `bacula-console` antigo. Solução comum: alias `alias bat=batcat` ou symlink em `~/.local/bin/bat`. Scripts portáveis devem detectar ambos via `command -v bat || command -v batcat`.

Veja também: [[03 - bat — cat moderno com syntax highlight]].

### MANPAGER
Env var que define qual pager o `man` usa pra renderizar manpages. Receita comum com bat: `export MANPAGER="sh -c 'col -bx | bat -l man -p'"`. O `col -bx` remove backspaces antigos antes do bat aplicar highlight. Resultado: `man find` com cores e busca interativa.

Veja também: [[03 - bat — cat moderno com syntax highlight]].

### syntax pager
Pager que aplica syntax highlight ao output antes de mostrar (vs less puro). bat é syntax pager genérico; delta é syntax pager especializado pra git diff. Ambos usam engine syntect (port do Sublime grammars pra Rust). Trade-off: cores vs performance em arquivos enormes.

Veja também: [[03 - bat — cat moderno com syntax highlight]], [[10 - delta — pager moderno pra git diff]].

### TTY detection
Detecção, pelo programa, se stdout é um terminal interativo ou um pipe/redirecionamento. APIs típicas: `isatty(1)` em C, `[ -t 1 ]` em shell. Ferramentas modernas (bat, eza, fzf) usam TTY detection pra decidir defaults (cores, paginação, header) — em pipe viram modo "plano" pra preservar scripts.

Veja também: [[03 - bat — cat moderno com syntax highlight]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/03 - bat — cat moderno com syntax highlight.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/03 - bat — cat moderno com syntax highlight.md"
grep -cE "^### (bat|BAT_THEME|batcat|MANPAGER|syntax pager|TTY detection)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥10 wikilinks, 6 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/03 - bat — cat moderno com syntax highlight.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 03 — bat"
```

---

## Task 6: Nota 04 — eza: ls moderno

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/04 - eza — ls moderno.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: eza, exa (legado), EZA_COLORS)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/eza-community/eza
WebFetch: https://github.com/eza-community/eza/blob/main/man/eza.1.md
```

Capturar: flags principais (`-l`, `-a`, `--tree`, `--git`, `--icons`, `--color-scale`, `--sort`), env vars (`EZA_COLORS`, `EZA_ICONS_AUTO`), relação com Nerd Fonts, status do projeto exa (arquivado).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "eza — ls moderno"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - eza
  - listing
aliases:
  - eza
  - ls moderno
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"eza é ls moderno em Rust — fork ativo do exa (arquivado em agosto 2023). Cores por tipo, ícones (com Nerd Font), modo árvore (`--tree`), status git inline (`--git`), color-scale por tamanho/idade. Configurável via `EZA_COLORS` (sintaxe diferente de `LS_COLORS`). Substitui `ls` pra inspeção visual rápida; mantém compat com ls(1) só parcialmente."

**O que é / Como funciona** (H3s):

### Filosofia e história
- exa: criado em 2014 por Benjamin Sago; arquivado em agosto 2023
- eza: fork comunitário ativo; mantém compat e adiciona features
- Default: cores por tipo de arquivo, info adicional em `-l` (perms, size humano, modificação, git status)
- Não é drop-in replacement de ls — algumas flags diferem; tem features que ls não tem

### Modos principais
- **Simple**: `eza` — lista arquivos coloridos, sem detalhes
- **Long**: `eza -l` — permissions, size, modificação, owner
- **All**: `eza -a` (inclui hidden) ou `-A` (hidden mas pula `.` e `..`)
- **Tree**: `eza --tree` (ou `-T`) — árvore recursiva; `-L 2` limita profundidade
- **Git**: `eza --git` — coluna extra com status git (M/A/D/I/N/T)
- **Long all**: `eza -lah` — combinação comum

### Ícones e Nerd Font
- `--icons` ativa ícones por tipo (folder, py, rs, md, etc.)
- Requer **Nerd Font** instalada E configurada no terminal
- Sem Nerd Font: ícones aparecem como quadrados ou `?`
- Env: `EZA_ICONS_AUTO=1` ativa por default se stdout é TTY

### Color-scale
- `--color-scale=size` ou `--color-scale=age` — gradiente de cor por tamanho/idade
- Visual rápido pra "quem é grande/antigo"

### Sorting
- `--sort=name|size|modified|created|extension|inode`
- `-r` reverte ordem; `--group-directories-first` agrupa diretórios primeiro

### EZA_COLORS vs LS_COLORS
- Sintaxe própria (não compatível com LS_COLORS do GNU coreutils)
- Formato: chave=código (ex: `di=34;01:fi=32`)
- Ver doc oficial pra chaves disponíveis (não são as mesmas do dircolors)

**Na prática** (H3s):

### Setup básico
```bash
# Aliases sugeridos no shell init
alias ls='eza --group-directories-first'
alias ll='eza -l --git --group-directories-first'
alias la='eza -lah --git --group-directories-first'
alias lt='eza --tree -L 2'
```

### Receitas
```bash
# Long listing com git status
eza -l --git

# Árvore limitada
eza --tree -L 3 --git-ignore  # respeita .gitignore

# Ordenar por tamanho descendente
eza -l --sort=size -r

# Color-scale por idade
eza -l --color-scale=age

# Só arquivos de uma extensão (não tem flag — pipe)
eza -l | rg '\.rs$'
```

### Quando eza vence ls
- Inspeção visual rápida em pastas com muitos arquivos
- Ver git status de arquivos sem rodar `git status`
- Árvore (sem precisar `tree` separado)
- Comparar tamanhos visualmente (color-scale)

### Quando ls clássico vence
- Scripts portáveis POSIX (ls está em qualquer Unix; eza precisa install)
- CI/ambientes minimalistas
- Compat de flags com ls(1) em scripts legados
- Speed em pastas enormes (eza tem overhead de parsing extra)

### Versão hedged
- eza 0.18+; verifique `eza --version`

**Armadilhas (≥5, bold-label):**

### (1) Ícones aparecendo como `?` ou quadrados
**Causa:** terminal sem Nerd Font configurada — glyphs Unicode privados (PUA) do Nerd Font ausentes na fonte default.
**Sintoma:** `eza --icons` mostra `` ou `?` em vez de ícones.
**Como detectar:** trocar pra fonte clássica (DejaVu Sans Mono); se quebra, era Nerd Font.
**Solução:** instalar Nerd Font (MesloLGS NF, FiraCode NF, JetBrainsMono NF) e configurar no terminal emulator. Ver verbete `[[Dicionário do Terminal#Nerd Font|Nerd Font]]`.

### (2) `alias ls=eza` quebra scripts que esperam flags ls(1) clássicos
**Causa:** alguns scripts CI ou Makefiles esperam `ls -la` com formato GNU/BSD exato; eza tem layout diferente.
**Sintoma:** parsing de output falha em scripts.
**Como detectar:** script funciona em CI sem alias; falha local com alias.
**Solução:** alias interativo somente: `if [[ -t 1 ]]; then alias ls=eza; fi`. Ou usar nome diferente (`alias l=eza`) preservando `ls` puro.

### (3) `--git` lento em repos grandes
**Causa:** flag busca git status pra cada arquivo listado; em repo com milhares de files, custa.
**Sintoma:** `eza -l --git` lento em monorepo enorme.
**Como detectar:** `time eza -l --git` num monorepo vs `time eza -l`.
**Solução:** usar `--git` só em pastas pequenas; remover do alias default `ll`; criar alias específico (`llg`) pra quando precisar.

### (4) Ordenação default ≠ lexicográfica (group-dirs-first)
**Causa:** algumas configs/aliases ativam `--group-directories-first` por default; ordem visual ≠ ls default.
**Sintoma:** ordem confusa quando comparar mentalmente com ls.
**Como detectar:** `eza` vs `ls` no mesmo dir.
**Solução:** decidir convenção (manter group-dirs-first é comum; ou removê-lo). Documentar em dotfiles pra futura você não estranhar.

### (5) `EZA_COLORS` ≠ `LS_COLORS` (sintaxe diferente)
**Causa:** copiar `LS_COLORS` de dircolors pra `EZA_COLORS` não funciona — eza usa chaves próprias.
**Sintoma:** cores não aplicam ou aplicam errado.
**Como detectar:** comparar `echo $LS_COLORS` com `echo $EZA_COLORS`.
**Solução:** ler `eza --color-help` ou doc oficial pras chaves do eza. Manter as duas vars separadas (LS_COLORS pra ls clássico; EZA_COLORS pro eza).

### (6) eza vs exa — confundir documentação antiga
**Causa:** muitos tutoriais antigos referenciam exa (`brew install exa`); o pacote foi arquivado.
**Sintoma:** install command falha; binário desatualizado.
**Como detectar:** `exa --version` mostra data antiga (2022 ou anterior).
**Solução:** sempre instalar eza (`brew install eza`, `cargo install eza`). Flags são quase 100% compat; migração trivial.

**Em inglês (8-10):**
Termos: listing, long format, hidden file, tree view, git status, icons, color scale, fork, archived, lexicographic.

**Veja também:**
- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — `fd -t d` lista pastas com semantics próprias
- [[03 - bat — cat moderno com syntax highlight]] — par natural na "stack moderna"
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#eza|eza]]
- [[Dicionário do Terminal#exa (legado)|exa (legado)]]
- [[Dicionário do Terminal#EZA_COLORS|EZA_COLORS]]
- [[Dicionário do Terminal#Nerd Font|Nerd Font]]
- [[Dicionário do Terminal#gitignore-aware|gitignore-aware]] — `--git-ignore` em eza

**Referências:**
- eza repo: https://github.com/eza-community/eza
- eza manpage: https://github.com/eza-community/eza/blob/main/man/eza.1.md
- exa (arquivado): https://the.exa.website/

- [ ] **Step 4: 3 verbetes pro Dicionário**

```markdown
### eza
ls moderno em Rust; fork ativo do exa (arquivado em agosto 2023). Cores por tipo, ícones (com Nerd Font), modo árvore (`--tree`), status git inline (`--git`), color-scale (`--color-scale=size|age`). Sintaxe parcial-compat com ls(1) — algumas flags diferem.

Veja também: [[04 - eza — ls moderno]].

### exa (legado)
ls moderno original em Rust por Benjamin Sago; arquivado em agosto 2023. Sucessor é eza (fork comunitário ativo). Tutoriais antigos referenciam exa; novos installs devem usar eza diretamente. Flags são quase 100% compat — migração trivial.

Veja também: [[04 - eza — ls moderno]].

### EZA_COLORS
Env var pra customizar cores do eza; sintaxe própria (NÃO compatível com `LS_COLORS` do GNU dircolors). Formato chave=código (ex: `di=34;01:fi=32`). Chaves específicas do eza em `eza --color-help` ou na doc oficial. Coexiste com `LS_COLORS` (uma por ferramenta).

Veja também: [[04 - eza — ls moderno]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/04 - eza — ls moderno.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/04 - eza — ls moderno.md"
grep -cE "^### (eza|exa \(legado\)|EZA_COLORS)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥9 wikilinks, 3 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/04 - eza — ls moderno.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 04 — eza"
```

---

## Task 7: Nota 05 — zoxide: cd inteligente com frecency

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/05 - zoxide — cd inteligente com frecency.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: zoxide, frecency, init script (shell))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/ajeetdsouza/zoxide
WebFetch: https://github.com/ajeetdsouza/zoxide/wiki
```

Capturar: algoritmo frecency, comandos (`z`, `zi`, `zoxide query`), init para Zsh/Bash/Fish, location do DB, integração com fzf pra `zi`.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "zoxide — cd inteligente com frecency"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - zoxide
  - frecency
aliases:
  - zoxide
  - z (zoxide)
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"zoxide é cd inteligente baseado em **frecency** (frequency + recency). Mantém DB local de pastas visitadas; `z foo` pula direto pra match com maior pontuação; `zi foo` abre fzf interativo. Init script no shell (substitui ou suplementa `cd`). Sucessor de `autojump` e `z.sh` — mais rápido (Rust), DB mais robusta (sqlite-like)."

**O que é / Como funciona** (H3s):

### Filosofia: aprender com seu uso
- Pastas que você visita muito + recentemente sobem na ranking
- Substring matching com pontuação: `z proj` pula pra pasta mais "frecente" cujo path contém `proj`
- DB local em `~/.local/share/zoxide/db.zo` (binário compacto)

### Algoritmo frecency
- Cada `cd` em pasta incrementa contador + atualiza timestamp
- Pontuação combina: número de visitas × recency factor
- Pastas antigas vão decaindo; pastas frequentes-e-recentes dominam
- Resultado: query curta basta pra navegar bem

### Comandos
- `z <substring>` — pula pra match com maior pontuação
- `z <a> <b>` — pula pra match que contém `a` E `b`
- `zi <substring>` — abre fzf interactive com candidatos rankeados (precisa fzf instalado)
- `z -` — volta pra pasta anterior (igual `cd -`)
- `zoxide query --list` — lista todas as entradas com pontuação (debug)
- `zoxide add <path>` — adiciona path manualmente
- `zoxide remove <path>` — remove entrada

### Init script no shell
- Comando: `zoxide init <shell>` produz script que define função/widget
- Adicionar ao `.zshrc`/`.bashrc`/`config.fish`:
  ```bash
  eval "$(zoxide init zsh)"
  ```
- Por padrão, define funções `z` e `zi`; sobrescrever `cd` requer `--cmd cd`

### DB location e portabilidade
- Default: `~/.local/share/zoxide/db.zo` (Linux); macOS análogo
- Configurável via `_ZO_DATA_DIR` env var
- Não sincroniza entre máquinas automaticamente — cada máquina tem o próprio DB

**Na prática** (H3s):

### Setup
```bash
# Install (assumindo via package manager ou cargo)
# Adicionar ao .zshrc DEPOIS do plugin manager (oh-my-zsh, zinit, etc.)
eval "$(zoxide init zsh)"

# Opcional: substituir cd completamente
# eval "$(zoxide init zsh --cmd cd)"
# Agora `cd foo` é zoxide; `cd /caminho/absoluto` ainda funciona
```

### Receitas
```bash
# Pular pra pasta "myproj" mais frecente
z myproj

# Pular pra match que tem 'src' e 'cli'
z src cli

# Interactive — escolher entre top matches
zi myproj

# Limpar DB (raro — se entradas obsoletas atrapalham)
zoxide query --all | xargs -I {} echo "remove: {}"  # dry-run
# Manual: zoxide remove <path>
```

### Migração de autojump / z.sh
```bash
zoxide import --from autojump ~/.local/share/autojump/autojump.txt
zoxide import --from z ~/.z
```

### Versão hedged
- zoxide 0.9+; verifique `zoxide --version`

**Armadilhas (≥5, bold-label):**

### (1) Init script ordering errado quebra `z`
**Causa:** `eval "$(zoxide init zsh)"` ANTES do plugin manager (oh-my-zsh, zinit, prezto) — plugins sobrescrevem widget/função.
**Sintoma:** `z` não funciona ou conflita com outra coisa.
**Como detectar:** `which z` mostra função de outro plugin ou builtin.
**Solução:** colocar `eval "$(zoxide init zsh)"` no FIM do `.zshrc`, depois de tudo que mexe em widgets/aliases.

### (2) `zi` sem fzf instalado falha silenciosamente
**Causa:** `zi` requer fzf no PATH; sem ele, behavior varia (erro ou fallback ruim).
**Sintoma:** `zi` não abre menu interativo.
**Como detectar:** `command -v fzf` retorna vazio.
**Solução:** instalar fzf primeiro (é dependência soft pra usar `zi`; `z` puro funciona sem).

### (3) Match surpresa em substring curta
**Causa:** `z d` casa qualquer pasta cujo path contém `d` (centenas em monorepo).
**Sintoma:** pula pra pasta inesperada.
**Como detectar:** `zoxide query d --list` mostra todos os candidatos.
**Solução:** usar substring maior (`z docs` em vez de `z d`), ou compor (`z docs api`).

### (4) DB não migra entre máquinas
**Causa:** `~/.local/share/zoxide/db.zo` é local; ao trocar de máquina, começa do zero.
**Sintoma:** `z` precisa "aprender de novo" no laptop novo.
**Como detectar:** `zoxide query --list` vazio em máquina recém-configurada.
**Solução:** sincronizar `db.zo` via Syncthing/Resilio entre máquinas similares; ou aceitar o cold start (uma semana de uso reconstrói o útil).

### (5) Conflito com aliases `cd` em containers/CI
**Causa:** em ambientes minimalistas sem zoxide instalado, scripts que assumem `cd foo` funcionar falham.
**Sintoma:** script funciona local; falha em CI.
**Como detectar:** rodar script em container limpo.
**Solução:** scripts portáveis devem usar paths absolutos ou checar `command -v zoxide` antes de usar `z`.

### (6) `_ZO_DATA_DIR` customizado quebrando portabilidade do init
**Causa:** mudar `_ZO_DATA_DIR` sem garantir que outras máquinas têm a mesma var.
**Sintoma:** zoxide procura DB no lugar errado; DB vazio.
**Como detectar:** `zoxide query --list` vazio mesmo após uso.
**Solução:** se customizar, exportar `_ZO_DATA_DIR` ANTES do `eval init` no `.zshrc`; documentar em dotfiles.

**Em inglês (8-10):**
Termos: frecency, frequency, recency, init script, substring match, database, ranking, widget, shell function, fuzzy.

**Veja também:**
- [[01 - fzf — fuzzy finder universal]] — `zi` usa fzf
- [[06 - atuin — history shell com SQLite e sync]] — também usa frecency em outra dimensão
- [[12 - Stack interativo — fzf zoxide atuin]] — composição capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#zoxide|zoxide]]
- [[Dicionário do Terminal#frecency|frecency]]
- [[Dicionário do Terminal#init script (shell)|init script (shell)]]

**Referências:**
- zoxide repo: https://github.com/ajeetdsouza/zoxide
- zoxide wiki: https://github.com/ajeetdsouza/zoxide/wiki

- [ ] **Step 4: 3 verbetes pro Dicionário**

```markdown
### frecency
Métrica de ranking que combina **frequency** (quantas vezes algo foi acessado) e **recency** (quão recente foi o último acesso). Pontuação decai com o tempo, mantendo "ativos recentes" no topo. Usada por zoxide pra pastas, atuin pra comandos do histórico, e historicamente por Firefox/Awesome Bar pra URLs.

Veja também: [[05 - zoxide — cd inteligente com frecency]], [[06 - atuin — history shell com SQLite e sync]].

### init script (shell)
Trecho de código shell que uma ferramenta (zoxide, atuin, fzf, starship) injeta no `.zshrc`/`.bashrc`/`config.fish` pra ativar funções, widgets, completion e bindings. Tipicamente via `eval "$(<tool> init <shell>)"`. Ordem importa: init scripts que mexem em widgets devem vir DEPOIS do plugin manager.

Veja também: [[05 - zoxide — cd inteligente com frecency]], [[06 - atuin — history shell com SQLite e sync]], [[12 - Stack interativo — fzf zoxide atuin]].

### zoxide
cd inteligente em Rust baseado em frecency. Mantém DB local de pastas visitadas; `z foo` pula direto pro match mais frecente; `zi foo` abre fzf interativo com candidatos rankeados. Sucessor de `autojump` e `z.sh` — mais rápido, DB mais robusta. Não sincroniza entre máquinas por padrão.

Veja também: [[05 - zoxide — cd inteligente com frecency]], [[12 - Stack interativo — fzf zoxide atuin]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/05 - zoxide — cd inteligente com frecency.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/05 - zoxide — cd inteligente com frecency.md"
grep -cE "^### (frecency|init script \(shell\)|zoxide)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥8 wikilinks, 3 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/05 - zoxide — cd inteligente com frecency.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 05 — zoxide"
```

---

## Task 8: Nota 06 — atuin: history shell com SQLite e sync

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: atuin, history sync, E2E encryption (history sync))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://docs.atuin.sh/
WebFetch: https://github.com/atuinsh/atuin
```

Capturar: comandos (`atuin import`, `atuin search`, `atuin stats`, `atuin sync`), search modes (`prefix`, `fulltext`, `fuzzy`), config em `~/.config/atuin/config.toml`, `secrets_filter`, modelo E2E do sync (key local), self-host setup.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "atuin — history shell com SQLite e sync"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - atuin
  - history
aliases:
  - atuin
  - history sync
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"atuin reescreve o history do shell em SQLite local, com fuzzy search interativa via Ctrl-R, stats (top comandos, dias mais ativos), e sync opcional E2E-encrypted (self-host ou atuin.sh). Cada comando registra cwd, exit code, duração, hostname — context muito mais rico que `~/.zsh_history`. Init script substitui binding do Ctrl-R."

**O que é / Como funciona** (H3s):

### Filosofia: history como dataset estruturado
- `~/.zsh_history` legacy: texto plano, comando por linha (talvez com timestamp)
- atuin: SQLite com schema rico (comando, cwd, hostname, exit code, duração, timestamp, session)
- Substitui Ctrl-R por TUI fuzzy/full-text com filtros (por cwd, por exit code, por host)

### Search modes
- `prefix` — match começa com
- `fulltext` — substring em qualquer posição
- `fuzzy` — fuzzy match (estilo fzf)
- Configurável em `~/.config/atuin/config.toml` (`search_mode = "fuzzy"`)

### Stats
- `atuin stats` — agregados (top commands, top dias da semana, etc.)
- `atuin history list` — listagem filtrável
- `atuin history list --cwd ~/work` — filtrar por pasta

### Sync E2E-encrypted (opcional)
- Default: SQLite só local (sem internet)
- Opcional: sync com servidor (atuin.sh hosted ou self-host)
- Modelo: chave de encryption gerada LOCAL no setup; servidor só vê bytes encriptados
- Trust: ainda confia que atuin.sh não tem backdoor; self-host elimina esse trust
- Sync resolve conflitos via timestamp + UUID

### Config (`~/.config/atuin/config.toml`)
- `search_mode` — modo de busca default
- `secrets_filter` — regex pra NÃO armazenar comandos com tokens/senhas
- `auto_sync` — `true`/`false`
- `sync_address` — URL do servidor (atuin.sh ou self-host)
- `style` — `auto|compact|full` (visual da TUI)

**Na prática** (H3s):

### Setup
```bash
# Install atuin
# Importar history existente
atuin import zsh   # ou bash/fish

# Ativar binding Ctrl-R (init script)
eval "$(atuin init zsh)"

# Opcional: registrar conta pra sync (auto-gera key local)
atuin register -u alice -e alice@example.com  # cria key local + login servidor
atuin sync                                      # primeira sync
```

### Config segura (não armazenar secrets)
```toml
# ~/.config/atuin/config.toml
search_mode = "fuzzy"
auto_sync = false                # default: review antes de syncar
inline_height = 25
style = "compact"

[secrets_filter]
filter_failed_exit_codes = false
patterns = [
    "AKIA[0-9A-Z]{16}",         # AWS access key
    "ghp_[A-Za-z0-9]{36}",      # GitHub PAT
    "sk-[A-Za-z0-9]{48}",       # OpenAI key
]
```

### Receitas
```bash
# Buscar comandos rodados em pasta específica
atuin search --cwd ~/work git

# Stats agregados
atuin stats

# Listar últimos 50 com exit code não-zero
atuin history list --filter-mode "all-failed" | head -50

# Sync manual (não-auto)
atuin sync
```

### Versão hedged
- atuin 18+; verifique `atuin --version`

**Armadilhas (≥5, bold-label):**

### (1) `atuin import` no shell errado
**Causa:** rodar `atuin import bash` quando seu history é zsh — não acha o arquivo ou parsing falha.
**Sintoma:** "no history found" ou imports zero entries.
**Como detectar:** verificar shell atual com `echo $SHELL`; verificar `HISTFILE`.
**Solução:** rodar `atuin import <shell>` com o shell certo (`zsh`, `bash`, `fish`). Re-rodar não duplica entradas (atuin deduplica por hash).

### (2) Sync com atuin.sh = confiar em third-party
**Causa:** mesmo com E2E encryption, o cliente vem da atuin.sh e o trust model assume cliente honesto.
**Sintoma:** preocupação de privacy mesmo com "E2E encrypted".
**Como detectar:** ler threat model na doc oficial.
**Solução:** **self-host** o servidor atuin (Docker; é simples) se trust de third-party é problema. E2E encryption ainda vale; servidor self-hosted só elimina o middleman.

### (3) Secrets viajando no sync
**Causa:** `secrets_filter` não configurado; tokens API e senhas em comandos viram parte do history e sincronizam.
**Sintoma:** `aws s3 cp ... AKIA...` aparece no sync.
**Como detectar:** `atuin history list | grep -iE 'token|key|secret'`.
**Solução:** configurar `secrets_filter` com regex pros formatos de keys que você usa (AWS, GitHub, OpenAI, etc.). Deletar entradas pré-existentes: `atuin history list | grep TOKEN | xargs -I {} atuin history delete {}`.

### (4) SQLite lock em multi-shell heavy use
**Causa:** muitos shells abertos escrevendo no mesmo SQLite simultaneamente.
**Sintoma:** "database is locked" erros sporádicos.
**Como detectar:** logs do atuin (`~/.local/share/atuin/`) com lock errors.
**Solução:** atuin recente lida bem; se persistir, aumentar `db_busy_timeout` no config. Em casos extremos, reduzir número de shells concorrentes.

### (5) Reset acidental (`atuin db delete`) sem backup
**Causa:** rodar comando destrutivo sem entender — apaga history local; se não sincado, é perda total.
**Sintoma:** `atuin search` vazio após reset.
**Como detectar:** `atuin stats` zerado.
**Solução:** SEMPRE backup `~/.local/share/atuin/history.db` antes de comandos destrutivos. Se sync ativo, `atuin sync` baixa de volta do servidor; sem sync, é perda definitiva.

### (6) Binding Ctrl-R conflita com plugins Zsh
**Causa:** plugin como `zsh-autosuggestions` ou `oh-my-zsh` redefine Ctrl-R; init do atuin precisa vir DEPOIS.
**Sintoma:** Ctrl-R abre history clássico (não atuin TUI).
**Como detectar:** `bindkey | grep '\^R'` mostra binding diferente do esperado.
**Solução:** mover `eval "$(atuin init zsh)"` pro fim do `.zshrc`, depois de tudo que mexe em bindkey.

**Em inglês (8-10):**
Termos: shell history, search mode, end-to-end encryption, self-host, stats, exit code, working directory, sync, filter, regex.

**Veja também:**
- [[05 - zoxide — cd inteligente com frecency]] — par natural (atuin pra history; zoxide pra pasta)
- [[12 - Stack interativo — fzf zoxide atuin]] — composição capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#atuin|atuin]]
- [[Dicionário do Terminal#history sync|history sync]]
- [[Dicionário do Terminal#E2E encryption (history sync)|E2E encryption (history sync)]]
- [[Dicionário do Terminal#frecency|frecency]]
- [[Dicionário do Terminal#init script (shell)|init script (shell)]]

**Referências:**
- atuin docs: https://docs.atuin.sh/
- atuin repo: https://github.com/atuinsh/atuin

- [ ] **Step 4: 3 verbetes pro Dicionário**

```markdown
### atuin
history shell em SQLite com fuzzy search e sync opcional E2E-encrypted (self-host ou atuin.sh). Cada comando registra cwd, exit code, duração, hostname. Substitui binding nativo do Ctrl-R por TUI rica. Config em `~/.config/atuin/config.toml` (search mode, secrets_filter, auto_sync).

Veja também: [[06 - atuin — history shell com SQLite e sync]], [[12 - Stack interativo — fzf zoxide atuin]].

### history sync
Sincronização de comandos shell entre máquinas. Naive: arquivo plano sync via dropbox/git (vaza secrets, sem dedup). atuin faz direito: SQLite + protocolo dedicado + E2E encryption. Trade-off: dependência de servidor (atuin.sh hosted ou self-hosted). Comandos sincados ficam disponíveis em todas as máquinas com a mesma key.

Veja também: [[06 - atuin — history shell com SQLite e sync]].

### E2E encryption (history sync)
Encryption fim-a-fim aplicada ao histórico de shell antes de sincronizar com servidor remoto. Chave gerada localmente no setup; servidor armazena só bytes encriptados. Modelo do atuin: ainda confia que cliente é honesto; self-host elimina trust de third-party. Não substitui `secrets_filter` (filtrar antes de armazenar é a defesa primária).

Veja também: [[06 - atuin — history shell com SQLite e sync]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync.md"
grep -cE "^### (atuin|history sync|E2E encryption \(history sync\))$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥9 wikilinks, 3 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 06 — atuin"
```

---

## Task 9: Nota 07 — jq: processor JSON com DSL

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/07 - jq — processor JSON com DSL.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: jq, raw output (jq -r), slurp (jq -s))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://jqlang.github.io/jq/manual/
WebFetch: https://jqlang.github.io/jq/tutorial/
```

Capturar: filtros básicos, operadores (`|`, `,`, `?`), funções (`select`, `map`, `reduce`, `keys`, `length`, `to_entries`, `from_entries`), flags (`-r`, `-c`, `-s`, `-e`, `--arg`, `--argjson`), comportamento de exit code.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "jq — processor JSON com DSL"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - jq
  - json
aliases:
  - jq
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"jq é processor JSON com DSL própria — pipeline de filtros (`|`), seleção (`select`), transformação (`map`), agregação (`reduce`). Lê JSON do stdin, escreve JSON do stdout. Flag `-r` emite strings sem aspas (essencial pra pipar pra cd/ssh); `-s` agrupa inputs num array; `-e` retorna exit não-zero quando filtro vazio. Essencial pra qualquer fluxo com API REST ou kubectl."

**O que é / Como funciona** (H3s):

### Filosofia: filtros componentes em pipeline
- Cada filtro recebe um valor e emite zero, um ou mais valores
- Pipe (`|`) encadeia filtros (como shell pipe, mas pra JSON)
- Lazy stream: jq processa input-por-input, não carrega tudo na memória

### Filtros essenciais
- `.` — identity (input inteiro)
- `.foo` — campo `foo` do objeto
- `.foo.bar` — encadeado
- `.[0]` — primeiro item do array
- `.[]` — iterar pelos itens do array (vira stream)
- `.foo?` — opcional (não erra se campo não existe)

### Operadores
- `|` — pipe (resultado vai pro próximo filtro)
- `,` — comma (combina outputs; resultado é vários valores)
- `+`, `-`, `*`, `/` — aritmética / merge de objetos

### Funções built-in importantes
- `select(cond)` — filtra (passa só items onde cond é true)
- `map(f)` — aplica `f` a cada item do array
- `reduce` — fold com acumulador
- `keys`, `values`, `length`, `type`
- `to_entries`, `from_entries` — converter objeto ↔ array de `{key, value}`

### Flags principais
- `-r` (raw output) — emite strings sem aspas externas
- `-c` (compact) — uma linha por valor
- `-s` (slurp) — agrupa todos os inputs num único array
- `-e` (exit) — exit code não-zero se output é vazio/null/false
- `--arg name value` — injeta string
- `--argjson name value` — injeta JSON (number, bool, object)

### Exit code semantics
- Default: exit 0 sempre que parsing OK
- `-e`: exit 1 se output é `null`, `false`, ou vazio. Útil em scripts.

**Na prática** (H3s):

### Receitas básicas
```bash
# Identity (pretty-print JSON)
curl -s https://api.example.com/v1/users | jq .

# Selecionar campo
echo '{"name":"alice","age":30}' | jq '.name'           # "alice"
echo '{"name":"alice","age":30}' | jq -r '.name'        # alice (sem aspas)

# Iterar array
echo '[1,2,3]' | jq '.[]'                                # 1\n2\n3

# Filtrar com select
jq '.users[] | select(.active)'

# Transformar com map
jq '.users | map({id, email})'

# Extrair lista de strings (raw)
jq -r '.users[].email'
```

### Receitas avançadas
```bash
# Injetar variável (string)
jq --arg user alice '.users[] | select(.name == $user)'

# Injetar JSON (objeto)
jq --argjson filter '{"active":true}' '.users[] | select(. == $filter)'

# Slurp (juntar múltiplos JSONs em array)
jq -s 'add' file1.json file2.json

# Exit code útil em script
if curl -s https://api/health | jq -e '.ok == true'; then
    echo "healthy"
fi

# Converter objeto pra CSV (raw + interpolation)
jq -r '.users[] | [.name, .email, .age] | @csv'

# Agregação com reduce
jq '[.items[].price] | reduce .[] as $p (0; . + $p)'
```

### Versão hedged
- jq 1.7+; verifique `jq --version`

**Armadilhas (≥5, bold-label):**

### (1) `-r` faltando — strings com aspas quebram pipe
**Causa:** sem `-r`, jq emite strings JSON com aspas externas (`"alice"` em vez de `alice`).
**Sintoma:** `cd "$(jq '.path' file)"` recebe `"/home/alice"` com aspas e falha.
**Como detectar:** output visualmente tem aspas; consumer falha.
**Solução:** quando o output é texto pro pipe (cd, ssh, xargs), SEMPRE usar `-r`. Manter sem `-r` quando consumer espera JSON.

### (2) `select` vs `map` confundidos
**Causa:** `select(cond)` filtra (mantém ou descarta); `map(f)` transforma cada item.
**Sintoma:** "queria filtrar mas tudo mudou" ou vice-versa.
**Como detectar:** ler o filtro com calma — `select` retorna o item ou nada; `map` retorna SEMPRE algo.
**Solução:** mnemonic — `select` é como `filter`/`where`; `map` é como `transform`. Combinar: `.users | map(select(.active))`.

### (3) `null` em chave faltante vs erro
**Causa:** `.foo` em objeto sem `foo` retorna `null` (não erra); `.foo.bar` em objeto sem `foo` retorna error.
**Sintoma:** "Cannot index null with string \"bar\"".
**Como detectar:** stack trace do jq.
**Solução:** usar `?` opcional: `.foo?.bar?` retorna `null` em vez de errar. Ou `select(.foo) | .foo.bar`.

### (4) Números float vs int — perda de precisão
**Causa:** jq trata todos os números como float64 (IEEE 754); inteiros grandes (Twitter IDs, timestamps em ns) perdem precisão.
**Sintoma:** ID `123456789012345678` vira `123456789012345700`.
**Como detectar:** comparar input vs output de número grande.
**Solução:** se precisa preservar precisão, manter como string no JSON (`"id": "123..."`) ou usar gojq/yq que lidam com bigint.

### (5) UTF-8 BOM no input quebra parser
**Causa:** alguns Windows tools (PowerShell) prefixam BOM (`EF BB BF`) em JSON; jq não tolera.
**Sintoma:** "parse error: Invalid numeric literal" na primeira linha.
**Como detectar:** `xxd file.json | head -1` mostra `efbb bf` no início.
**Solução:** strip BOM antes: `sed '1s/^\xef\xbb\xbf//' file.json | jq ...` ou converter com `iconv -f UTF-8-BOM -t UTF-8`.

### (6) `-s` slurp em stream gigante engole memória
**Causa:** `-s` agrupa TUDO num array; em log streaming gigante, jq tenta carregar tudo.
**Sintoma:** OOM ou jq travado em arquivo enorme.
**Como detectar:** memória do processo jq subindo monotonicamente.
**Solução:** processar streaming sem `-s` quando possível. Pra agregação realmente precisa, usar `reduce` que é incremental.

**Em inglês (8-10):**
Termos: filter pipeline, raw output, slurp, select, map, reduce, exit code, identity, projection, interpolation.

**Veja também:**
- [[08 - yq — processor YAML e as duas implementações]] — par natural pra YAML
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — composição capstone
- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — `rg --json | jq` pra análise estruturada
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#jq|jq]]
- [[Dicionário do Terminal#raw output (jq -r)|raw output (jq -r)]]
- [[Dicionário do Terminal#slurp (jq -s)|slurp (jq -s)]]

**Referências:**
- jq manual: https://jqlang.github.io/jq/manual/
- jq tutorial: https://jqlang.github.io/jq/tutorial/

- [ ] **Step 4: 3 verbetes pro Dicionário**

```markdown
### jq
Processor JSON com DSL própria — pipeline de filtros (`|`), seleção (`select`), transformação (`map`), agregação (`reduce`). Lê JSON do stdin, escreve JSON do stdout. Streaming-friendly (processa input-por-input). Pinned em 1.7+; flag `--version` confirma. Filtros: `.foo`, `.[]`, `.[0]`, `.foo?` (opcional). Funções: `select`, `map`, `reduce`, `keys`, `to_entries`.

Veja também: [[07 - jq — processor JSON com DSL]], [[13 - Pipeline JSON e YAML — jq yq fzf]].

### raw output (jq -r)
Flag do jq (`-r` ou `--raw-output`) que emite strings JSON sem aspas externas. Essencial pra pipar pra `cd`, `ssh`, `xargs` — sem `-r`, `"alice"` chega literal com aspas e o consumer falha. Manter sem `-r` apenas quando o consumer espera JSON válido (outro jq, yq, parser).

Veja também: [[07 - jq — processor JSON com DSL]].

### slurp (jq -s)
Flag do jq (`-s` ou `--slurp`) que agrupa TODOS os inputs num único array antes de processar. Útil pra agregar múltiplos JSON documents (`jq -s 'add' a.json b.json`). Cuidado em streams gigantes — carrega tudo na memória; pra agregação em stream prefira `reduce` que é incremental.

Veja também: [[07 - jq — processor JSON com DSL]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/07 - jq — processor JSON com DSL.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/07 - jq — processor JSON com DSL.md"
grep -cE "^### (jq|raw output \(jq -r\)|slurp \(jq -s\))$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥8 wikilinks, 3 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/07 - jq — processor JSON com DSL.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 07 — jq"
```

---

## Task 10: Nota 08 — yq: processor YAML e as duas implementações

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/08 - yq — processor YAML e as duas implementações.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: yq (Go), yq (Python/kislyuk), YAML multi-doc, anchors e aliases (YAML))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://mikefarah.gitbook.io/yq/
WebFetch: https://github.com/kislyuk/yq
WebFetch: https://kislyuk.github.io/yq/
```

Capturar: diferenças concretas de sintaxe entre yq Go (Mike Farah) e yq Python (kislyuk), comportamento com multi-doc, preservação de comments/ordem, anchors/aliases, command de detecção de versão.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "yq — processor YAML e as duas implementações"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - yq
  - yaml
aliases:
  - yq
  - yq Go
  - yq Python
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"yq processa YAML/JSON/XML — mas existem **duas implementações populares com sintaxe diferente**: Mike Farah (Go, default em Homebrew) e kislyuk (Python, wrappa jq). Confundir as duas é o footgun central — exemplos da web frequentemente não rodam por serem da outra impl. Detectar versão: `yq --version`. Receita segura pra Go: usar sintaxe própria. Pra Python: sintaxe = jq mas operando em YAML."

**O que é / Como funciona** (H3s):

### As duas implementações
| Aspecto | yq (Go) — Mike Farah | yq (Python) — kislyuk |
|---|---|---|
| Linguagem | Go | Python (wrappa jq nativo) |
| Default install | Homebrew, snap | pip, apt em Debian/Ubuntu |
| Sintaxe | Própria, estilo jq mas ≠ | Idêntica a jq |
| In-place edit | `yq -i '.foo = "bar"' file.yaml` | não nativo (script) |
| Multi-doc | `yq eval-all` | menos completo |
| Preservação comments | sim (em casos) | não |
| Anchors/aliases YAML | expandidos por default | comportamento custom |

### Detectar qual está instalado
```bash
yq --version
# yq Go: "yq (https://github.com/mikefarah/yq/) version v4.x.x"
# yq Python: "yq 3.x.x"
```

### Sintaxe yq (Go) — exemplos canônicos
```bash
# Ler campo
yq '.spec.template.spec.containers[0].image' deployment.yaml

# Modificar in-place
yq -i '.image = "nginx:latest"' file.yaml

# Converter YAML → JSON
yq -o json file.yaml

# Multi-doc — processar TODOS os documentos
yq eval-all '. as $item ireduce ({}; . * $item)' *.yaml

# Adicionar elemento a array
yq '.items += ["novo"]' file.yaml
```

### Sintaxe yq (Python) — exemplos canônicos
```bash
# Sintaxe = jq (pq wrappa jq)
yq '.spec.template.spec.containers[0].image' deployment.yaml

# Converter YAML → JSON (default; -y mantém YAML)
yq '.spec' deployment.yaml      # output JSON
yq -y '.spec' deployment.yaml   # output YAML

# In-place requer script ad-hoc
yq -y '.image = "nginx:latest"' file.yaml > tmp && mv tmp file.yaml
```

### Conversão YAML ↔ JSON pra usar com jq (Go)
```bash
# YAML → JSON via yq Go, depois jq
yq -o json values.yaml | jq '.global.image'
```

### Multi-doc (`---`)
```yaml
# file.yaml
---
name: alice
---
name: bob
```
- yq Go: `yq '.name' file.yaml` retorna `alice` E `bob` (cada doc)
- yq Python: pode precisar `yq --slurp '.[].name'` (varia versão)

**Na prática** (H3s):

### Receitas Go (Mike Farah)
```bash
# Listar imagens de um deployment Kubernetes
yq '.spec.template.spec.containers[].image' k8s/deploy.yaml

# Modificar versão in-place
yq -i '.image = "myapp:v2.3.0"' deploy.yaml

# Merge multi-doc (kustomize-style)
yq eval-all '. as $item ireduce ({}; . * $item)' base.yaml overlay.yaml

# Comparar dois YAMLs (output diff-friendly)
yq -o json a.yaml > /tmp/a.json
yq -o json b.yaml > /tmp/b.json
diff <(jq -S . /tmp/a.json) <(jq -S . /tmp/b.json)
```

### Receitas Python (kislyuk)
```bash
# Filtrar com sintaxe jq mas output YAML
yq -y '.users[] | select(.active)' users.yaml

# Converter pra processar com jq (output JSON default)
yq '.metrics' app.yaml | jq '.cpu_threshold'
```

### Decidir qual usar
- **Go**: padrão em Homebrew/asdf; melhor pra k8s, kustomize, helm values; preserva comments melhor; suporte multi-doc rico.
- **Python**: se já usa jq intensivamente e quer reutilizar a sintaxe; instalação leve via pip.
- Em time / projeto: **fixar uma** e documentar. Mixar gera confusão.

### Versão hedged
- yq Go 4.x+; yq Python 3.x+; verifique `yq --version` localmente

**Armadilhas (≥5, bold-label):**

### (1) Confundir as duas impls — receita não funciona
**Causa:** copiar exemplo da web (StackOverflow, blog) sem checar qual yq é.
**Sintoma:** comando dá erro de sintaxe; output inesperado.
**Como detectar:** `yq --version` — Go fala "v4.x.x" (com `v`); Python fala "3.x.x" (sem `v`, número menor).
**Solução:** sempre prefaciar receitas internas com "[yq Go]" ou "[yq Python]". Usar a impl que seu time padronizou. Em scripts CI, validar versão antes de rodar.

### (2) Preservação de comments difere
**Causa:** edição in-place pode descartar comments dependendo de impl/versão.
**Sintoma:** comments somem após `yq -i ...`.
**Como detectar:** diff antes/depois mostra perda de comments.
**Solução:** yq Go preserva melhor que Python; verificar versão (recentes preservam mais). Pra comments críticos, considerar ferramentas dedicadas (`ruamel.yaml` em Python).

### (3) Multi-doc (`---`) suporte ≠ entre impls
**Causa:** YAML multi-doc é feature comum em k8s/CI; impls tratam diferente.
**Sintoma:** comando que funciona em arquivo single-doc falha em multi-doc.
**Como detectar:** rodar `yq '.name' multidoc.yaml` — Go retorna múltiplos; Python varia.
**Solução:** yq Go: usar `yq eval-all` pra processar todos os docs juntos. yq Python: usar `--slurp` pra agregar. Documentar abordagem por impl.

### (4) Anchors e aliases YAML — comportamento opaco
**Causa:** `&anchor`/`*anchor` permitem reuso; yq tipicamente EXPANDE no parse (resolve aliases).
**Sintoma:** output não tem mais `&`/`*` — o YAML "perde" estrutura.
**Como detectar:** input tem `&base` e `*base`; output só tem valores duplicados.
**Solução:** se precisa preservar anchors, ler doc da impl (flags como `--no-anchor-name` em yq Go). Aceitar expansão como default na maioria dos pipelines.

### (5) Instalar acidentalmente a impl errada
**Causa:** `apt install yq` em Debian/Ubuntu instala Python (kislyuk); `brew install yq` instala Go; `pip install yq` instala Python.
**Sintoma:** scripts copiados pra outra máquina falham; sintaxe esperada não bate.
**Como detectar:** comparar `yq --version` entre máquinas.
**Solução:** documentar qual impl em README/dotfiles. Pra Go em Debian: `wget https://github.com/mikefarah/yq/releases/...` (binário direto) ou snap.

### (6) yq Python output default = JSON (não YAML)
**Causa:** kislyuk converte YAML→JSON internamente pra usar jq; output default é JSON.
**Sintoma:** rodar `yq '.foo' file.yaml` retorna JSON, surpreende quem esperava YAML.
**Como detectar:** output entre `{}`/`""`/`[]` puros, sem indentação YAML.
**Solução:** usar flag `-y` (yaml output) em yq Python: `yq -y '.foo' file.yaml`. Em yq Go não precisa — output default já é YAML.

**Em inglês (8-10):**
Termos: implementation, fork, multi-document, anchor, alias, in-place edit, parser, conversion, preserve, expand.

**Veja também:**
- [[07 - jq — processor JSON com DSL]] — base do yq Python; complementa yq Go via conversão
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — composição capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#yq (Go)|yq (Go)]]
- [[Dicionário do Terminal#yq (Python/kislyuk)|yq (Python/kislyuk)]]
- [[Dicionário do Terminal#YAML multi-doc|YAML multi-doc]]
- [[Dicionário do Terminal#anchors e aliases (YAML)|anchors e aliases (YAML)]]

**Referências:**
- yq Go (Mike Farah): https://mikefarah.gitbook.io/yq/
- yq Python (kislyuk): https://github.com/kislyuk/yq
- yq Python doc: https://kislyuk.github.io/yq/

- [ ] **Step 4: 4 verbetes pro Dicionário**

```markdown
### anchors e aliases (YAML)
Mecanismo YAML pra reusar nós: `&name` define anchor; `*name` referencia (alias). Útil em config DRY (definir defaults uma vez, referenciar em vários lugares). Comportamento ao processar com yq: tipicamente expandido por default (anchor vira valor duplicado no output); preservação depende de impl e flags.

Veja também: [[08 - yq — processor YAML e as duas implementações]].

### YAML multi-doc
Múltiplos documentos YAML em um arquivo, separados por `---` (e opcionalmente `...` no fim de cada). Comum em manifests Kubernetes (vários resources num arquivo) e CI configs. Processar com yq Go: `yq eval-all` itera todos. Com yq Python: usar `--slurp` pra agregar em array. Splitter clássico: `csplit` ou `yq -s '.[]'`.

Veja também: [[08 - yq — processor YAML e as duas implementações]].

### yq (Go)
Impl yq de Mike Farah, em Go. Default em Homebrew e snap. Sintaxe própria (estilo jq mas ≠). Preserva comments melhor que Python; suporte rico a multi-doc (`eval-all`); in-place nativo (`-i`). Output default = YAML. Versão `v4.x+`. Padrão em fluxos Kubernetes, kustomize, helm.

Veja também: [[08 - yq — processor YAML e as duas implementações]], [[13 - Pipeline JSON e YAML — jq yq fzf]].

### yq (Python/kislyuk)
Impl yq de Andrey Kislyuk, em Python — wrappa jq nativo. Default em `pip install yq` e em alguns Debian/Ubuntu. Sintaxe **idêntica a jq** (boa pra quem já usa jq). Output default = JSON (use `-y` pra YAML). Versão `3.x+`. Menos comum em fluxos k8s/helm; comum em pipelines onde já se usa jq pesado.

Veja também: [[08 - yq — processor YAML e as duas implementações]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/08 - yq — processor YAML e as duas implementações.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/08 - yq — processor YAML e as duas implementações.md"
grep -cE "^### (anchors e aliases \(YAML\)|YAML multi-doc|yq \(Go\)|yq \(Python/kislyuk\))$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥8 wikilinks, 4 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/08 - yq — processor YAML e as duas implementações.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 08 — yq"
```

---

## Task 11: Nota 09 — tldr e cheat: docs práticas em fluxo

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/09 - tldr e cheat — docs práticas em fluxo.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: tldr-pages, cheatsheet)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://tldr.sh/
WebFetch: https://github.com/tldr-pages/tldr
WebFetch: https://github.com/cheat/cheat
```

Capturar: clientes tldr disponíveis (tealdeer, tldr-rust, original node), comando `tldr --update`, cache offline, cheat Go vs Python (legado), location dos sheets.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "tldr e cheat — docs práticas em fluxo"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - tldr
  - cheat
  - docs
aliases:
  - tldr
  - cheat
  - tldr-pages
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"tldr-pages é coleção comunitária de pages curtas (1 tela, comandos de exemplo); `cheat` é cheatsheet local + customizável (você cria/edita pra workflows próprios). Complementam man — man tem invariantes e edge cases; tldr/cheat respondem "como uso isso AGORA". Múltiplos clientes tldr (tealdeer em Rust é rápido); cheat tem versão Go ativa (Python é legado)."

**O que é / Como funciona** (H3s):

### Por que duas ferramentas (não escolha)
- **tldr-pages**: doc comunitária, padronizada; útil pra ferramentas conhecidas
- **cheat**: cheatsheet local; útil pra workflows seus (kubernetes commands de produção, queries SQL repetidas, etc.)
- **man**: invariantes; precisão; edge cases — não substituível

### tldr-pages
- Repo central: github.com/tldr-pages/tldr
- Pages em markdown simples; uma página por comando
- Estrutura: comando, descrição curta (2-3 linhas), 5-10 exemplos típicos
- Cliente baixa do CDN e cacheia local
- `tldr --update` atualiza cache

### Clientes tldr (escolher um)
- **tealdeer** (Rust) — rápido, single binary, mantido
- **tldr-rust** — outro em Rust
- **tldr (Node original)** — referência, mais lento
- **tldr-py** — Python

### cheat (workflow local)
- Cheatsheets em `~/.config/cheat/cheatsheets/personal/`
- Community sheets em `~/.config/cheat/cheatsheets/community/` (cloned do repo)
- Search: `cheat -s <pattern>`
- Edit: `cheat -e <name>` abre no `$EDITOR`
- Tags pra organizar (`tags: kubernetes,production`)

### Versão histórica do cheat
- **cheat Go** (cheat/cheat) — versão atual mantida desde 2018
- **cheat Python** (chrisallenlane/cheat) — versão original, **descontinuada**
- Confundir as duas é armadilha real (sintaxe e config dirs diferem)

### Quando cada uma vence
| Pergunta | Resposta |
|---|---|
| "Como faço operação genérica X em comando Y conhecido?" | tldr |
| "Comando completo que eu uso no meu workflow específico?" | cheat (próprio) |
| "Detalhes de TODAS as flags, edge cases, invariantes?" | man |
| "Tô offline, sem cache do tldr" | cheat local OR man |

**Na prática** (H3s):

### Setup tldr (assumindo tealdeer)
```bash
# Install tealdeer
# Update cache
tldr --update

# Uso
tldr tar
tldr docker run

# Idioma específico (default = en)
tldr -L pt_BR tar

# Listar plataformas disponíveis
tldr --list-platforms
```

### Setup cheat
```bash
# Install cheat (Go version)
# Init configs
cheat --init > ~/.config/cheat/conf.yml

# Criar cheatsheet pessoal
cheat -e mycheat
# Editor abre arquivo em ~/.config/cheat/cheatsheets/personal/mycheat
# Conteúdo exemplo:
# ---
# tags: [git, daily]
# ---
# # Rebase interativo das últimas 5 commits
# git rebase -i HEAD~5
#
# # Reset hard pra remoto
# git reset --hard origin/main

# Buscar
cheat -s rebase     # search por palavra
cheat mycheat       # ver cheatsheet específico
cheat -l            # listar todos
```

### Receitas
```bash
# Pipeline tldr → fzf pra navegar
tldr --list | fzf --preview 'tldr {}'

# Cheat com fzf
ls ~/.config/cheat/cheatsheets/personal/ | fzf --preview 'cheat {}'

# Adicionar tldr ao alias do `?` (zsh function)
function ? { tldr "$@"; }
```

### Versões hedged
- tealdeer 1.6+ (cliente tldr); verifique `tldr --version`
- cheat 4.4+ (Go version); verifique `cheat --version`

**Armadilhas (≥5, bold-label):**

### (1) tldr-pages desatualizada ou incompleta
**Causa:** tldr é comunidade; pages podem refletir versão antiga do comando ou estar incompletas.
**Sintoma:** receita do tldr não funciona; flag mudou.
**Como detectar:** comparar com `--help` da ferramenta.
**Solução:** considerar tldr como ponto de partida, não verdade absoluta. Contribuir fix via PR (tldr-pages aceita facilmente).

### (2) cheat Go vs cheat Python (legado)
**Causa:** `pip install cheat` ainda instala versão Python descontinuada.
**Sintoma:** comandos diferem (`cheat -l` vs `cheatsheets`); paths de config diferem (`~/.cheat/` vs `~/.config/cheat/`).
**Como detectar:** `cheat --version` — Go fala "cheat 4.x"; Python é mais antigo, layout diferente.
**Solução:** instalar Go version (binário direto do repo cheat/cheat ou `brew install cheat`). Documentar em dotfiles qual usar.

### (3) Cache local de tldr quebrado/antigo
**Causa:** `--update` não foi rodado faz semanas; cache obsoleto.
**Sintoma:** pages aparecem antigas; novos comandos não constam.
**Como detectar:** olhar timestamp em `~/.cache/tldr/` ou similar.
**Solução:** `tldr --update` periodicamente (cron semanal opcional). Tealdeer tem `auto_update_interval_hours` na config.

### (4) Traduções tldr inconsistentes com inglês
**Causa:** pages PT/ES/etc. são traduzidas por voluntários; podem estar desatualizadas vs en.
**Sintoma:** flag mencionada na PT-BR não existe mais; só em en.
**Como detectar:** comparar `-L en` com `-L pt_BR`.
**Solução:** preferir `-L en` como source-of-truth; usar traduções pra contexto rápido apenas.

### (5) Achar que tldr substitui man
**Causa:** tldr é resumo; man é referência completa.
**Sintoma:** receita básica funciona; edge case ou flag específica não está documentada no tldr.
**Como detectar:** procurar flag avançada e não encontrar.
**Solução:** usar tldr pra start rápido; cair em man pra detalhes (flags com semantics não-óbvias, exit codes, env vars). `MANPAGER` com bat (nota 03) torna man menos doloroso.

### (6) Cheatsheets pessoais não versionados — perda em troca de máquina
**Causa:** `~/.config/cheat/cheatsheets/personal/` não foi adicionado ao repo de dotfiles.
**Sintoma:** ao mudar de máquina, cheatsheets pessoais somem.
**Como detectar:** clonar dotfiles em VM; verificar se `cheat -l` retorna seus sheets.
**Solução:** incluir `~/.config/cheat/cheatsheets/personal/` no manager de dotfiles (stow/chezmoi/bare repo). Community sheets viram via git clone separado (pesados, mudam pouco).

**Em inglês (8-10):**
Termos: documentation, cheatsheet, manpage, community-driven, cache, offline, command reference, example-driven, deprecated, fork.

**Veja também:**
- [[03 - bat — cat moderno com syntax highlight]] — `MANPAGER` com bat pra manpages bonitas
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#tldr-pages|tldr-pages]]
- [[Dicionário do Terminal#cheatsheet|cheatsheet]]
- [[Dicionário do Terminal#MANPAGER|MANPAGER]]

**Referências:**
- tldr-pages: https://tldr.sh/
- tldr-pages repo: https://github.com/tldr-pages/tldr
- cheat repo: https://github.com/cheat/cheat

- [ ] **Step 4: 2 verbetes pro Dicionário**

```markdown
### cheatsheet
Folha de uso prático curta e runnable — comandos comuns com 1-3 linhas de contexto cada. Diferente de manpage (referência exaustiva) e tldr (community-driven, genérica): cheatsheet é local + customizável. Ferramenta `cheat` mantém em `~/.config/cheat/cheatsheets/personal/`; também há cheat.sh (online). Útil pra workflows pessoais repetitivos.

Veja também: [[09 - tldr e cheat — docs práticas em fluxo]].

### tldr-pages
Repo comunitário de pages curtas (uma tela, 5-10 exemplos por comando) — github.com/tldr-pages/tldr. Cliente CLI (`tldr`, `tealdeer`, etc.) baixa pages e cacheia local. Cobertura: comandos populares (git, docker, kubectl, tar). Incompleto pra ferramentas obscuras. Traduções por voluntários (PT-BR, ES, etc.) podem estar desatualizadas vs inglês.

Veja também: [[09 - tldr e cheat — docs práticas em fluxo]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/09 - tldr e cheat — docs práticas em fluxo.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/09 - tldr e cheat — docs práticas em fluxo.md"
grep -cE "^### (cheatsheet|tldr-pages)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥7 wikilinks, 2 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/09 - tldr e cheat — docs práticas em fluxo.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 09 — tldr e cheat"
```

---

## Task 12: Nota 10 — delta: pager moderno pra git diff

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/10 - delta — pager moderno pra git diff.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: delta, OSC 8)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/dandavison/delta
WebFetch: https://dandavison.github.io/delta/
```

Capturar: config em `~/.gitconfig`, features (`navigate`, `side-by-side`, `line-numbers`, `hyperlinks`), `[interactive] diffFilter`, presets, integração com bat themes (`syntax-theme`), modo standalone (`diff a b | delta`).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "delta — pager moderno pra git diff"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - delta
  - git
aliases:
  - delta
  - git-delta
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"delta é pager especializado em git diff/show/log/blame, com syntax highlight (syntect, igual bat), side-by-side opcional, navegação por keys (n/N entre hunks), hyperlinks OSC 8 (terminais modernos), preservação de cores. Configurado no `~/.gitconfig`. Standalone funciona em diff puro também. Para fluxos de revisão de PR no terminal, transforma `git diff` de cinza/preto pra leitura humana."

**O que é / Como funciona** (H3s):

### Filosofia: pager especializado pra git
- Engine syntect (mesma do bat) — highlight em ~150 linguagens
- Recebe input estilo `git diff` (com headers `+`/`-`, paths, ranges)
- Reformata visualmente: cores, line numbers, navegação, hyperlinks

### Features (todas opcionais, ativadas no config)
- `navigate` — n/N pulam entre hunks; muito útil em diff grande
- `side-by-side` — antes/depois lado a lado (precisa terminal largo)
- `line-numbers` — numeração nas duas colunas
- `hyperlinks` — OSC 8 escape sequences viram links clicáveis (em terminais que suportam)
- `syntax-theme` — tema syntax (compartilha temas bat)
- `decorations` — preset combinado (file/hunk headers visuais)

### Config em gitconfig
```toml
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    light = false                # false = fundo escuro
    side-by-side = true
    line-numbers = true
    syntax-theme = Dracula
    hyperlinks = true
    features = decorations

[merge]
    conflictStyle = diff3        # ajuda delta render melhor

[diff]
    colorMoved = default         # detecta linhas movidas
```

### `[interactive] diffFilter` — afeta `git add -p`
- Sem isso: `git add -p` (patch interativo) usa pager default (cru)
- Com isso: chunks que aparecem em `git add -p` ficam coloridos

### Modo standalone
```bash
diff -u a.txt b.txt | delta
# Útil pra diff fora do git
```

### Hyperlinks OSC 8 (terminais que suportam)
- kitty, wezterm, recent gnome-terminal, recent iTerm
- File:line do diff vira link clicável (abre no editor configurado)
- Em terminais sem suporte: hyperlinks viram texto literal (`file://...`) — pode ser feio

**Na prática** (H3s):

### Setup inicial
```bash
# Install delta (binário Rust)
# Configurar gitconfig
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.side-by-side true
git config --global delta.line-numbers true
git config --global delta.syntax-theme "Dracula"

# Verificar
git diff HEAD~1
```

### Receitas
```bash
# Diff comum
git diff
git diff HEAD~5

# Show de commit
git show <hash>

# Log com diffs (cuidado com volume)
git log -p --max-count=3

# Standalone (sem git)
diff -u file_a file_b | delta

# Comparar dois branches lado a lado
git diff main..feature -- src/
```

### Integrar com bat themes
- `bat --list-themes` mostra themes disponíveis
- `delta.syntax-theme = <nome>` no gitconfig
- Mesmos themes funcionam (engine compartilhada)

### Comparação: delta vs diff-so-fancy vs git-pager default
- **default (less)**: cinza/preto/vermelho/verde; sem syntax; navegação limitada
- **diff-so-fancy**: melhoria sobre default; sem syntax; sem side-by-side
- **delta**: syntax highlight; side-by-side; navegação; hyperlinks; mais features

### Versão hedged
- delta 0.16+; verifique `delta --version`

**Armadilhas (≥5, bold-label):**

### (1) Config errada no gitconfig é silenciosa
**Causa:** typo em `[delta]` section ou key — delta não roda; git cai pra less default.
**Sintoma:** `git diff` aparece sem syntax (cru, listras vermelhas/verdes).
**Como detectar:** `git config --get core.pager` mostra esperado? `delta --version` instalado?
**Solução:** copiar config do README oficial; testar com `git diff HEAD~1` em repo conhecido. Se falhar, isolar: `git -c core.pager=delta diff` força.

### (2) Side-by-side em terminal estreito
**Causa:** `side-by-side = true` precisa ~180 colunas; em terminal de 100 colunas, fica cortado.
**Sintoma:** linhas truncadas; pior que single-column.
**Como detectar:** `tput cols` mostra largura.
**Solução:** condicional — só side-by-side em monitor wide. Ou deixar `false` global e usar `git -c delta.side-by-side=true diff` quando precisa.

### (3) Hyperlinks OSC 8 viram literal em terminal sem suporte
**Causa:** terminal antigo (gnome-terminal pré-3.40, alacritty antigo, screen) não interpreta OSC 8.
**Sintoma:** vê `]8;;file://...^G` no diff.
**Como detectar:** ler diff e ver texto estranho onde deveria ter link.
**Solução:** desativar em terminais sem suporte: `[delta] hyperlinks = false`. Detectar terminal: `$TERM`, `$TERM_PROGRAM`.

### (4) Performance em diff gigante
**Causa:** delta aplica highlight + reformatação; em diff de milhares de linhas, custa.
**Sintoma:** `git log -p` em repo grande lento.
**Como detectar:** comparar com `git --no-pager log -p` vs `git log -p`.
**Solução:** `[delta] max-line-length = 512` (linhas mais longas viram cru). Ou usar pager raw temporário: `git --no-pager diff`.

### (5) Conflito com outras configs de pager
**Causa:** `[pager]` section no gitconfig tem entries customizadas (`pager.diff = something`); sobrescrevem `core.pager`.
**Sintoma:** `git diff` usa pager X; `git show` usa pager Y; inconsistente.
**Como detectar:** `git config --get-all pager.*`.
**Solução:** garantir `core.pager = delta` E `[pager] diff = delta, log = delta, show = delta` consistentes — ou remover overrides específicos.

### (6) `colorMoved` em diff style não bate com tema delta
**Causa:** `[diff] colorMoved = zebra` ou `dimmed-zebra` colore linhas movidas com cores que conflitam com tema delta.
**Sintoma:** linhas movidas em cor estranha (e.g. magenta sobre azul) — ilegível.
**Como detectar:** diff com refactor (linhas movidas) usando tema escuro mostra cores feias.
**Solução:** ajustar `[delta] map-styles` pra remapear cores; ou usar `colorMoved = default` (delta lida bem).

**Em inglês (8-10):**
Termos: pager, syntax highlight, side-by-side, hyperlink, escape sequence, navigation, hunk, decoration, theme, refactor detection.

**Veja também:**
- [[03 - bat — cat moderno com syntax highlight]] — engine compartilhada (syntect); temas comuns
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|TUIs (galho 4)]] — Lazygit usa delta como pager opcionalmente
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#delta|delta]]
- [[Dicionário do Terminal#OSC 8|OSC 8]]
- [[Dicionário do Terminal#syntax pager|syntax pager]]
- [[Dicionário do Terminal#BAT_THEME|BAT_THEME]] — temas compartilháveis

**Referências:**
- delta repo: https://github.com/dandavison/delta
- delta doc: https://dandavison.github.io/delta/

- [ ] **Step 4: 2 verbetes pro Dicionário**

```markdown
### delta
Pager moderno especializado em git diff/show/log/blame, com syntax highlight (engine syntect, igual bat), side-by-side opcional, navegação por n/N entre hunks, hyperlinks OSC 8 em terminais que suportam. Configurado no `~/.gitconfig` (`[core] pager = delta`, `[interactive] diffFilter`, `[delta] features = ...`). Standalone também funciona (`diff a b | delta`).

Veja também: [[10 - delta — pager moderno pra git diff]].

### OSC 8
Escape sequence ANSI (Operating System Command 8) que define hyperlinks clicáveis em terminais que suportam. Formato: `ESC ] 8 ; ; URL BEL texto ESC ] 8 ; ; BEL`. Terminais com suporte: kitty, wezterm, recent gnome-terminal, recent iTerm. Em terminais sem suporte aparece como texto literal corrompido.

Veja também: [[10 - delta — pager moderno pra git diff]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/10 - delta — pager moderno pra git diff.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/10 - delta — pager moderno pra git diff.md"
grep -cE "^### (delta|OSC 8)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥8 wikilinks, 2 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/10 - delta — pager moderno pra git diff.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 10 — delta"
```

---

## Task 13: Nota 11 — Monitores e disco (btop + htop + dust)

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/11 - Monitores e disco — btop htop dust.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: btop, htop, dust)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/aristocratos/btop
WebFetch: https://htop.dev/
WebFetch: https://github.com/bootandy/dust
```

Capturar: flags principais (btop `--tty_on`, htop `-d`/`-u`/`-p`, dust `-d`/`-n`/`--ignore-directory`), confirmar comportamento de dust quanto a .gitignore (Task 0).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Monitores e disco — btop, htop, dust"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - btop
  - htop
  - dust
  - monitoring
aliases:
  - btop
  - htop
  - dust
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Três ferramentas pra observabilidade local: **btop** (TUI moderna, gráficos, mouse), **htop** (clássico leve, ubíquo em servidores), **dust** (du moderno em árvore por tamanho). htop pra ssh em servidor minimalista; btop pra workstation rica; dust pra responder "quem comeu meu disco?". Todos lêem /proc (Linux) ou equivalente; nenhum precisa root pra uso comum."

**O que é / Como funciona** (H3s):

### btop — monitor moderno
- TUI rica: CPU/RAM/disk/network com gráficos, processos, sensors
- Mouse-aware: click pra ordenar coluna, scroll
- Temas customizáveis (`~/.config/btop/themes/`)
- Config persistente em `~/.config/btop/btop.conf`
- Modo TTY (`--tty_on`) pra ssh com bandwidth baixo

### htop — clássico leve
- TUI simples, ubíqua (instalada em quase qualquer Linux server)
- F-keys: F2 setup, F3 search, F4 filter, F5 tree view, F9 kill, F10 quit
- Suporta árvore de processos (parent → children)
- Filtros por user, command
- Mínimo footprint — bom em servidor com poucos recursos

### dust — du moderno
- du em árvore visual: barras horizontais mostram proporção
- Default: top N (algo como 30) maiores; `-n <num>` ajusta
- `-d <num>` profundidade máxima
- `--ignore-directory <nome>` pula pasta específica
- Output colorido por padrão

### Comparação btop vs htop
| Aspecto | btop | htop |
|---|---|---|
| Visual | Rico (gráficos, mouse) | Simples (barras, listas) |
| Resource overhead | Maior (~20-50MB RAM) | Mínimo (~5MB) |
| Customização | Themes, layout flexível | Config básica |
| ssh em servidor minimalista | --tty_on funciona | Default OK |
| Workstation moderna | Default ótimo | Funciona, sub-utiliza terminal |

### Quando cada um vence
- **htop em ssh:** server slow, bandwidth limitado, "matar processo rápido"
- **btop em workstation:** monitorar build local, ver IO/network em gráfico, mouse-friendly
- **dust em disco cheio:** identificar pasta culpada rapidamente

**Na prática** (H3s):

### Setup
```bash
# btop config (gerado no primeiro run)
btop                                  # cria ~/.config/btop/btop.conf

# htop config (sem state — só config interativo)
htop                                  # cria ~/.config/htop/htoprc após F10 com mudanças

# dust não tem config persistente — flags por invocação
```

### Receitas comuns
```bash
# Top 30 maiores pastas, profundidade 3
dust -d 3 -n 30 ~

# Excluir pastas custosas
dust -d 2 --ignore-directory node_modules --ignore-directory .git ~

# htop com refresh 1s, só processos do user atual
htop -d 1 -u $USER

# btop em modo TTY (ssh resource-baixo)
btop --tty_on

# Buscar processo no htop: F3, digitar nome, Enter
# Matar no htop: F9, escolher signal (default SIGTERM, 9=SIGKILL)
```

### Aliases sugeridos
```bash
alias top=btop                        # se você sempre quer btop em interativo
alias du-disk='dust -d 3 -n 30'
```

### Persistência de config (dotfiles)
- **btop**: `~/.config/btop/btop.conf` pode ir nos dotfiles, mas é OS-específico (paths absolutos podem aparecer)
- **htop**: `~/.config/htop/htoprc` é portável; gere em uma máquina, replique
- **dust**: sem config; flags por uso

### Versão hedged
- btop 1.3+; htop 3.x+; dust 1.x+; verifique versões localmente

**Armadilhas (≥5, bold-label):**

### (1) btop em ssh com bandwidth baixo
**Causa:** btop default usa muitos chars Unicode pra gráficos; em conexão lenta, refresh lag.
**Sintoma:** btop fica congelado por segundos a cada update.
**Como detectar:** ssh com `-vvv` mostra latência alta.
**Solução:** rodar com `btop --tty_on` (modo TTY-friendly, menos chars). Ou usar htop em servidor remoto.

### (2) htop kill em árvore pode matar processo errado
**Causa:** F5 tree view mostra hierarquia; F9 (kill) na pasta-pai não mata children pelo PID parent — mas matar parent pode deixar children órfãos (init adopt).
**Sintoma:** processo mau-comportado continua rodando após "kill no parent".
**Como detectar:** após kill, `ps aux` mostra child ainda ativo.
**Solução:** entender o problema: pra matar grupo, usar PGID (`kill -- -$PGID`) ou rodar `pkill -P <ppid>`. htop em si só kill por PID.

### (3) dust e .gitignore — verificar comportamento atual
**Causa (a confirmar no Task 0):** dust pode ou não respeitar `.gitignore` por default.
**Sintoma:** output infla com `node_modules/`, `target/`, etc. — pasta inocente parece grande.
**Como detectar:** rodar `dust -d 2 .` em projeto com node_modules; ver se aparece.
**Solução:** usar `--ignore-directory node_modules --ignore-directory .git --ignore-directory target` no alias default. Se dust adicionar `--gitignore` no futuro, atualizar.

### (4) btop config persistido em dotfiles com paths absolutos
**Causa:** btop salva paths de logs, themes customizados em `btop.conf` — paths absolutos da máquina origem.
**Sintoma:** ao copiar config pra outra máquina, btop falha em achar log/theme paths.
**Como detectar:** abrir `btop.conf` e procurar paths que começam com `/`.
**Solução:** versionar só keys portáveis (theme padrão, cores), ou regenerar config em cada máquina. Ou usar chezmoi templates pra paths.

### (5) Contagem RAM Linux ≠ "memória disponível" intuitiva
**Causa:** Linux conta cache+buffers como "usado" pra fins de free, mas `available` (kernel ≥ 3.14) é o que realmente importa.
**Sintoma:** htop mostra 90% RAM "usada"; mas sistema responde bem (cache, não app).
**Como detectar:** comparar `free -h` (used) vs (available).
**Solução:** confiar em `available`, não `used`. htop modo "free memory" mostra parecido com `free -h`; btop tem visualização separada de cache vs realmente-usado.

### (6) Confundir RSS / VSZ no kill decision
**Causa:** RSS (resident set size — RAM real) vs VSZ (virtual — endereço alocado, pode não usar) — kill por VSZ alto pode matar inocente.
**Sintoma:** processo com VSZ enorme parece "comilão" mas RSS é pequeno (lazy allocation).
**Como detectar:** htop mostra ambos (M_RESIDENT = RSS; M_SIZE = VSZ).
**Solução:** priorizar RSS pra decisões de kill por memória. VSZ é só ceiling de endereço.

**Em inglês (8-10):**
Termos: process monitor, memory usage, resident set size, virtual memory, disk usage, tree view, refresh rate, kill signal, available memory, cache.

**Veja também:**
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|TUIs (galho 4)]] — Lazydocker pra inspeção específica de containers (vs btop pra host)
- [[Dicionário do Terminal#btop|btop]]
- [[Dicionário do Terminal#htop|htop]]
- [[Dicionário do Terminal#dust|dust]]

**Referências:**
- btop: https://github.com/aristocratos/btop
- htop: https://htop.dev/
- dust: https://github.com/bootandy/dust

- [ ] **Step 4: 3 verbetes pro Dicionário**

```markdown
### btop
Monitor de sistema TUI moderno em C++ — gráficos coloridos pra CPU/RAM/disk/network, mouse-aware, themes customizáveis. Sucessor espiritual de bashtop/bpytop (mesma família). Config persistente em `~/.config/btop/btop.conf`. Modo `--tty_on` pra ssh com bandwidth limitado. Resource overhead maior que htop (~20-50MB RAM).

Veja também: [[11 - Monitores e disco — btop htop dust]].

### dust
du moderno em Rust por bootandy — visualização em árvore por tamanho com barras horizontais coloridas. Default mostra top N maiores (~30); `-n` ajusta; `-d` limita profundidade; `--ignore-directory` pula pastas. Não tem config persistente; flags por invocação. Útil pra responder "quem comeu meu disco?" rapidamente.

Veja também: [[11 - Monitores e disco — btop htop dust]].

### htop
Monitor clássico de processos com TUI — desenvolvido desde 2004, ubíquo em servidores Linux. F-keys (F2 setup, F3 search, F5 tree, F9 kill, F10 quit). Footprint mínimo (~5MB RAM). Filtros por user/command. Config em `~/.config/htop/htoprc`. Ainda recomendado pra ssh em servidor minimalista — btop é overkill em conexão lenta.

Veja também: [[11 - Monitores e disco — btop htop dust]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/11 - Monitores e disco — btop htop dust.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/11 - Monitores e disco — btop htop dust.md"
grep -cE "^### (btop|dust|htop)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥7 wikilinks, 3 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/11 - Monitores e disco — btop htop dust.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 11 — Monitores e disco"
```

---

## Task 14: Nota 12 — Stack interativo (fzf + zoxide + atuin)

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/12 - Stack interativo — fzf zoxide atuin.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: zsh widget)

- [ ] **Step 1: Pesquisa-âncora**

Sem novas fetches obrigatórias (docs já foram fetched em Tasks 3, 7, 8). Focar em **patterns de composição** — buscar especificamente:

```
WebFetch: https://github.com/junegunn/fzf#tips (se ainda não foi)
```

Procurar "Tips" / "Examples" / "Wiki" pra patterns de composição entre fzf e outras ferramentas.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Stack interativo — fzf zoxide atuin"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - fzf
  - zoxide
  - atuin
  - composicao
aliases:
  - Stack interativo
  - fzf zoxide atuin
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Capstone — fzf + zoxide + atuin compondo o fluxo diário. zoxide pula pastas via frecency; atuin substitui Ctrl-R com fuzzy search rico; fzf é motor de seleção compartilhado (zi usa fzf; atuin tem TUI próxima). Init order importa: atuin DEPOIS de plugins zsh que mexem em Ctrl-R; zoxide pode vir antes. `FZF_DEFAULT_OPTS` aplicado em todos. Assume leitura das notas 01, 05, 06."

**O que é / Como funciona** (H3s):

### As três peças do quebra-cabeça
- **zoxide** — "para onde ir" (pastas)
- **atuin** — "o que eu fiz antes" (history)
- **fzf** — "como escolher rapidamente" (selecionar item)

Sozinhas, cada uma resolve um problema; juntas, viram o loop:
1. `z proj` — pular pra pasta do projeto
2. `Ctrl-R "deploy"` — recuperar último deploy via atuin
3. `Ctrl-T` ou `**<TAB>` — completar paths via fzf

### Init order no shell (importa)
```bash
# ~/.zshrc — order matters

# 1. Plugin manager (oh-my-zsh, zinit, prezto) — primeiro de tudo
source ~/.config/zinit/zinit.zsh

# 2. Plugins (autosuggestions, syntax-highlighting, completions)
zinit light zsh-users/zsh-autosuggestions
zinit light zdharma-continuum/fast-syntax-highlighting

# 3. zoxide — antes de atuin é OK; antes ou depois de fzf não importa muito
eval "$(zoxide init zsh)"

# 4. atuin — DEPOIS de plugins que mexem em Ctrl-R
eval "$(atuin init zsh)"

# 5. fzf bindings — opcionalmente DEPOIS de atuin (ordem depende: atuin sobrescreve Ctrl-R; fzf pode adicionar Ctrl-T/Alt-C)
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

### Compartilhar config visual com FZF_DEFAULT_OPTS
```bash
export FZF_DEFAULT_OPTS="
  --height 60%
  --layout=reverse
  --border=rounded
  --preview-window=right:60%:wrap
  --bind 'ctrl-/:toggle-preview'
"
```

Atuin não usa FZF_DEFAULT_OPTS diretamente (TUI própria), mas tem opções equivalentes em `~/.config/atuin/config.toml` (`inline_height`, `style`).

### Composição em receitas

**Pular pra pasta + escolher arquivo:**
```bash
cd "$(zoxide query -l | fzf --preview 'eza --tree -L 2 {}')"
nvim "$(fd -t f | fzf --preview 'bat --color=always {}')"
```

**Buscar comando recente filtrado por pasta:**
```bash
atuin search --cwd "$(pwd)" --search-mode fuzzy "git"
```

**Workflow git completo:**
```bash
# Trocar branch via fzf
git checkout "$(git branch --format='%(refname:short)' | fzf --preview 'git log --oneline -10 {}')"

# Achar commit pra cherry-pick
git log --oneline | fzf --preview 'git show --color {1}' | awk '{print $1}'
```

### Convergência: por que esse stack
- Todas as 3 são Rust (binários standalone, sem deps runtime)
- Todas defendem TTY-aware behavior (funcionam em pipe sem quebrar)
- Todas usam frecency-like ranking em algum lugar (zoxide explicit; atuin pra ordering interno)

**Na prática** (H3s):

### Setup do zero em máquina nova
```bash
# Instalar via package manager preferido
# Adicionar ao ~/.zshrc na ordem certa (ver Step 3 acima)

# Importar histórico zsh pro atuin
atuin import zsh

# Verificar bindings
bindkey '^R'                # deve mostrar atuin widget
bindkey '^T'                # deve mostrar fzf widget

# Treinar zoxide (rodar cd manualmente nos primeiros dias)
cd ~/work/myproj
cd ~/personal/dotfiles
# Em alguns dias, `z proj` já funciona
```

### Configurações finas

**Atuin sem auto-sync (manual):**
```toml
# ~/.config/atuin/config.toml
auto_sync = false
search_mode = "fuzzy"
inline_height = 25
style = "compact"
```

**zoxide com `cd` substituído:**
```bash
eval "$(zoxide init zsh --cmd cd)"
# Agora `cd foo` é zoxide search; `cd /caminho/absoluto` ainda funciona
# Trade-off: mais ergonômico; menos óbvio quando vê script seu
```

**FZF customizado pra cada binding:**
```bash
export FZF_CTRL_T_OPTS="--preview 'bat --color=always {}'"
export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window=down:3:hidden"
export FZF_ALT_C_OPTS="--preview 'eza --tree -L 2 {}'"
```

### Versão hedged
Verifique versões instaladas localmente; stack assume:
- fzf 0.4x+, zoxide 0.9+, atuin 18+

**Armadilhas (≥5, bold-label):**

### (1) Init order quebra Ctrl-R
**Causa:** plugin Zsh (oh-my-zsh, fast-syntax-highlighting) que mexe em Ctrl-R carregado DEPOIS do `atuin init`.
**Sintoma:** Ctrl-R abre history clássico, não atuin TUI.
**Como detectar:** `bindkey '^R'` retorna `_history-incremental-search-backward` ou widget de outro plugin.
**Solução:** mover `eval "$(atuin init zsh)"` pro FIM do `.zshrc`, depois de tudo. Ou usar `precmd` hook.

### (2) zsh widget collisions
**Causa:** zoxide, atuin e plugin manager tentam definir o mesmo widget name (raro mas acontece).
**Sintoma:** binding intermitente; mensagem `widget already defined` no startup.
**Como detectar:** `zsh -lic exit 2>&1 | grep -i widget`.
**Solução:** ler logs de startup; renomear widget conflitante (raro precisar). Geralmente init order resolve.

### (3) `FZF_DEFAULT_OPTS` com preview pesado lentando tudo
**Causa:** colocar `--preview 'bat ...'` em `FZF_DEFAULT_OPTS` aplica em TODA invocação fzf — inclusive Ctrl-R (que mostra comandos, não files).
**Sintoma:** Ctrl-R lento; preview de comandos tenta bat e quebra.
**Como detectar:** ver lag em Ctrl-R; preview vazio ou estranho.
**Solução:** **NÃO** colocar `--preview` em `FZF_DEFAULT_OPTS`. Usar `FZF_CTRL_T_OPTS` pra preview de files; deixar Ctrl-R limpo.

### (4) atuin e zoxide ambos rastreando "lugares" — mental model
**Causa:** atuin rastreia cwd em cada comando; zoxide rastreia cwd em cada cd. Semântica diferente.
**Sintoma:** "atuin search --cwd /foo" mostra comandos rodados ali; "z foo" pula pra `/foo` mais frecente.
**Como detectar:** entender propósitos diferentes.
**Solução:** mental model: zoxide = "onde ir"; atuin = "o que fiz onde". Não competem; complementam.

### (5) Reinstalar shell init silently breaks
**Causa:** trocar shell ou reinstalar dotfiles pode sobrescrever `.zshrc` sem os `eval init` das ferramentas.
**Sintoma:** próximo shell aberto não tem `z`, Ctrl-R clássico voltou.
**Como detectar:** `command -v z` falha; `bindkey '^R'` aponta pra widget default.
**Solução:** dotfiles versionados (galho 5) com `.zshrc` controlado. Bootstrap script (galho 5 nota 08) reaplica configs e roda `eval init`s.

### (6) atuin sync com self-host quebra após troca de domínio/IP
**Causa:** `sync_address` no atuin config tem IP/hostname antigo do self-host; mudou e config não foi atualizada.
**Sintoma:** `atuin sync` retorna erro de connection refused ou DNS.
**Como detectar:** `atuin sync` logs explícitos.
**Solução:** atualizar `sync_address` em `~/.config/atuin/config.toml`. Se key ainda válida, sync resume; se nova instância sem dados, restaurar via backup `~/.local/share/atuin/history.db`.

**Em inglês (8-10):**
Termos: init order, widget, key binding, frecency, composition, capstone, fuzzy search, history, working directory, env var.

**Veja também:**
- [[01 - fzf — fuzzy finder universal]] — motor de seleção
- [[05 - zoxide — cd inteligente com frecency]] — pastas via frecency
- [[06 - atuin — history shell com SQLite e sync]] — history rico
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — outro capstone (composição em dados estruturados)
- [[03-Dominios/Tecnologia/Terminal/Shell/index|Shell (galho 2)]] — Zsh + OMZ; base pros init scripts
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#zsh widget|zsh widget]]
- [[Dicionário do Terminal#init script (shell)|init script (shell)]]
- [[Dicionário do Terminal#FZF_DEFAULT_OPTS|FZF_DEFAULT_OPTS]]
- [[Dicionário do Terminal#frecency|frecency]]

**Referências:**
- fzf wiki: https://github.com/junegunn/fzf/wiki
- zoxide wiki: https://github.com/ajeetdsouza/zoxide/wiki
- atuin docs: https://docs.atuin.sh/

- [ ] **Step 4: 1 verbete pro Dicionário**

```markdown
### zsh widget
Função zsh registrada via `zle -N <nome>` pra responder a uma keypress (binding via `bindkey '^R' <nome>`). zoxide, atuin, fzf usam widgets pra inserir/sobrescrever Ctrl-R, Ctrl-T, Alt-C. Conflitos surgem quando duas ferramentas tentam definir o mesmo widget. Order matters: o último init wins.

Veja também: [[12 - Stack interativo — fzf zoxide atuin]], [[06 - atuin — history shell com SQLite e sync]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/12 - Stack interativo — fzf zoxide atuin.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/12 - Stack interativo — fzf zoxide atuin.md"
grep -cE "^### zsh widget$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥11 wikilinks (mais que outras notas — capstone linka muito), 1 verbete visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/12 - Stack interativo — fzf zoxide atuin.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 12 — Stack interativo"
```

---

## Task 15: Nota 13 — Pipeline JSON e YAML (jq + yq + fzf)

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/CLI Utils/13 - Pipeline JSON e YAML — jq yq fzf.md`
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (verbetes: pipefail, xargs -r)

- [ ] **Step 1: Pesquisa-âncora**

Sem novas fetches obrigatórias (jq/yq já feitas em Tasks 9, 10). Confirmar:

```
WebFetch: https://kubernetes.io/docs/reference/kubectl/jsonpath/ (pra referência cruzada jq vs kubectl jsonpath)
```

Capturar: `set -o pipefail` (bash spec), `xargs -r` (GNU extension), kubectl `-o json|yaml` flags.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Pipeline JSON e YAML — jq yq fzf"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - jq
  - yq
  - fzf
  - pipeline
aliases:
  - Pipeline JSON YAML
  - jq yq fzf
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Capstone — receitas reais de pipeline composto pra processar dados estruturados no fluxo cotidiano. `curl | jq | fzf` pra explorar API; `kubectl get -o json | jq` pra filtrar k8s; `yq -o json | jq` pra usar yq Go com sintaxe jq downstream; error handling com `set -o pipefail` + `jq -e`. Assume leitura das notas 07 (jq) e 08 (yq)."

**O que é / Como funciona** (H3s):

### Por que composição
- jq sozinho: transformações JSON elegantes
- yq sozinho: transformações YAML
- fzf sozinho: seleção interativa
- Juntos: pipeline reativo que filtra → escolhe → age

### Os três padrões
1. **Explorar**: `<fonte JSON/YAML> | jq <filtro> | fzf` — selecionar item
2. **Modificar**: `<fonte> | yq -o json | jq <transform> | <consumer>` — pipeline de transformação
3. **Acionar**: `<seleção> | xargs <comando>` — agir sobre seleção

### Error handling em pipes
```bash
set -euo pipefail              # standard prelude
# -e: exit em erro
# -u: erro em variável não-definida
# -o pipefail: pipe falha se QUALQUER comando do pipe falhar

# Sem pipefail: curl_falha | jq retorna sucesso (jq nem viu)
# Com pipefail: pipeline detecta falha do curl
```

### `jq -e` em scripts
```bash
# -e: exit 1 se output é null/false/vazio
if curl -sf https://api/health | jq -e '.ok == true' >/dev/null; then
    echo "healthy"
fi
```

### `xargs -r` (GNU) ou `xargs --no-run-if-empty`
- Default xargs: lista vazia → executa comando sem args (comportamento indefinido)
- `-r`: lista vazia → não roda nada (mais seguro)

**Na prática** (H3s):

### Explorar API REST
```bash
# GitHub: listar issues open do repo
curl -s https://api.github.com/repos/cli/cli/issues | \
  jq -r '.[] | "\(.number)\t\(.title)"' | \
  fzf --delimiter='\t' --with-nth=2 --preview 'echo {1}'

# Selecionar e ver detalhes
issue_number=$(curl -s https://api.github.com/repos/cli/cli/issues | \
  jq -r '.[] | "\(.number)\t\(.title)"' | \
  fzf | awk -F'\t' '{print $1}')

curl -s "https://api.github.com/repos/cli/cli/issues/${issue_number}" | jq .
```

### Filtrar k8s resources (assume kubectl configurado)
```bash
# Pods com status NotReady em todos os namespaces
kubectl get pods --all-namespaces -o json | \
  jq -r '.items[] | select(.status.containerStatuses[]?.ready == false) |
         "\(.metadata.namespace)\t\(.metadata.name)"'

# Imagens únicas de deployments
kubectl get deploy -A -o json | \
  jq -r '.items[].spec.template.spec.containers[].image' | \
  sort -u

# Selecionar pod interativamente pra exec
pod=$(kubectl get pods -o json | \
  jq -r '.items[].metadata.name' | \
  fzf --preview "kubectl describe pod {}")
kubectl exec -it "$pod" -- bash
```

### YAML → JSON pra pipeline com jq (Go)
```bash
# values.yaml (Helm) → extrair imagem com jq
yq -o json values.yaml | jq '.global.image'

# Diff de dois YAMLs
diff <(yq -o json --indent=2 a.yaml | jq -S .) \
     <(yq -o json --indent=2 b.yaml | jq -S .)

# Multi-doc YAML → array JSON
yq -o json eval-all '. as $i ireduce ([]; . + [$i])' multidoc.yaml | jq '.[0]'
```

### Script robusto com error handling
```bash
#!/usr/bin/env bash
set -euo pipefail

API="https://api.example.com/v1"

# curl falha → pipeline falha (pipefail)
users=$(curl -sf "$API/users")

# jq -re: erro se não achar
admin_id=$(echo "$users" | jq -re '.users[] | select(.role == "admin") | .id' | head -1) || {
    echo "ERR: no admin found" >&2
    exit 1
}

# xargs -r evita executar com input vazio
echo "$users" | jq -r '.users[].email' | xargs -r -n1 echo "Notifying:"
```

### Receitas avançadas
```bash
# jq + parallel pra processamento concorrente
cat large.json | jq -c '.items[]' | parallel -j 4 'echo {} | jq -r .id | xargs process-item'

# yq pra atualizar versão em vários files
fd -t f -e yaml -x yq -i '.image = "myapp:v2.3.0"' {}

# Comparar k8s manifests antes/depois de deploy
kubectl get deployment myapp -o json > before.json
kubectl apply -f new-deploy.yaml
kubectl get deployment myapp -o json > after.json
diff <(jq -S '.spec' before.json) <(jq -S '.spec' after.json) | delta
```

**Armadilhas (≥5, bold-label):**

### (1) Pipe sem `set -o pipefail` mascara falhas
**Causa:** default shell — exit code do pipeline é do ÚLTIMO comando; `cmd_falha | jq` retorna sucesso (jq não falhou).
**Sintoma:** script "termina OK" mas resultado errado.
**Como detectar:** desligar pipefail e ver script "ter sucesso" mesmo com curl 404.
**Solução:** SEMPRE `set -o pipefail` em scripts. Idealmente `set -euo pipefail` no topo.

### (2) `jq -e` surpreendendo com null/false
**Causa:** `-e` retorna exit ≠ 0 quando output é null/false/vazio. Útil mas vira armadilha se você esperava só "vazio".
**Sintoma:** script falha pq jq filter retornou `false` (não null).
**Como detectar:** `echo '{"x":false}' | jq -e '.x'; echo $?` mostra 1.
**Solução:** entender: `-e` é "output é truthy?". Se quer só "tem output?", use `jq` sem `-e` + `grep -q .` ou check `[[ -n "$result" ]]`.

### (3) `kubectl -o json` vs `-o yaml` mudam parser downstream
**Causa:** copiar receita "kubectl ... | jq" mas usar `-o yaml` por engano — jq não parse YAML.
**Sintoma:** "parse error: Invalid numeric literal".
**Como detectar:** primeira linha do output não é JSON válido.
**Solução:** combinar coerentemente — `-o json | jq` ou `-o yaml | yq` (Go) ou `-o yaml | yq | jq` (Python wrappa).

### (4) `xargs` sem `-r` em lista vazia executa comando vazio
**Causa:** lista vazia → xargs executa `cmd` sem args, com semantics indefinida (alguns comandos rodam vazio; outros falham).
**Sintoma:** comportamento estranho em pipeline com filtro que pode resultar vazio.
**Como detectar:** `echo '' | xargs ls` lista diretório atual (surpresa).
**Solução:** SEMPRE `xargs -r` em scripts (GNU extension; macOS pode precisar `--no-run-if-empty`).

### (5) Binary safety no preview fzf com jq output
**Causa:** jq emite JSON binary-safe, mas piping pra cat/preview sem cuidado pode quebrar terminal se valor contém chars de controle.
**Sintoma:** terminal corrompido após fzf preview de JSON com chars exóticos.
**Como detectar:** ver `\x1b` ou `\x07` no output.
**Solução:** usar `bat --color=always` no preview (lida com binary detection); ou sanitizar com `jq -c | tr -cd '\n[:print:]'`.

### (6) jq float64 perde precisão em IDs grandes
**Causa:** mesmo de nota 07 (jq armadilha 4) — IDs `int64` (Twitter, Snowflake) viram float; perde dígitos.
**Sintoma:** ID `1234567890123456789` vira `1234567890123456800`.
**Como detectar:** comparar input vs output em IDs grandes.
**Solução:** preservar como string no JSON original; ou usar `--raw-input --raw-output -R` pra IDs como strings. Em pipelines com Twitter/Snowflake, manter `id` como string sempre.

**Em inglês (8-10):**
Termos: pipeline, error handling, exit code, pipefail, structured data, JSON, YAML, conversion, interactive selection, batch processing.

**Veja também:**
- [[07 - jq — processor JSON com DSL]] — base
- [[08 - yq — processor YAML e as duas implementações]] — base
- [[01 - fzf — fuzzy finder universal]] — motor de seleção
- [[12 - Stack interativo — fzf zoxide atuin]] — outro capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#pipefail|pipefail]]
- [[Dicionário do Terminal#xargs -r|xargs -r]]
- [[Dicionário do Terminal#jq|jq]]
- [[Dicionário do Terminal#yq (Go)|yq (Go)]]
- [[Dicionário do Terminal#raw output (jq -r)|raw output (jq -r)]]

**Referências:**
- jq manual: https://jqlang.github.io/jq/manual/
- yq Go: https://mikefarah.gitbook.io/yq/
- kubectl JSONPath: https://kubernetes.io/docs/reference/kubectl/jsonpath/ (referência cruzada)

- [ ] **Step 4: 2 verbetes pro Dicionário**

```markdown
### pipefail
Opção do shell bash/zsh (`set -o pipefail`) que faz o exit code de um pipeline refletir falha em QUALQUER estágio, não só no último. Sem pipefail: `cmd_falha | jq` retorna sucesso (jq não falhou). Com pipefail: pipeline propaga erro. Combinar com `set -euo pipefail` (errexit + nounset + pipefail) como prelude padrão de scripts robustos.

Veja também: [[13 - Pipeline JSON e YAML — jq yq fzf]].

### xargs -r
Flag GNU do `xargs` (também `--no-run-if-empty`) que evita executar o comando quando a lista de entrada é vazia. Default do xargs: executa comando sem args mesmo em lista vazia — semantics indefinida (`ls` lista cwd; `rm` falha). Sempre usar em scripts. macOS pode precisar `--no-run-if-empty` (BSD xargs).

Veja também: [[13 - Pipeline JSON e YAML — jq yq fzf]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Tecnologia/Terminal/CLI Utils/13 - Pipeline JSON e YAML — jq yq fzf.md"
grep -c '\[\[' "03-Dominios/Tecnologia/Terminal/CLI Utils/13 - Pipeline JSON e YAML — jq yq fzf.md"
grep -cE "^### (pipefail|xargs -r)$" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥11 wikilinks, 2 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/13 - Pipeline JSON e YAML — jq yq fzf.md" "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-cli-utils): add nota 13 — Pipeline JSON e YAML"
```

---

## Task 16: Pass final no MOC do galho

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/CLI Utils/index.md`

- [ ] **Step 1: Conferir que todos os wikilinks resolvem**

```bash
ls "03-Dominios/Tecnologia/Terminal/CLI Utils/"
```

Esperado: 13 arquivos `.md` (notas) + `index.md` = 14 arquivos.

- [ ] **Step 2: Substituir placeholders de versão**

No `index.md`, bloco "Versões assumidas": trocar `<VERSAO_*>` pelos valores reais capturados no Task 0. Usar `Edit` por placeholder.

Exemplo:
- `<VERSAO_FZF>` → `0.48+ (verifique localmente)`
- `<VERSAO_RG>` → `14.1.0 (sistema de referência)`
- ...

- [ ] **Step 3: Bumpa `updated:`**

Frontmatter `updated:` → `2026-05-22` (já correto se MOC foi criado hoje; só confirmar).

- [ ] **Step 4: Validação**

```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  "03-Dominios/Tecnologia/Terminal/CLI Utils/index.md" --respect-public-only
```

Esperado: 0 broken links.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/CLI Utils/index.md"
git commit -m "docs(terminal-cli-utils): pass final no MOC do galho"
```

---

## Task 17: Pass final no Dicionário

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Verificar verbetes presentes**

```bash
grep -cE "^### " "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
# Esperado: total ≈ 119 (pré-existente) + 40 (galho 6) ≈ 159
```

Listar verbetes do bloco CLI Utils:
```bash
awk '/^## CLI Utils$/,/^## [^C]/' "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md" | grep -cE "^### "
# Esperado: ≈ 40
```

- [ ] **Step 2: Conferir ordem alfabética case-insensitive**

```bash
awk '/^## CLI Utils$/,0' "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md" | \
  grep -E "^### " | sed 's/^### //' > /tmp/cli-utils-actual.txt
sort -f /tmp/cli-utils-actual.txt > /tmp/cli-utils-sorted.txt
diff /tmp/cli-utils-actual.txt /tmp/cli-utils-sorted.txt
```

Esperado: diff vazio (já em ordem alfabética).

Se houver entries fora de ordem, usar Edit pra reordenar.

- [ ] **Step 3: Conferir ausência de duplicatas com outros blocos**

```bash
# Lista todos os verbetes (todos os ###); detectar duplicatas
grep -E "^### " "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md" | sort | uniq -d
```

Esperado: vazio (sem duplicatas).

- [ ] **Step 4: Confirmar "Veja também" em todos os verbetes do bloco**

```bash
awk '/^## CLI Utils$/,/^## [^C]/' "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md" | \
  awk '/^### / {term=$0; veja=0} /^Veja também/ {veja=1} /^### / && veja==0 && NR>1 {print "MISSING veja em:", term}'
```

Esperado: nenhum verbete sem "Veja também".

- [ ] **Step 5: Bumpa `updated:` no frontmatter**

Edit: `updated: 2026-05-22`.

- [ ] **Step 6: Commit (só se houve alterações)**

```bash
git status --short "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
# Se modificado:
git add "03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md"
git commit -m "docs(terminal-cli-utils): pass final no Dicionário"
```

Se não houve alterações (já estava correto), pular commit.

---

## Task 18: Tronco com wikilink ativo

**Files:**
- Modify: `03-Dominios/Tecnologia/Terminal/index.md`

- [ ] **Step 1: Localizar placeholder**

```bash
grep -n "CLI Utils — galho 6 (planejado)" "03-Dominios/Tecnologia/Terminal/index.md"
```

Esperado: linha 32 com `- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…`.

- [ ] **Step 2: Substituir por wikilink ativo**

Use `Edit`:
- `old_string`: `- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…`
- `new_string`: `- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|CLI Utils]] — galho 6: substituições modernas de utilitários UNIX (cat/ls/grep/find/du/top) + fluxo interativo (fzf/zoxide/atuin) + processamento estruturado (jq/yq)`

- [ ] **Step 3: Confirmar galhos 1-5 ainda corretos**

```bash
grep -E "^- \[\[" "03-Dominios/Tecnologia/Terminal/index.md" | head -6
```

Esperado: 6 entradas com wikilinks ativos pros galhos 1-6 (Editor, Shell, Multiplexer, TUIs, Dotfiles, CLI Utils); galho 7 ainda como placeholder.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Tecnologia/Terminal/index.md"
git commit -m "feat(terminal): tronco com wikilink ativo pro galho 6 (CLI Utils)"
```

---

## Task 19: Validação final + cross-task review

**Files:** (nenhum direto; cross-task review pode produzir fixes)

- [ ] **Step 1: Validar wikilinks na pasta inteira**

```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  "03-Dominios/Tecnologia/Terminal/CLI Utils/" --respect-public-only
```

Esperado: 0 broken links.

Se houver broken: investigar caso-a-caso, corrigir com Edit, re-rodar.

- [ ] **Step 2: Dispatch cross-task review subagent (paralelo)**

Dispatcher lê todas as 13 notas e checa consistência. Prompt do subagent:

> Leia as 13 notas em `03-Dominios/Tecnologia/Terminal/CLI Utils/` (01 a 13). Para cada uma, valide:
>
> 1. **Code fences fechadas** — toda ` ``` ` tem par fechando. Contar ` ``` ` em cada arquivo: deve ser par.
> 2. **Armadilhas em formato bold-label** — cada armadilha tem `### (N) Título` + 4 labels (`**Causa:**`, `**Sintoma:**`, `**Como detectar:**`, `**Solução:**`). NUNCA callouts Obsidian (`> [!warning]`). NUNCA tabela.
> 3. **"Em inglês" em bullets bilíngues** — formato `- **PT** — *EN*. "frase técnica em PT."`. NUNCA tabela.
> 4. **"Veja também" sem backticks em wikilinks** — `[[link]]`, NÃO `` `[[link]]` ``.
> 5. **MOC + tronco em "Veja também"** — `[[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]` e `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]` presentes.
> 6. **TL;DR em callout `> [!abstract] TL;DR`** — NÃO H2 nem texto solto.
> 7. **Versões hedged** — sem pins específicos no corpo (ex: "fzf 0.4x+" OK; "fzf 0.48.0" não).
> 8. **Sem fabricação** — sem `josenaldo`, sem `/home/josenaldo/`, sem "no meu setup".
> 9. **Notas 12 e 13** — verificar que NÃO duplicam conteúdo das notas individuais (07, 08 pro 13; 01, 05, 06 pro 12). Devem focar em **composição**, não re-explicação.
> 10. **Frontmatter completo** — `title`, `created`, `updated`, `type`, `status`, `publish`, `fase`, `tags`, `aliases`.
>
> Classifique findings: **Critical** (quebra padrão ou estrutura), **Important** (degrada qualidade), **Nit** (cosmético).
>
> Reportar em formato de tabela: `arquivo | classificação | problema | linha (se aplicável)`.

- [ ] **Step 3: Se cross-task review reportou Critical ou Important — dispatch fix subagent**

Prompt do fix subagent:

> Receba a lista de findings Critical/Important do cross-task review do galho 6 — CLI Utils. Para cada finding:
>
> 1. Ler o arquivo
> 2. Aplicar correção mínima (preserva conteúdo; só corrige o problema apontado)
> 3. Re-validar
>
> Após todos os fixes, fazer commit único:
>
> ```bash
> git add <arquivos modificados>
> git commit -m "fix(terminal-cli-utils): cross-task — <resumo dos fixes>"
> ```
>
> NUNCA usar `git add -A`. Stage explícito por arquivo.

- [ ] **Step 4: Validação pós-fix**

```bash
# Re-rodar verificar-wikilinks
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  "03-Dominios/Tecnologia/Terminal/CLI Utils/" --respect-public-only

# Conferir commits sem Co-Authored-By Claude
git log --since="6 hours ago" --grep="Co-Authored-By" --oneline
```

Esperado: 0 broken links; nenhum commit com `Co-Authored-By: Claude`.

- [ ] **Step 5: Sumário final**

Verificar critério de pronto:
- [ ] 14 arquivos em `03-Dominios/Tecnologia/Terminal/CLI Utils/` (13 notas + MOC)
- [ ] ~40 verbetes novos no bloco `## CLI Utils` do Dicionário
- [ ] Tronco com wikilink ativo pro galho 6
- [ ] `verificar-wikilinks` → 0 broken
- [ ] Zero commits com `Co-Authored-By: Claude`
- [ ] Cross-task review passou sem Critical/Important

Reportar ao usuário: galho 6 entregue, próximo (galho 7 — Workflow) ainda planejado.

---

## Self-review do plano

(seção executada pela writing-plans skill antes de finalizar)

**Spec coverage:**
- ✅ §3.1 (13 notas) → Tasks 3-15
- ✅ §3.2 (MOC) → Task 1 + Task 16 (pass final)
- ✅ §3.3 (~40 verbetes) → integrados nos Steps 4 das Tasks 3-15 + Task 17 (pass final)
- ✅ §3.4 (tronco) → Task 18
- ✅ §4 (convenções) → restrições absolutas no header + Step 3 de cada nota
- ✅ §5 (conteúdo por nota) → embedado em cada task 3-15
- ✅ §6 (pesquisa) → Step 1 de cada nota
- ✅ §7 (execução) → Tasks 0-19
- ✅ §8 (critério de pronto) → Task 19 Step 5
- ✅ §9 (riscos) → tratados em armadilhas das notas E em restrições absolutas + cross-task review

**Placeholder scan:**
- Sem TBDs, TODOs, "implement later".
- `<VERSAO_*>` no MOC é intencional — substituído no Task 16 com valores reais do Task 0.
- "Add appropriate error handling" / "handle edge cases" — não presente; armadilhas concretas em cada nota.

**Type consistency:**
- Nomes de arquivo das notas batem entre o MOC (Task 1), o tronco (Task 18) e as tasks individuais (3-15).
- Wikilinks em "Veja também" entre notas usam consistente formato `[[XX - título]]`.
- Verbetes referenciados em "Veja também" batem com nomes definidos nos Steps 4.

**Decomposição:**
- 13 notas independentes mas com ordem fase-progressiva (Iniciado → Adepto → Magus).
- Notas 12 e 13 (capstones) explicitamente dependem das anteriores — prompt do implementer alerta pra NÃO re-explicar.

Plan complete.

