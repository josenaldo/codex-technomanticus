---
title: "Plano — Execução do Galho 1 da trilha Terminal (Editor / Neovim + LazyVim)"
date: 2026-05-19
status: ready
type: plan
publish: false
---

# Galho 1 da trilha Terminal (Editor) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produzir, em `03-Dominios/Terminal/Editor/`, **13 notas atômicas + 1 MOC do galho** (Iniciado 4 + Adepto 5 + Magus 4) cobrindo Neovim + LazyVim do "abrir e salvar" até "Treesitter queries + DAP". Em paralelo, criar `03-Dominios/Terminal/Dicionário do Terminal.md` (~30 verbetes) e ativar o wikilink do Editor no tronco `03-Dominios/Terminal/index.md`. Todos os arquivos com `publish: true`, PT-BR, com seção "Em inglês" por nota (mini-glossário PT→EN).

**Architecture:** Galho atômico em pasta dedicada, com MOC interno + 13 notas numeradas (`NN - Título.md`). Dicionário do Terminal vive no topo do domínio (`03-Dominios/Terminal/`) — trilha-wide, alimentado conforme as notas referenciam termos. LazyVim é caminho primário em Iniciado/Adepto; Neovim/Vim core domina em Magus. Cada nota segue template híbrido (TL;DR + corpo técnico + "Em inglês" + "Veja também" + "Referências"). Wikilinks densos: nota↔nota, nota→verbete, nota→tronco, MOC→todas as notas. Ordem de execução: por fase (01→04, 05→09, 10→13) com commit por arquivo.

**Tech Stack:** Markdown (Obsidian Flavored), wikilinks Obsidian, callouts, frontmatter YAML, Quartz para publicação. Sem código executável de sistema — code samples são Lua de config Neovim ou comandos Ex/keymaps. Testes locais ocasionais (`nvim --headless` ou `:checkhealth`) em notas que mostram config (04, 06, 08, 09).

**Referências:**
- Spec: `docs/superpowers/specs/2026-05-19-terminal-editor-design.md`
- Roadmap macro: `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`
- Plano-mãe (formato análogo): `docs/superpowers/plans/2026-05-07-node-runtime-event-loop-execution.md`
- Plano do tronco da trilha: `docs/superpowers/plans/2026-05-18-terminal-tronco-execution.md`
- Template de glossário: `03-Dominios/Empreendedorismo/Indie Hacker 101/Dicionário do Indie Hacker.md`
- Tronco Terminal a atualizar no fim: `03-Dominios/Terminal/index.md`

---

## ⚠️ Restrições absolutas

### Fabricação de experiência

A memória [Nunca inventar dados sobre o usuário](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_no_fabrication.md) é regra inegociável. **Nenhuma nota pode atribuir ao autor experiências profissionais, projetos, clientes ou casos não-vividos.**

Para a seção "Na prática" e exemplos:

- "Padrão observado no ecossistema LazyVim/Neovim" — OK
- "Caso típico em projetos TS/JS" — OK
- "Armadilha comum reportada na comunidade (r/neovim, LazyVim Discussions)" — OK
- Citações com fonte verificável (docs oficiais, talks identificadas, repos públicos) — OK
- Hipotéticos explícitos ("Imagine que você está editando um JSON aninhado…") — OK
- "Eu uso isso no meu projeto X em Y empresa" — **PROIBIDO**

Quando faltar contexto factual ou houver dúvida sobre versão/comportamento de plugin, **PERGUNTAR antes de escrever** — nunca preencher com plausibilidade.

### Commits sem Co-Authored-By

A memória [Nao assinar commits](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_commits.md) é regra inegociável. **Nenhum commit deste plano leva `Co-Authored-By: Claude`.** Nem `--no-verify` nem `--no-gpg-sign` salvo pedido explícito.

### Isolamento público/apocrypha

Este galho é 100% público. **Nenhum arquivo aqui pode referenciar conteúdo do apocrypha** — sem wikilinks, paths ou menções. Tudo o que entra é citável publicamente.

### Não remover `index.md` do Quartz

A memória [Nunca remover index.md Quartz](/home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/feedback_quartz_index.md) é regra inegociável. **O `03-Dominios/Terminal/index.md` é editado, nunca removido.** A pasta `Editor/` recebe seu próprio `index.md` como MOC do galho — criar, não substituir nada.

---

## File Structure

16 arquivos novos + 1 modificado:

```
03-Dominios/Terminal/
├── Dicionário do Terminal.md                                     # Task 1 (esqueleto), Task 17 (pass final)
├── index.md                                                       # MODIFICADO (Task 18 — ativa wikilink Editor)
└── Editor/
    ├── index.md                                                   # MOC do galho — Task 2 (esqueleto), Task 16 (pass final)
    ├── 01 - Modal editing.md                                      # Task 3
    ├── 02 - Motions, operadores e text objects.md                 # Task 4
    ├── 03 - Edição e navegação.md                                 # Task 5
    ├── 04 - LazyVim tour.md                                       # Task 6
    ├── 05 - Lua para Neovim.md                                    # Task 7
    ├── 06 - Estrutura de config.md                                # Task 8
    ├── 07 - lazy.nvim.md                                          # Task 9
    ├── 08 - Customizando LazyVim.md                               # Task 10
    ├── 09 - LSP no Neovim.md                                      # Task 11
    ├── 10 - Registers, marks, macros.md                           # Task 12
    ├── 11 - Workflow avançado.md                                  # Task 13
    ├── 12 - Treesitter avançado.md                                # Task 14
    └── 13 - Snippets e DAP.md                                     # Task 15
```

**Tasks finais (16, 17, 18, 19):**
- Pass final no MOC do galho com wikilinks confirmados
- Pass final no Dicionário do Terminal (alfabetização dentro de blocos, "Veja também" por verbete)
- Atualização do tronco `Terminal/index.md` (bullet do Editor vira wikilink ativo)
- Validação final (build Quartz local + verificar wikilinks)

---

## Template padrão por nota

Definido uma vez, aplicado a todas as 13 notas. Variações permitidas estão na seção 6 do spec.

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
  - editor
  - <fase>
  - <tag específica: modal-editing, lsp, treesitter, etc>
aliases:
  - <opcional>
---

# <Título>

> [!abstract] TL;DR
> 2-4 linhas em PT-BR. Conceito + regra prática + por que importa.

## O que é / Como funciona

<1-3 parágrafos. Definição precisa. Pressupõe leitura do MOC do galho ou consulta paralela ao Dicionário.>

## Na prática

<Exemplos concretos: config Lua, keymap, comando Ex, sequência de keys. Para 04, sub-headings por área (Telescope, neo-tree, etc.).>

## Armadilhas

<2+ armadilhas reais reportadas na comunidade ou documentadas. Não genéricas — específicas do tema.>

## Em inglês

<5-10 termos PT → EN. Cada termo com 1 frase curta de uso em contexto técnico (PR review, pair programming, docs).>

Ex:
- **modo normal** — *normal mode*. "Press `Esc` to return to normal mode before typing a command."
- **registrador** — *register*. "Yank the line into register `a` with `\"ay`."

## Veja também

- [[<outra nota do galho>]] — relação
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]
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
- [ ] 2+ exemplos práticos concretos (config Lua, keymap, comando Ex, sequência de keys)
- [ ] Seção "Em inglês" com 5-10 termos PT→EN + 1 frase de uso por termo
- [ ] Seção "Armadilhas" com 2+ casos concretos (não genéricos, com causa+sintoma+como detectar)
- [ ] Wikilinks pros verbetes do Dicionário (lista por nota nas Tasks 3-15, alinhada ao spec §5)
- [ ] Frontmatter completo (`publish: true`, `status: seedling`, `fase: <fase>`, tags consistentes)
- [ ] PT-BR natural; termos técnicos em inglês mantidos (motion, plugin, buffer, register…)
- [ ] **Zero atribuição de experiência pessoal fabricada** ao autor (regra absoluta)
- [ ] Nenhuma alegação técnica não-trivial sem fonte ou exemplo que comprove

---

## Bibliografia centralizada

Consulta rápida durante a escrita. URLs verificadas no spec §5 e §9.

### Fontes canônicas globais

- **Neovim user docs:** `https://neovim.io/doc/user/`
- **LazyVim docs:** `https://www.lazyvim.org/`
- **lazy.nvim docs:** `https://lazy.folke.io/`
- **kickstart.nvim:** `https://github.com/nvim-lua/kickstart.nvim`
- **Awesome Neovim:** `https://github.com/rockerBOO/awesome-neovim`
- **Folke (autor LazyVim/lazy.nvim):** `https://github.com/folke`

### Canais e comunidade

- **TJ DeVries (YouTube — core contributor):** `https://www.youtube.com/@teej_dv`
- **ThePrimeagen (YouTube — workflow):** `https://www.youtube.com/@ThePrimeagen`
- **r/neovim:** `https://www.reddit.com/r/neovim/`
- **LazyVim Discussions:** `https://github.com/LazyVim/LazyVim/discussions`

### Repos chave

- **LazyVim:** `https://github.com/LazyVim/LazyVim`
- **LazyVim starter:** `https://github.com/LazyVim/starter`
- **lazy.nvim:** `https://github.com/folke/lazy.nvim`
- **nvim-treesitter:** `https://github.com/nvim-treesitter/nvim-treesitter`
- **nvim-treesitter-textobjects:** `https://github.com/nvim-treesitter/nvim-treesitter-textobjects`
- **nvim-lspconfig:** `https://github.com/neovim/nvim-lspconfig`
- **mason.nvim:** `https://github.com/williamboman/mason.nvim`
- **nvim-cmp:** `https://github.com/hrsh7th/nvim-cmp`
- **conform.nvim:** `https://github.com/stevearc/conform.nvim`
- **LuaSnip:** `https://github.com/L3MON4D3/LuaSnip`
- **friendly-snippets:** `https://github.com/rafamadriz/friendly-snippets`
- **nvim-dap:** `https://github.com/mfussenegger/nvim-dap`
- **nvim-dap-ui:** `https://github.com/rcarriga/nvim-dap-ui`
- **persistence.nvim:** `https://github.com/folke/persistence.nvim`
- **todo-comments.nvim:** `https://github.com/folke/todo-comments.nvim`

### Livros e long-form

- **Learn Vim (irian.to):** `https://learnvim.irian.to/`
- **Practical Vim (Drew Neil):** `https://pragprog.com/titles/dnvim2/practical-vim-second-edition/`
- **Learn Vimscript the Hard Way (Steve Losh):** `https://learnvimscriptthehardway.stevelosh.com/`
- **Boost your fu (Barbarian Meets Coding):** `https://www.barbarianmeetscoding.com/boost-your-coding-fu-with-vscode-and-vim`

### Lua

- **Lua 5.1 reference:** `https://www.lua.org/manual/5.1/`
- **Learn X in Y minutes — Lua:** `https://learnxinyminutes.com/docs/lua/`
- **:help lua-guide:** `https://neovim.io/doc/user/lua-guide.html`

### Specs externas

- **LSP spec:** `https://microsoft.github.io/language-server-protocol/`
- **DAP spec:** `https://microsoft.github.io/debug-adapter-protocol/`
- **Tree-sitter queries:** `https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries`

---

## Task 0: Pré-flight

**Files:**
- Create: `03-Dominios/Terminal/Editor/` (diretório)

- [ ] **Step 1: Verificar contexto e memórias críticas**

Run:
```bash
cat /home/josenaldo/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/MEMORY.md | grep -iE "fabrica|invent|assinar|commit|quartz|apocrypha"
```

Expected: pelo menos linhas referenciando `feedback_no_fabrication.md`, `feedback_commits.md`, `feedback_quartz_index.md`, `feedback_public_apocrypha_separation.md`. Se faltar alguma, **abortar e pedir reload de memória** antes de prosseguir.

- [ ] **Step 2: Confirmar que tronco e spec existem**

Run:
```bash
test -f "03-Dominios/Terminal/index.md" && echo "ok: tronco existe"
test -f "docs/superpowers/specs/2026-05-19-terminal-editor-design.md" && echo "ok: spec existe"
test ! -d "03-Dominios/Terminal/Editor" && echo "ok: Editor/ ainda não existe" || echo "ATENÇÃO: Editor/ já existe — investigar"
test ! -f "03-Dominios/Terminal/Dicionário do Terminal.md" && echo "ok: Dicionário ainda não existe" || echo "ATENÇÃO: Dicionário já existe — investigar"
```

Expected: 4 linhas `ok:`. Qualquer "ATENÇÃO" = parar e investigar antes de prosseguir (pode ser sessão anterior incompleta).

- [ ] **Step 3: Confirmar branch e working tree limpa**

Run:
```bash
git status --short
git rev-parse --abbrev-ref HEAD
```

Expected: branch `main` e working tree limpa (sem changes pendentes não relacionados). Se houver changes pendentes, decidir com o usuário se commita/stash antes de prosseguir.

- [ ] **Step 4: Criar o diretório `Editor/`**

Run:
```bash
mkdir -p "03-Dominios/Terminal/Editor"
ls -la "03-Dominios/Terminal/Editor"
```

Expected: diretório vazio criado.

- [ ] **Step 5: Sanity check das fontes-âncora principais**

Disparar 3 WebFetch em paralelo para confirmar acessibilidade:

```
WebFetch: https://www.lazyvim.org/
WebFetch: https://lazy.folke.io/
WebFetch: https://neovim.io/doc/user/intro.html
```

Capturar páginas iniciais; se alguma estiver fora do ar, registrar e pesquisar fontes alternativas no momento da nota afetada (não bloquear o galho inteiro).

- [ ] **Step 6: Commit pré-flight**

Como o `mkdir` cria pasta vazia (que git ignora), este task não tem o que commitar isoladamente. **Pular o commit aqui** e seguir direto pra Task 1 — o primeiro commit do galho será do Dicionário esqueleto.

---

## Task 1: Dicionário do Terminal — esqueleto

**Files:**
- Create: `03-Dominios/Terminal/Dicionário do Terminal.md`

**Objetivo:** Criar o glossário no topo do domínio com estrutura por blocos temáticos (sem verbetes ainda — vão sendo preenchidos pelas notas conforme aparecem). Pattern alinhado com `Dicionário do Indie Hacker.md` e `Dicionário de React.md`.

- [ ] **Step 1: Escrever o arquivo**

Criar `03-Dominios/Terminal/Dicionário do Terminal.md` com **exatamente** o conteúdo abaixo:

````markdown
---
title: "Dicionário do Terminal"
created: 2026-05-19
updated: 2026-05-19
type: glossary
status: seedling
aliases: []
tags:
  - glossary
  - terminal
lang: pt
publish: true
---

# Dicionário do Terminal

> Glossário do domínio Terminal: jargão de editor (Neovim, LazyVim, modal editing), shell, multiplexer, TUIs e workflow. Cada verbete é referenciado por uma ou mais notas das trilhas do domínio.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática.
- Verbetes em ordem alfabética dentro de cada bloco.
- Linkar de outra nota: [[Dicionário do Terminal#Nome do termo]]
- Customizar texto exibido: [[Dicionário do Terminal#Nome do termo|texto]]
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Ajuste `lang:` no frontmatter (`pt` ou `en`) — define o idioma das definições.
- Cada verbete tem (i) 1-3 frases de definição em PT-BR e (ii) "Veja também:" com wikilinks para a(s) nota(s) que aprofundam.
-->

## Vim / Neovim core

## Ecossistema LazyVim

## LSP & dev

## Avançado
````

Use `Write` com o conteúdo acima exatamente (inclusive a linha em branco final).

- [ ] **Step 2: Verificar criação e frontmatter**

Run:
```bash
test -f "03-Dominios/Terminal/Dicionário do Terminal.md" && echo "ok: file exists"
wc -l "03-Dominios/Terminal/Dicionário do Terminal.md"
head -16 "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: arquivo existe, ≥25 linhas, frontmatter visível nas 16 primeiras linhas (title, type, publish, tags, lang).

- [ ] **Step 3: Validar YAML do frontmatter**

Run:
```bash
python3 -c "
import yaml, sys
content = open('03-Dominios/Terminal/Dicionário do Terminal.md').read()
parts = content.split('---', 2)
if len(parts) < 3:
    print('FAIL: no frontmatter delimiters'); sys.exit(1)
fm = yaml.safe_load(parts[1])
assert fm.get('type') == 'glossary', f'type expected glossary, got {fm.get(\"type\")}'
assert fm.get('publish') is True, f'publish expected True, got {fm.get(\"publish\")}'
assert 'glossary' in fm.get('tags', []), 'missing tag glossary'
assert 'terminal' in fm.get('tags', []), 'missing tag terminal'
print('ok: frontmatter valid')
"
```

Expected: `ok: frontmatter valid`. Qualquer outra saída = corrigir o frontmatter.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git status
```

Expected: status mostra apenas `new file: 03-Dominios/Terminal/Dicionário do Terminal.md`.

Then:
```bash
git commit -m "$(cat <<'EOF'
feat(terminal): scaffold Dicionário do Terminal

Cria 03-Dominios/Terminal/Dicionário do Terminal.md como glossário
trilha-wide do domínio Terminal. Estrutura inicial em 4 blocos
temáticos (Vim/Neovim core, Ecossistema LazyVim, LSP & dev, Avançado)
sem verbetes — serão preenchidos pelas notas conforme aparecem.

Pattern alinhado com Dicionário do Indie Hacker e Dicionário de React.

Galho: docs/superpowers/specs/2026-05-19-terminal-editor-design.md
EOF
)"
```

---

## Task 2: MOC do galho Editor — esqueleto

**Files:**
- Create: `03-Dominios/Terminal/Editor/index.md`

**Objetivo:** Criar o MOC do galho com todas as 13 notas listadas como wikilinks (mesmo que ainda não existam — Obsidian aceita wikilinks pendentes; Quartz só renderiza vivos). Estrutura segue o spec §5.

- [ ] **Step 1: Escrever o arquivo**

Criar `03-Dominios/Terminal/Editor/index.md` com **exatamente** o conteúdo abaixo:

````markdown
---
title: "Editor"
type: moc
publish: true
created: 2026-05-19
updated: 2026-05-19
status: growing
progresso: andamento
tags:
  - terminal
  - editor
  - moc
  - neovim
  - lazyvim
aliases:
  - Editor
  - Neovim
  - LazyVim
---
# Editor

> [!abstract] TL;DR
> Galho 1 da trilha Terminal. Domínio de Neovim + LazyVim como editor primário, em 3 fases (4 + 5 + 4 = 13 notas): do modal editing à customização avançada com Treesitter, DAP e snippets.

Esse galho cobre o editor end-to-end: filosofia modal, motions e text objects (Iniciado), config em Lua, lazy.nvim, LSP e customização (Adepto), técnicas de produtividade e refactoring assistido por AST (Magus). LazyVim é o caminho primário porque é o setup real operado; Vim/Neovim core aparece quando o conceito é universal.

## Conteúdo

### Iniciado

- [[01 - Modal editing]]
- [[02 - Motions, operadores e text objects]]
- [[03 - Edição e navegação]]
- [[04 - LazyVim tour]]

### Adepto

- [[05 - Lua para Neovim]]
- [[06 - Estrutura de config]]
- [[07 - lazy.nvim]]
- [[08 - Customizando LazyVim]]
- [[09 - LSP no Neovim]]

### Magus

- [[10 - Registers, marks, macros]]
- [[11 - Workflow avançado]]
- [[12 - Treesitter avançado]]
- [[13 - Snippets e DAP]]

## Rotas alternativas

- **Uso diário** (Iniciado completa): `01` → `02` → `03` → `04`
- **Customização**: `04` → `06` → `07` → `08`
- **Produtividade avançada**: `02` → `10` → `11` → `12`

## Versões assumidas

- **Neovim:** 0.10+ stable (features 0.11+ marcadas explicitamente nas notas)
- **LazyVim:** versão de 2026-05-19 (verificar `:Lazy` na sessão de execução; declarar exata em pass final)
- **lazy.nvim:** latest
- **LuaJIT:** bundled com Neovim (Lua 5.1-compatible)

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
content = open('03-Dominios/Terminal/Editor/index.md').read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1])
assert fm.get('type') == 'moc', 'type não é moc'
assert fm.get('publish') is True, 'publish não é True'
assert fm.get('title') == 'Editor', 'title incorreto'
for t in ['terminal', 'editor', 'moc']:
    assert t in fm.get('tags', []), f'tag {t} ausente'
print('ok: frontmatter valid')
"
grep -c '^- \[\[' "03-Dominios/Terminal/Editor/index.md"
```

Expected: `ok: frontmatter valid` e contagem ≥ 13 (as 13 notas + outros wikilinks).

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Terminal/Editor/index.md"
git commit -m "$(cat <<'EOF'
feat(terminal-editor): scaffold MOC do galho Editor

Cria 03-Dominios/Terminal/Editor/index.md como MOC do galho 1 da
trilha Terminal. Lista as 13 notas planejadas (Iniciado 4 + Adepto 5
+ Magus 4) como wikilinks pendentes, mais 3 rotas alternativas (Uso
diário, Customização, Produtividade avançada) e versões assumidas
(Neovim 0.10+, LazyVim 2026-05-19, lazy.nvim latest).

Galho: docs/superpowers/specs/2026-05-19-terminal-editor-design.md
EOF
)"
```

---

## Task 3: Nota 01 — Modal editing

**Files:**
- Create: `03-Dominios/Terminal/Editor/01 - Modal editing.md`

**Conteúdo-chave do spec (§5, Iniciado):**

> Filosofia "edição como linguagem". Modos (normal, insert, visual, visual-line, visual-block, command, terminal). Troca entre modos (`i`/`a`/`o`, `Esc`/`<C-[>`, `v`/`V`/`<C-v>`, `:`). Indicadores no statusline do LazyVim. Por que isso multiplica velocidade.

**Verbetes referenciados:** modal editing, modo.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://neovim.io/doc/user/intro.html
WebFetch: https://learnvim.irian.to/basics/buffers_windows_tabs
```
(`:Tutor` não é WebFetch-ável — citar como fonte primária dentro do Neovim.)

Capturar: definição precisa de cada modo, comandos de entrada, indicadores visuais.

- [ ] **Step 2: Criar frontmatter + esqueleto**

Criar `03-Dominios/Terminal/Editor/01 - Modal editing.md` com:

```yaml
---
title: "Modal editing"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - modal-editing
  - neovim
aliases:
  - Modal editing
  - Modos do Vim
---
```

Seguido do esqueleto do template padrão (TL;DR vazio, sub-headings a preencher).

- [ ] **Step 3: Escrever a nota completa**

**Cobrir obrigatoriamente:**

- **TL;DR:** "Vim/Neovim separa edição em modos. No modo normal você não digita texto — você comanda. No modo insert você digita. Essa separação transforma edição em uma linguagem de operadores + alvos, e é o que multiplica velocidade."
- **O que é / Como funciona:**
  - Definição: editor modal vs não-modal (VS Code/IntelliJ default).
  - Lista dos 7 modos: normal, insert, visual (char), visual-line (`V`), visual-block (`<C-v>`), command (`:`), terminal (`:terminal`).
  - Filosofia: "Vim is a language. Verbs (operators) + nouns (motions/text objects)". Modo normal = espaço de comando.
  - Como cada modo se identifica visualmente no statusline do LazyVim (`-- INSERT --`, `-- VISUAL --`, etc.).
- **Na prática:**
  - Entrar em insert: `i` (antes do cursor), `a` (depois), `o` (linha abaixo), `O` (linha acima), `I` (início da linha), `A` (fim da linha).
  - Sair de qualquer modo: `<Esc>` ou `<C-[>` (equivalente e mais rápido em alguns layouts).
  - Visual: `v` (char), `V` (linha), `<C-v>` (bloco — útil pra colunas).
  - Command-line: `:` abre, `<Esc>` cancela.
  - Mostrar o ciclo de edição mais comum: normal → `cw` (change word) → digita → `<Esc>` → continua em normal.
- **Armadilhas:**
  - (1) **"Por que minhas letras viraram comandos?"** — você esqueceu de entrar em modo insert. Sintoma: cada tecla move o cursor ou apaga algo. Detectar: olhar o statusline. Sair: `i` ou `a`.
  - (2) **`<Esc>` lento via `jk`/`jj` (custom)** — comunidade redefine, mas LazyVim default mantém `<Esc>` puro; saber disso antes de copiar dotfiles alheios.
  - (3) **Modo terminal "trava"** — no terminal embutido, `<Esc>` vai pro terminal, não pro Neovim. Sair: `<C-\><C-n>` (LazyVim default).
- **Em inglês:** modo (mode), modo normal (normal mode), modo de inserção (insert mode), modo visual (visual mode), modo de comando (command-line mode), entrar em (enter), sair de (exit/leave), edição modal (modal editing), digitar (type), comandar (command). Cada termo com 1 frase técnica.
- **Veja também:**
  - `[[02 - Motions, operadores e text objects]]`
  - `[[03 - Edição e navegação]]`
  - `[[04 - LazyVim tour]]`
  - `[[03-Dominios/Terminal/Editor/index|MOC do galho]]`
  - `[[Dicionário do Terminal#Modal editing|modal editing]]`, `[[Dicionário do Terminal#Modo|modo]]`
- **Referências:** Neovim intro, `:Tutor`, Learn Vim, Practical Vim, Boost Your Fu (URLs do spec §5).

Tamanho-alvo: 200-300 linhas.

- [ ] **Step 4: Criar verbetes referenciados no Dicionário**

Para cada verbete listado (modal editing, modo), abrir `03-Dominios/Terminal/Dicionário do Terminal.md` e adicionar dentro do bloco `## Vim / Neovim core` em ordem alfabética:

```markdown
### Modal editing
Modelo de edição em que o editor opera em modos distintos (normal, insert, visual, command…); cada modo redefine o significado das teclas. É a base de Vim/Neovim e o que permite tratar edição como uma linguagem de comandos.

Veja também: [[01 - Modal editing]], [[02 - Motions, operadores e text objects]].

### Modo
Um dos estados internos do Neovim que define como as teclas são interpretadas. Os modos principais são: normal (comandos), insert (digitar), visual (selecionar), command-line (`:`), terminal (REPL embutido).

Veja também: [[01 - Modal editing]].
```

Se a skill `/verbete` estiver disponível, prefira invocá-la — ela cuida da alfabetização. Se inserir manualmente, manter ordem alfabética dentro de cada bloco.

Atualizar o `updated:` do dicionário para `2026-05-19`.

- [ ] **Step 5: Validar a rubrica**

Aplicar a checklist da seção "Critérios de qualidade por nota" (acima neste plano).

Run:
```bash
test -f "03-Dominios/Terminal/Editor/01 - Modal editing.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/01 - Modal editing.md"
grep -c '^## ' "03-Dominios/Terminal/Editor/01 - Modal editing.md"
```

Expected: arquivo existe, ≥6 wikilinks, ≥5 sub-headings.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/01 - Modal editing.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 01 — Modal editing"
```

---

## Task 4: Nota 02 — Motions, operadores e text objects

**Files:**
- Create: `03-Dominios/Terminal/Editor/02 - Motions, operadores e text objects.md`

**Conteúdo-chave do spec (§5, Iniciado):**

> Gramática verbo+substantivo. Motions essenciais. Operadores. Text objects. Contagem antes de motion. Dot command.

**Verbetes referenciados:** motion, operador, text object.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://neovim.io/doc/user/motion.html
WebFetch: https://thevaluable.dev/vim-text-objects/
```

Capturar: lista canônica de motions, text objects (incluindo `i`/`a` prefixes), operadores standard.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Motions, operadores e text objects"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - motions
  - text-objects
  - operators
aliases:
  - Motions
  - Text objects
  - Operadores
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Edição em Vim é `<operador><motion ou text object>`. Aprender 10 operadores × 20 motions/text objects te dá centenas de combinações. Mais o `.` repete a última edição."
- **O que é / Como funciona:**
  - **Gramática:** `d` (delete) + `iw` (inner word) = `diw`. `c` (change) + `ap` (around paragraph) = `cap`. `y` (yank) + `i"` (inside quotes) = `yi"`.
  - **Operadores principais:** `d` (delete), `c` (change), `y` (yank), `v` (visual), `gu`/`gU` (lowercase/uppercase), `>`/`<` (indent), `=` (auto-indent).
  - **Motions:** definem alvo a partir do cursor. `w`/`e`/`b` (word), `W`/`E`/`B` (WORD — separado por espaço, mais largo), `f<x>`/`t<x>`/`F<x>`/`T<x>` (until char), `0`/`^`/`$` (linha), `gg`/`G` (arquivo), `%` (par de delimitador), `}`/`{` (parágrafo).
  - **Text objects:** delimitam região independente do cursor. `iw`/`aw` (word, inner/around), `ip`/`ap` (paragraph), `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `it`/`at` (tag).
  - **Contagem:** `3w` = avança 3 words. `d3w` = deleta 3 words. `5j` = desce 5 linhas.
  - **Dot command:** `.` repete a última *change* (não motion). Multiplicador de produtividade — combinar com `/` e `n` permite "repetir-confirmar" em refactor manual.
- **Na prática:**
  - Tabela operador × motion com exemplos: `daw` (delete a word), `ci"` (change inside quotes), `yi(` (yank inside parens), `>ip` (indent paragraph), `gUiw` (uppercase word).
  - Workflow real: renomear variável dentro de uma função — `gd` (go to definition) → `*` (busca a palavra) → `cgn` (change next match) → digita novo nome → `<Esc>` → `.` repete pra próxima ocorrência.
  - Visual mode como "operador implícito": `v` + motion → operação. Útil quando o alvo é incomum.
- **Armadilhas:**
  - (1) **Confundir `w` com `W`** — `w` para em pontuação, `W` só em espaço. Em código TS `foo.bar.baz`, `w` te leva a `.`, `W` te leva pro próximo identificador inteiro.
  - (2) **`i"` não funciona se cursor não estiver na linha das aspas** — diferente de algumas IDEs, Vim text objects são locais à linha do cursor (exceto paragraph/section). Mover para a linha antes.
  - (3) **`.` esquecido** — manual de refactoring usando `:%s` quando 3 ocorrências sequenciais aceitam `cgn` + `.` + `.`. `:%s` é mais seguro pra substituições globais, mas mais lento pra 2-3 casos.
- **Em inglês:** motion, operator (operador), text object, word (palavra), WORD (palavra-WORD, sem pontuação), inside (interno, `i`-prefix), around (envolvente, `a`-prefix), repeat (repetir, dot command), grammar (gramática). 5-10 termos.
- **Veja também:** notas 01, 03, 04, 10 (registers usam `y`), 12 (textobjects via Treesitter ampliam o conjunto), MOC do galho, verbetes do dicionário.
- **Referências:** `:help motion.txt`, `:help text-objects`, The Valuable Dev, ThePrimeagen "Vim As Your Editor", Practical Vim.

Tamanho-alvo: 300-400 linhas (denso de exemplos).

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Vim / Neovim core`, em ordem alfabética:

```markdown
### Motion
Comando que move o cursor em modo normal (ex: `w`, `e`, `gg`, `f<x>`). Em Vim, motions são "substantivos" que combinam com operadores ("verbos") para formar comandos. Ex: `dw` = delete + word.

Veja também: [[02 - Motions, operadores e text objects]].

### Operador
Comando que age sobre um alvo definido por motion ou text object. Operadores principais: `d` (delete), `c` (change), `y` (yank), `v` (visual), `>`/`<` (indent), `gu`/`gU` (case).

Veja também: [[02 - Motions, operadores e text objects]].

### Text object
Região textual delimitada semanticamente (palavra, parágrafo, par de delimitadores, tag HTML…). Acessada por prefixos `i` (inner — só o conteúdo) ou `a` (around — inclui delimitadores). Ex: `ci"` muda o conteúdo entre aspas; `da{` deleta o bloco `{ }` inteiro.

Veja também: [[02 - Motions, operadores e text objects]], [[12 - Treesitter avançado]].
```

Atualizar `updated:` do dicionário.

- [ ] **Step 5: Validar rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Editor/02 - Motions, operadores e text objects.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/02 - Motions, operadores e text objects.md"
```

Expected: ≥6 wikilinks. Rubrica completa aprovada.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/02 - Motions, operadores e text objects.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 02 — Motions, operadores e text objects"
```

---

## Task 5: Nota 03 — Edição e navegação

**Files:**
- Create: `03-Dominios/Terminal/Editor/03 - Edição e navegação.md`

**Conteúdo-chave do spec (§5, Iniciado):**

> Ex commands básicas. Yank/paste/delete básico. Search. Substitute. Undo/redo + undotree. Buffers vs windows vs tabs. Splits e navegação entre janelas. Jump list. `:help` e descoberta.

**Verbetes referenciados:** jump list, undotree. (buffer pode virar verbete se faltar — adicionar como tal.)

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://neovim.io/doc/user/change.html
WebFetch: https://neovim.io/doc/user/windows.html
WebFetch: https://learnvim.irian.to/basics/buffers_windows_tabs
```

Capturar: comandos Ex essenciais, search/substitute, modelo buffer/window/tab.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Edição e navegação"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - ex-commands
  - navigation
  - search
aliases:
  - Edição e navegação
  - Ex commands
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Depois de motions/operadores, o que falta pro uso diário é o resto da interface: Ex commands (`:w`, `:e`), busca (`/`, `:s`), undo/redo, e o modelo buffer/window/tab. Saber estes 30 comandos cobre 90% do dia."
- **O que é / Como funciona:**
  - **Ex commands:** modo command-line (`:` em normal). Persistem na história (`:` + `<Up>`).
  - **File ops:** `:w` (write), `:e <path>` (edit), `:q` (quit), `:wq`/`:x` (write+quit), `:q!` (force quit sem salvar), `:qa` (quit all).
  - **Shell:** `:!cmd` (executa comando no shell, ex: `:!git status`).
  - **Yank/paste/delete básico:** `yy` (yank line), `dd` (delete line — vai pro register), `p`/`P` (paste depois/antes).
  - **Search:** `/<termo>` (forward), `?<termo>` (backward), `n`/`N` (próximo/anterior), `*`/`#` (busca palavra sob cursor forward/backward).
  - **Substitute:** `:s/x/y/g` (linha atual, todas ocorrências), `:%s/x/y/g` (arquivo todo), `:%s/x/y/gc` (com confirmação por ocorrência).
  - **Undo/redo:** `u` (undo), `<C-r>` (redo). Undo persistente entre sessões com `undofile` (default no LazyVim). `:undotree` (com plugin undotree.nvim — bundle do LazyVim Extra) navega o tree de edits.
  - **Buffer/window/tab:**
    - **Buffer:** representação em memória de um arquivo aberto. Você pode ter N buffers e M windows; um buffer pode estar em zero ou várias windows.
    - **Window:** viewport visível em uma split. Não é "abrir um arquivo novo" — é "abrir uma janela sobre um buffer".
    - **Tab:** layout de windows (não "aba do navegador" — Neovim tab agrupa splits).
  - **Splits:** `:split` (horizontal), `:vsplit` (vertical), `<C-w>h/j/k/l` (navegar entre splits), `<C-w>=` (igualar tamanho), `<C-w>q` (fechar split).
  - **Buffer nav:** `:bnext`/`:bprev` (sem Telescope), `:b <nome>` (parcial-match), `:ls` (lista buffers). Em LazyVim, `<S-h>`/`<S-l>` é o keymap default pra prev/next.
  - **Jump list:** `<C-o>` (jump back), `<C-i>` (jump forward). Cada motion não-trivial (`gd`, `*`, `%`, mesmo `/`) empurra no jump stack. `:jumps` lista.
  - **`:help`:** `:help <tópico>` abre help split. `:help motion.txt`, `:help :s`, `:help <C-w>`. Em LazyVim, `<leader>fh` (Telescope help_tags) é fuzzy-find sobre todos os tópicos.
- **Na prática:**
  - Sessão típica abrindo um projeto: `nvim .` → neo-tree mostra → `o` (open) num arquivo → `<C-w>w` move entre splits → `:vsplit` abre dual-pane.
  - Refactor manual: `*` busca palavra → `:s//novo/g` (deixar pattern vazio reusa a última busca) → `n` próxima ocorrência → repete.
  - Recovery: editou demais e quer voltar 10 minutos atrás → `:earlier 10m` (time-based undo, pouco conhecido).
- **Armadilhas:**
  - (1) **Confundir window com tab** — quem vem de IDE espera "tab = arquivo aberto". Em Neovim, isso é buffer; tab é layout de splits.
  - (2) **`:q` reclama "no write since last change"** — Vim te protege. Salvar (`:w`) ou forçar (`:q!`). Quem força por hábito perde edits.
  - (3) **Substitute global de palavra parcial** — `:%s/log/error/g` substitui em `login`, `analog`, etc. Usar boundary: `:%s/\<log\>/error/g`.
  - (4) **`<C-i>` = `<Tab>` no terminal** — alguns terminals/keymaps não distinguem. Se jump forward não funcionar, verificar terminal (ex: alacritty handles fine; alguns tmux setups colidem — relevante quando galho Multiplexer chegar).
- **Em inglês:** salvar (write/save), buscar (search), substituir (substitute/replace), janela (window), aba (tab), buffer, lista de saltos (jump list), desfazer (undo), refazer (redo). 5-10 termos.
- **Veja também:** 02 (motions), 04 (Telescope expande tudo aqui), 10 (registers detalha o sistema de paste), 11 (quickfix é o "super-search"), MOC, dicionário.
- **Referências:** `:help change.txt`, `:help pattern.txt`, `:help windows.txt`, `:help cmdline`, Brian Storti registers, Learn Vim buffers.

Tamanho-alvo: 350-450 linhas (nota mais larga da Iniciado — cobre muito chão).

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Vim / Neovim core`, em ordem alfabética:

```markdown
### Buffer
Representação em memória de um arquivo aberto no Neovim. Independente de windows e tabs — N buffers podem estar abertos sem nenhum visível, e o mesmo buffer pode aparecer em várias windows.

Veja também: [[03 - Edição e navegação]].

### Jump list
Pilha de saltos que o Neovim mantém para cada window. Comandos como `gd`, `*`, `}`, `/` empurram a posição. Navegar: `<C-o>` (back), `<C-i>` (forward). Listar: `:jumps`.

Veja também: [[03 - Edição e navegação]].

### Undotree
Estrutura em árvore (não linear) que o Neovim mantém pra desfazer/refazer. Cada `u` volta no tempo; mas se você edita após um undo, cria um novo ramo. Plugin `undotree.nvim` (LazyVim Extra) navega visualmente; comandos `:earlier`/`:later` movem por tempo (`:earlier 5m`).

Veja também: [[03 - Edição e navegação]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

Run:
```bash
test -f "03-Dominios/Terminal/Editor/03 - Edição e navegação.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/03 - Edição e navegação.md"
```

Expected: ≥7 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/03 - Edição e navegação.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 03 — Edição e navegação"
```

---

## Task 6: Nota 04 — LazyVim tour

**Files:**
- Create: `03-Dominios/Terminal/Editor/04 - LazyVim tour.md`

**Conteúdo-chave do spec (§5, Iniciado):**

> Tour do que LazyVim bundle e como usar — sem configurar nada. Telescope, neo-tree, which-key, bufferline+statusline, LSP keys default, nvim-cmp, Comment.nvim, nvim-surround, format on save, `:Lazy`.

**Verbetes referenciados:** distribuição, LazyVim, Telescope, neo-tree, which-key, LSP, code action, format on save.

**Regra dura:** essa nota mostra **o que vem ligado** e como usar. Não configura nada. Configuração é exclusivamente Adepto (tasks 8-10).

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://www.lazyvim.org/
WebFetch: https://www.lazyvim.org/keymaps
WebFetch: https://github.com/LazyVim/starter
```

Capturar: keymaps default canônicos, lista de plugins bundle, behavior de format on save.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "LazyVim tour"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - lazyvim
  - tour
aliases:
  - LazyVim tour
  - LazyVim defaults
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir (com sub-headings em "Na prática" — variação permitida pelo spec §6):**

- **TL;DR:** "LazyVim é uma distribuição Neovim que vem com ~50 plugins pré-configurados e keymaps coerentes. Esta nota é um tour: o que vem ligado, qual key usa, e quando consultar `which-key` pra descobrir o resto. Não configura nada — só usa."
- **O que é / Como funciona:**
  - **Distribuição:** preset Neovim+plugins+config opinatedo. LazyVim escolhe o stack mainstream (Telescope, lazy.nvim, conform, mason) e pré-configura tudo. Diferença de "Neovim vanilla": tudo funciona de saída.
  - **Instalação:** `git clone github.com/LazyVim/starter ~/.config/nvim && nvim` — boot inicial baixa todos plugins via lazy.nvim. (Citar URL do starter; não detalhar mais — quem está aqui já passou por isso.)
  - **Filosofia LazyVim:** "Use defaults. Customize on top, don't fight them." Override é tarefa de Adepto.
- **Na prática (sub-headings):**
  - **Telescope (fuzzy finder):**
    - `<leader>ff` — find files no projeto
    - `<leader>fg` — live grep
    - `<leader>,` — switch buffer
    - `<leader>fh` — help_tags (fuzzy do `:help`)
    - `<leader>fr` — recent files
    - `<leader>sk` — search keymaps (descoberta!)
    - Dentro do prompt: `<C-q>` envia resultados pra quickfix; `<Tab>` multi-select.
  - **neo-tree (file explorer):**
    - `<leader>e` — toggle (LazyVim default — branch root)
    - `<leader>fe` — toggle escopo cwd
    - Dentro: `a` (add), `d` (delete), `r` (rename), `c`/`x` (copy/cut), `p` (paste), `Y` (copy path), `?` (help).
  - **which-key (descoberta):**
    - Pressione `<leader>` e espere — popup mostra grupos disponíveis (`f`=find, `g`=goto, `c`=code, `s`=search…). Diminui drasticamente a memorização inicial.
    - Mesmo padrão funciona após operadores (`y`, `d`, `c`) e `g`, `z`.
  - **Statusline (lualine) e bufferline:**
    - Statusline mostra: modo atual, branch git, diagnostic counts, posição.
    - Bufferline lista buffers como tabs visuais. `<S-h>`/`<S-l>` move entre eles; `<leader>bd` fecha o buffer atual sem fechar a window.
  - **LSP keys default (usar, não configurar):**
    - `gd` — go to definition
    - `gr` — references (em Telescope)
    - `K` — hover (doc inline)
    - `<leader>ca` — code action
    - `<leader>cr` — rename symbol
    - `<leader>cf` — format
    - `]d`/`[d` — próximo/anterior diagnostic
  - **nvim-cmp (auto-complete):**
    - Popup aparece automaticamente em insert mode com suggestions do LSP, buffer, path, snippets.
    - `<C-n>`/`<C-p>` navega, `<CR>` ou `<Tab>` aceita, `<Esc>` cancela.
  - **Comment.nvim:**
    - `gcc` — comenta/descomenta linha atual
    - `gc<motion>` — comenta região (ex: `gcap` comenta o parágrafo)
    - Em visual: `gc` comenta a seleção
  - **nvim-surround:**
    - `ys<motion><char>` — add surround (ex: `ysiw"` envolve word em aspas)
    - `cs<old><new>` — change surround (ex: `cs"'` muda `"` por `'`)
    - `ds<char>` — delete surround (ex: `ds"` remove aspas)
  - **Format on save:**
    - LazyVim **formata ao salvar por default** (`:w`) via conform.nvim. Pode surpreender — se você esperava editar e ver as edits exatas no commit, formatter pode mexer.
    - Toggle: `<leader>uf` (disable format on save).
  - **`:Lazy` (interface do plugin manager):**
    - `:Lazy` abre TUI. Comandos comuns: `S` sync (install+update+clean), `U` update, `R` restore lockfile, `c` checkhealth dos plugins.
- **Armadilhas:**
  - (1) **Format on save reescreve edits que o LSP não entende** — ex: você editou JSON com `// comentário`, salva, formatter reformata e remove comentário. Se acontecer, `<leader>uf` toggle ou usar `:noautocmd w`.
  - (2) **`<leader>` é Space** — default do LazyVim. Quem vem de configs antigas (vimrc com `,` como leader) precisa adaptar dedos.
  - (3) **Telescope `<leader>ff` em projeto grande sem `.git` vira pesado** — LazyVim usa `cwd` se não há repo. Fix: `cd` no root primeiro ou usar `<leader>fF` (find files all = sem filtro de hidden/ignore).
  - (4) **`gd` (LSP) vs `gd` (Vim default)** — Vim's `gd` salta pra declaração local. LazyVim sobrescreve com LSP go-to-definition quando há server ativo. Em arquivo sem LSP, comportamento volta ao default.
- **Em inglês:** distribuição (distribution), atalho de teclado (keymap/keybinding), descobertabilidade (discoverability), formatação ao salvar (format on save), ação de código (code action), saltar para definição (go to definition), referências (references). 5-10 termos.
- **Veja também:** 01 (modal), 02 (motions), 03 (Ex/buffers), 06 (estrutura de config — onde isso vive), 08 (override de defaults), 09 (LSP em detalhe), MOC, dicionário.
- **Referências:** LazyVim docs, keymaps, starter, repo, TJ DeVries channel, LazyVim Discussions.

Tamanho-alvo: 500-600 linhas (aceita ser grande — coberture lateral grande, único tour). Se uma sub-seção (ex: Telescope) sentir-se "autônoma" o suficiente, parar e perguntar ao usuário antes de splitar.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Ecossistema LazyVim`, em ordem alfabética:

```markdown
### Distribuição
Preset de configuração de Neovim que combina um conjunto de plugins, opções e keymaps. Exemplos: LazyVim, LunarVim, AstroNvim, NvChad, kickstart.nvim. Diferente de Neovim "vanilla", onde tudo é configurado do zero.

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### LazyVim
Distribuição Neovim opinatedo mantida por Folke Lemaitre. Bundle inclui Telescope (fuzzy), neo-tree (explorer), which-key, lazy.nvim (plugin manager), LSP stack (mason + nvim-lspconfig + nvim-cmp + conform). Filosofia: "use defaults; customize on top".

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### neo-tree
Plugin de file explorer (árvore de arquivos lateral) que LazyVim usa como default. Atalho `<leader>e`. Suporta operações sobre arquivos (add, delete, rename, copy/paste) por keymaps dentro da árvore.

Veja também: [[04 - LazyVim tour]].

### Telescope
Plugin de fuzzy finder pra Neovim. Em LazyVim, atalhos principais: `<leader>ff` (find files), `<leader>fg` (live grep), `<leader>,` (buffers), `<leader>fh` (help). Pode mandar resultados pra quickfix com `<C-q>`.

Veja também: [[04 - LazyVim tour]], [[11 - Workflow avançado]].

### which-key
Plugin de descoberta de keymaps. Após pressionar uma key prefix (ex: `<leader>`), espera ~1s e mostra popup com os keymaps disponíveis e o que fazem. Atalho `<leader>sk` no LazyVim faz search-keymap.

Veja também: [[04 - LazyVim tour]].
```

E no bloco `## LSP & dev`:

```markdown
### Code action
Operação contextual sugerida pelo LSP — refactoring, fix automático, import, etc. Em LazyVim: `<leader>ca` lista as code actions disponíveis na linha/cursor atual.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Format on save
Comportamento (default no LazyVim) de rodar o formatter (conform.nvim no LazyVim) automaticamente ao salvar (`:w`). Toggle: `<leader>uf`.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### LSP
Language Server Protocol — protocolo cliente/servidor que dá a editores recursos como go-to-definition, hover, completions, diagnostics, formatting. Implementado em Neovim via cliente built-in (`vim.lsp`) e `nvim-lspconfig`. Servers são instalados via Mason.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar config local (critério #8 do spec)**

Como essa nota mostra keymaps default, garantir que os defaults batem com a instalação do usuário. Rodar:

```bash
nvim --headless -c 'lua print(vim.fn.maparg("<leader>ff", "n"))' -c 'q' 2>&1 | head -20
```

Expected: alguma menção a `Telescope` ou `:Telescope find_files`. Se vazio, ou usuário não tem LazyVim instalado, ou keymaps mudaram. **Perguntar antes de prosseguir.**

Alternativa rápida (visual): abrir `nvim`, pressionar `<Space>` e confirmar que `which-key` aparece.

- [ ] **Step 6: Validar rubrica**

Aplicar checklist completa.

Run:
```bash
test -f "03-Dominios/Terminal/Editor/04 - LazyVim tour.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/04 - LazyVim tour.md"
grep -c '^### ' "03-Dominios/Terminal/Editor/04 - LazyVim tour.md"
```

Expected: ≥10 wikilinks (denso de cross-refs), ≥8 sub-headings (uma por sub-seção de "Na prática").

- [ ] **Step 7: Commit**

```bash
git add "03-Dominios/Terminal/Editor/04 - LazyVim tour.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 04 — LazyVim tour"
```

---

## ✅ Checkpoint Iniciado

Após Task 6, a fase **Iniciado** está completa. Antes de seguir pra Adepto:

- [ ] **Verificar coverage da barra de qualidade #1-3** (spec §4):
  1. Editar texto fluentemente em modo normal — coberto por 01, 02
  2. Salvar/abrir/navegar — coberto por 03
  3. Usar LazyVim no dia-a-dia (Telescope, neo-tree, which-key, LSP defaults) — coberto por 04
- [ ] **Inspecionar Dicionário** — verbetes adicionados: ~13 (modal editing, modo, motion, operador, text object, buffer, jump list, undotree, distribuição, LazyVim, neo-tree, Telescope, which-key, code action, format on save, LSP).
- [ ] **Brief intermediate review** com o usuário (se em modo subagent-driven, fazer entre Task 6 e Task 7).

---

## Task 7: Nota 05 — Lua para Neovim

**Files:**
- Create: `03-Dominios/Terminal/Editor/05 - Lua para Neovim.md`

**Conteúdo-chave do spec (§5, Adepto):**

> Sintaxe Lua mínima (tabelas, funções, módulos, `require`, escopo, `local`). `vim.api`, `vim.fn`, `vim.opt`, `vim.keymap.set`, `vim.cmd`, `vim.uv`. Diferenças vs Vimscript (mínimo necessário pra ler config alheia). Gotchas (strings, truthiness em Lua).

**Verbetes referenciados:** Lua, init.lua.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://neovim.io/doc/user/lua-guide.html
WebFetch: https://learnxinyminutes.com/docs/lua/
```

Capturar: API canônica `vim.*`, tabela = único container, truthiness em Lua (só `false` e `nil` são falsy — `0` e `""` são truthy).

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Lua para Neovim"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - lua
  - neovim
aliases:
  - Lua
  - Lua no Neovim
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Neovim usa Lua como linguagem de config. Lua é minúsculo: tabelas, funções, módulos, alguns operadores. O que demanda mais aprendizado é o `vim.*` API que Neovim expõe pra editor."
- **O que é / Como funciona:**
  - **Lua minimal:**
    - Tipos: `nil`, `boolean`, `number`, `string`, `table`, `function`. Tabela é único container (faz array, dict, struct, object).
    - Vars: `local x = 1` (escopo léxico) vs `x = 1` (global — evitar).
    - Functions: `local function f(a, b) return a + b end`. First-class — passam como argumento, retornam de outras.
    - Tables: `t = { 1, 2, 3 }` (array, 1-indexed), `t = { foo = "bar" }` (dict). Indexar: `t[1]` ou `t.foo` (sugar pra `t["foo"]`).
    - Truthiness: **só `false` e `nil` são falsy**. `0`, `""`, `{}` são todos truthy. Pegada clássica.
    - Operadores: `==` igualdade, `~=` desigualdade (não `!=`), `not` ao invés de `!`, `and`/`or` ao invés de `&&`/`||`. Concat: `..` (não `+`).
    - `require("nome")` carrega módulo (procura em `runtimepath`). Módulos retornam um valor (tipicamente tabela).
  - **API Neovim (`vim.*`):**
    - `vim.opt` — opções (set/get). Ex: `vim.opt.number = true`, `vim.opt.relativenumber = true`. Compõe valores: `vim.opt.listchars:append({ tab = "→ " })`.
    - `vim.keymap.set(mode, lhs, rhs, opts)` — define keymap. `vim.keymap.set("n", "<leader>w", "<cmd>w<CR>", { desc = "Save" })`.
    - `vim.api.*` — API low-level (buffers, windows, autocommands). Ex: `vim.api.nvim_create_autocmd("BufWritePre", { callback = function() ... end })`.
    - `vim.fn.*` — chamadas a funções Vimscript (ex: `vim.fn.expand("%:p")` pega path do buffer atual).
    - `vim.cmd("colorscheme tokyonight")` — executa comando Ex.
    - `vim.uv` (alias pra `vim.loop`) — bindings de libuv (IO assíncrono, timers, fs). Usado em plugins; raro em config pessoal.
- **Na prática:**
  - Exemplo 1: definir leader e opções básicas (sem usar LazyVim — Lua puro).
    ```lua
    vim.g.mapleader = " "
    vim.opt.number = true
    vim.opt.relativenumber = true
    vim.opt.expandtab = true
    vim.opt.shiftwidth = 2
    ```
  - Exemplo 2: keymap com função inline.
    ```lua
    vim.keymap.set("n", "<leader>rs", function()
      vim.cmd("source %")
      vim.notify("Sourced!")
    end, { desc = "Re-source current file" })
    ```
  - Exemplo 3: autocmd em Lua.
    ```lua
    vim.api.nvim_create_autocmd("BufWritePre", {
      pattern = "*.lua",
      callback = function() vim.lsp.buf.format() end,
    })
    ```
  - Exemplo 4: ler config alheia (snippet de plugin spec de exemplo). Mostrar entender sem decorar.
- **Armadilhas:**
  - (1) **`0` é truthy em Lua** — `if x then` aceita `x = 0`. Quem vem de Python/JS escorrega aqui. Para "vazio", usar `nil` explicitamente.
  - (2) **Tabela 1-indexed** — `t[1]` é o primeiro elemento, não `t[0]`. `#t` é o comprimento *contando do 1 até o primeiro `nil`* — listas com buracos têm `#` imprevisível.
  - (3) **`local` esquecido** — `x = 1` no top-level cria global. Em config compartilhada, pollui namespace. Sempre `local` por default.
  - (4) **`vim.opt` vs `vim.o`** — `vim.o.listchars = "tab:→ "` (string) vs `vim.opt.listchars = { tab = "→ " }` (table). `vim.opt` aceita operações compostas (`:append`, `:remove`); `vim.o` é set direto. LazyVim usa `vim.opt` por convenção.
- **Em inglês:** tabela (table), módulo (module), escopo léxico (lexical scope), variável local (local variable), atribuição (assignment), truthy/falsy (truthy/falsy — sem tradução elegante; manter EN). 5-10 termos.
- **Veja também:** 06 (onde Lua vive na config), 07 (lazy.nvim usa Lua DSL), 08 (overrides de plugin = Lua), MOC, dicionário.
- **Referências:** `:help lua-guide`, `:help lua`, Lua 5.1 manual, Learn X in Y, TJ DeVries channel, kickstart.nvim.

Tamanho-alvo: 350-450 linhas.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Avançado` (Lua e init.lua entram aqui — é jargão pra quem já passou de "usuário" pra "configurador"):

```markdown
### init.lua
Arquivo principal de configuração do Neovim moderno (sucessor do `init.vim` em Vimscript). Localização: `~/.config/nvim/init.lua`. No LazyVim, é minimal — apenas faz `require("config.lazy")` que carrega o bootstrap.

Veja também: [[05 - Lua para Neovim]], [[06 - Estrutura de config]].

### Lua
Linguagem de scripting embutida em Neovim (via LuaJIT — Lua 5.1-compatible). Substitui Vimscript pra config moderna. Tipos minimal (nil, boolean, number, string, table, function), 1-indexed em tabelas, truthiness peculiar (`0` é truthy).

Veja também: [[05 - Lua para Neovim]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/05 - Lua para Neovim.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/05 - Lua para Neovim.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/05 - Lua para Neovim.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 05 — Lua para Neovim"
```

---

## Task 8: Nota 06 — Estrutura de config

**Files:**
- Create: `03-Dominios/Terminal/Editor/06 - Estrutura de config.md`

**Conteúdo-chave do spec (§5, Adepto):**

> Layout de `~/.config/nvim/` no LazyVim. Ordem de carregamento. Criar keymaps via `vim.keymap.set`. Opções via `vim.opt`. Autocmds.

**Verbetes referenciados:** init.lua, autocmd, keymap, leader key.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://www.lazyvim.org/configuration/general
WebFetch: https://github.com/LazyVim/starter
```

Capturar: estrutura canônica do starter, ordem de require.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Estrutura de config"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - config
  - lazyvim
aliases:
  - Estrutura de config
  - Layout LazyVim
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "LazyVim organiza config em pastas: `lua/config/` pra options/keymaps/autocmds/bootstrap, e `lua/plugins/` pra plugins. Saber a ordem de carregamento é o que destrava a confusão 'onde colocar isto?'."
- **O que é / Como funciona:**
  - **Layout:**
    ```
    ~/.config/nvim/
    ├── init.lua                    # entry point — require("config.lazy")
    ├── lua/
    │   ├── config/
    │   │   ├── lazy.lua            # bootstrap do lazy.nvim, leader, imports
    │   │   ├── options.lua         # vim.opt.* (carregado antes dos plugins)
    │   │   ├── autocmds.lua        # vim.api.nvim_create_autocmd
    │   │   └── keymaps.lua         # vim.keymap.set (carregado após plugins)
    │   └── plugins/                # 1 arquivo por plugin ou grupo
    │       ├── editor.lua
    │       ├── lsp.lua
    │       └── ...
    └── lazy-lock.json              # versões fixadas (commit)
    ```
  - **Ordem de carregamento:**
    1. `init.lua` chama `require("config.lazy")`.
    2. `config.lazy` define `vim.g.mapleader` (deve ser ANTES dos plugins).
    3. `config.options` carrega opções.
    4. `config.autocmds` registra autocmds.
    5. lazy.nvim importa `plugins/*.lua` e carrega plugins.
    6. Plugins prontos → `config.keymaps` registra atalhos (alguns dependem de plugins).
  - **`vim.keymap.set`:**
    - `vim.keymap.set(mode, lhs, rhs, opts)` — `mode` é `"n"` (normal), `"i"` (insert), `"v"` (visual), `"x"` (visual-block), `"t"` (terminal), tabela `{"n","v"}` pra múltiplos.
    - `rhs` pode ser string (sequência de keys) ou função.
    - `opts`: `{ desc = "...", silent = true, noremap = true }` (noremap é default em `vim.keymap.set`).
  - **`vim.opt`:**
    - `vim.opt.X = valor` — setting global.
    - `vim.opt_local.X = valor` — buffer-local (equivalente `:setlocal`).
    - Valores compostos (`listchars`, `wildmode`): tabelas com `:append`/`:remove`.
  - **Autocmds:**
    - Grupo (`augroup`) agrupa autocmds e permite reset (`clear = true`).
    - Eventos comuns: `BufWritePre`, `BufWritePost`, `FileType`, `VimEnter`, `TextYankPost`.
    - `pattern` filtra (ex: `"*.lua"`, `"*"`, lista).
    - `callback` é função Lua; ou `command` é string com Ex command.
- **Na prática:**
  - **Exemplo 1: keymap simples em `lua/config/keymaps.lua`:**
    ```lua
    vim.keymap.set("n", "<leader>so", "<cmd>source %<CR>",
      { desc = "Source current file" })
    ```
  - **Exemplo 2: option custom em `lua/config/options.lua`:**
    ```lua
    vim.opt.wrap = true
    vim.opt.linebreak = true
    vim.opt.colorcolumn = "100"
    ```
  - **Exemplo 3: autocmd em `lua/config/autocmds.lua`:**
    ```lua
    vim.api.nvim_create_autocmd("TextYankPost", {
      group = vim.api.nvim_create_augroup("YankHighlight", { clear = true }),
      callback = function() vim.highlight.on_yank({ timeout = 200 }) end,
    })
    ```
- **Armadilhas:**
  - (1) **Leader definido tarde demais** — se `vim.g.mapleader` é setado em `keymaps.lua` (carregado depois dos plugins), plugins que definem `<leader>X` em `keys = {...}` capturam o leader errado. **Setar em `lazy.lua` antes de `require("lazy")`.**
  - (2) **`lua/plugins/<arquivo>.lua` deve retornar uma tabela** — se esquecer `return { ... }`, o plugin não carrega e não dá erro evidente.
  - (3) **Autocmd duplicado** — sem `augroup` com `clear = true`, `:source` na config registra o autocmd N vezes (uma por reload). Sintoma: callback dispara várias vezes.
  - (4) **`vim.opt.colorcolumn = 100` (number)** — vai dar erro. `colorcolumn` espera string: `"100"` ou `"80,100,120"`.
- **Em inglês:** caminho de carregamento (load path/runtimepath), inicialização (startup), opção global (global option), buffer-local (buffer-local), atalho (mapping/keymap), descrição (description, `desc` field), tecla líder (leader key), grupo de autocmd (augroup). 5-10 termos.
- **Veja também:** 05 (Lua), 07 (lazy.nvim), 08 (override sai daqui), MOC, dicionário.
- **Referências:** LazyVim config general, file structure, `:help runtimepath`, starter, kickstart.

Tamanho-alvo: 350-450 linhas.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Vim / Neovim core`:

```markdown
### Autocmd
Comando que dispara automaticamente em eventos do Neovim (salvar arquivo, abrir buffer, mudar tipo, etc.). Em Lua: `vim.api.nvim_create_autocmd`. Agrupados em `augroup` pra evitar duplicação ao recarregar config.

Veja também: [[06 - Estrutura de config]].

### Keymap
Mapeamento de uma sequência de teclas pra uma ação. Em Neovim moderno: `vim.keymap.set(mode, lhs, rhs, opts)`. Opções comuns: `desc` (descrição visível em which-key), `silent`, `noremap` (default true em vim.keymap.set).

Veja também: [[06 - Estrutura de config]], [[08 - Customizando LazyVim]].

### Leader key
Tecla "prefixo" pra atalhos custom. Default Neovim: `\`. Em LazyVim: `<Space>`. Configurada com `vim.g.mapleader = " "` ANTES de plugins carregarem.

Veja também: [[06 - Estrutura de config]], [[08 - Customizando LazyVim]].
```

(`init.lua` já existe — não duplicar.)

Atualizar `updated:`.

- [ ] **Step 5: Validar config local (critério #8)**

Verificar que o starter do LazyVim segue exatamente o layout descrito:

```bash
ls -la ~/.config/nvim/lua/config/ 2>/dev/null
ls ~/.config/nvim/lua/plugins/ 2>/dev/null | head -10
```

Expected: `lazy.lua`, `options.lua`, `keymaps.lua`, `autocmds.lua` presentes; pelo menos algum arquivo em `plugins/`. Se o usuário usa layout customizado, ajustar o exemplo na nota e adicionar nota de variação.

- [ ] **Step 6: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/06 - Estrutura de config.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/06 - Estrutura de config.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 7: Commit**

```bash
git add "03-Dominios/Terminal/Editor/06 - Estrutura de config.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 06 — Estrutura de config"
```

---

## Task 9: Nota 07 — lazy.nvim

**Files:**
- Create: `03-Dominios/Terminal/Editor/07 - lazy.nvim.md`

**Conteúdo-chave do spec (§5, Adepto):**

> Plugin spec. Lifecycle. Lazy-loading (event, cmd, ft, keys). `:Lazy`. Lockfile. `opts` vs `config`.

**Verbetes referenciados:** plugin manager, lazy.nvim, lazy-loading, plugin spec.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://lazy.folke.io/spec
WebFetch: https://www.lazyvim.org/configuration/plugins
```

Capturar: campos canônicos da spec (`url`, `opts`, `config`, `init`, `keys`, `event`, `cmd`, `ft`, `dependencies`, `enabled`, `lazy`, `priority`).

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "lazy.nvim"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - lazy-nvim
  - plugin-manager
aliases:
  - lazy.nvim
  - Plugin manager
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "lazy.nvim é o plugin manager que LazyVim usa. Plugin = tabela Lua (spec) que diz onde buscar, quando carregar, e como configurar. Lazy-loading por evento/comando/filetype/key é o que mantém startup rápida."
- **O que é / Como funciona:**
  - **Plugin spec — campos principais:**
    - `[1]` ou `url` — `"author/repo"` (GitHub) ou URL completa.
    - `opts = { ... }` — tabela passada pra `require("plugin").setup(opts)` automaticamente.
    - `config = function(_, opts) require("plugin").setup(opts) end` — controle total da inicialização. **Usar opts sempre que possível; config quando precisa de lógica extra.**
    - `init = function() ... end` — roda no startup, antes do plugin carregar (raro precisar).
    - `dependencies = { "outro/plugin" }` — força ordem de load.
    - `event = "VeryLazy" | "BufReadPost" | ...` — carrega em evento.
    - `cmd = "Telescope"` — carrega quando comando Ex é chamado.
    - `ft = { "lua", "python" }` — carrega ao abrir arquivo do tipo.
    - `keys = { "<leader>ff", ... }` — carrega quando key é pressionada.
    - `enabled = false` — desabilita o plugin (sem deletar).
    - `priority = 1000` — força ordem (colorscheme normalmente é 1000).
    - `lazy = true` — força lazy (default em LazyVim quando há trigger).
  - **Lifecycle:** spec coletada → resolvida (dependências) → lazy-loaded ou eager → `init` → `config` (com `opts` mergeados) → plugin ativo.
  - **`:Lazy` (TUI):**
    - `S` — Sync (install+update+clean conforme spec)
    - `U` — Update
    - `R` — Restore (volta pra `lazy-lock.json`)
    - `c` — Clean (remove plugins não-mais-spec'd)
    - `P` — Profile (mostra tempo de load de cada plugin)
    - `?` — help
  - **`lazy-lock.json`:** snapshot dos commits/tags exatos de cada plugin. **Commitar no repo de dotfiles** — reproduz mesma versão em outra máquina via `:Lazy restore`.
  - **`opts` vs `config`:**
    - `opts = { x = 1 }` → lazy.nvim chama `require("plugin").setup({ x = 1 })`. 90% dos casos.
    - `config = function(_, opts) ... end` → você controla. Usar pra setup customizado (ex: customizar `cmp.setup` com mapping function).
- **Na prática:**
  - **Exemplo 1: plugin novo em LazyVim** (`lua/plugins/zen.lua`):
    ```lua
    return {
      "folke/zen-mode.nvim",
      cmd = "ZenMode",
      keys = {
        { "<leader>uz", "<cmd>ZenMode<cr>", desc = "Zen mode" },
      },
      opts = {
        window = { width = 0.8 },
      },
    }
    ```
  - **Exemplo 2: dependência + lazy-load por filetype** (`lua/plugins/markdown.lua`):
    ```lua
    return {
      "MeanderingProgrammer/render-markdown.nvim",
      ft = { "markdown" },
      dependencies = { "nvim-treesitter/nvim-treesitter" },
      opts = {},
    }
    ```
  - **Exemplo 3: config function pra lógica condicional:**
    ```lua
    return {
      "neovim/nvim-lspconfig",
      config = function()
        local lspconfig = require("lspconfig")
        local servers = { "ts_ls", "lua_ls" }
        for _, s in ipairs(servers) do
          lspconfig[s].setup({})
        end
      end,
    }
    ```
- **Armadilhas:**
  - (1) **Não retornar tabela** — `lua/plugins/foo.lua` sem `return { ... }`: plugin não carrega, sem erro óbvio. `:Lazy` não lista.
  - (2) **`opts` vs `config` simultâneo** — se usar `config = function(_, opts) ... end`, o `opts` é passado mas você precisa chamar `setup` manualmente. Erro comum: usa `config` e não chama setup.
  - (3) **`lazy-lock.json` não commitado** — sem ele, "rodou na minha máquina" volta. Adicionar ao repo de dotfiles.
  - (4) **`event = "VeryLazy"`** — `VeryLazy` é evento próprio do lazy.nvim (após UI pronta). Útil pra plugins que não precisam estar prontos no boot. Não confundir com `BufReadPost`.
- **Em inglês:** plugin manager, plugin spec, carregamento preguiçoso (lazy loading), gatilho (trigger), evento (event), dependência (dependency), arquivo de lock (lockfile), perfil de tempo (profile/timing). 5-10 termos.
- **Veja também:** 06 (onde a spec vive), 08 (override de plugin LazyVim), 09 (LSP plugins via spec), MOC, dicionário.
- **Referências:** lazy.folke.io, plugin spec ref, LazyVim plugins doc, Awesome Neovim.

Tamanho-alvo: 350-450 linhas.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Ecossistema LazyVim`:

```markdown
### Lazy-loading
Carregar um plugin apenas quando necessário (em evento, comando, filetype ou tecla específica), ao invés de no startup. Reduz tempo de boot. Em lazy.nvim: campos `event`, `cmd`, `ft`, `keys` na plugin spec.

Veja também: [[07 - lazy.nvim]].

### lazy.nvim
Plugin manager moderno do Neovim mantido por Folke Lemaitre. Usa Lua DSL pra spec de plugins. Recursos: lazy-loading nativo, lockfile (`lazy-lock.json`), profiling, UI interativa (`:Lazy`).

Veja também: [[07 - lazy.nvim]].

### Plugin manager
Ferramenta que instala, atualiza e carrega plugins do Neovim. Os principais: lazy.nvim (atual, em LazyVim), packer.nvim (legado), vim-plug (legado, Vimscript). LazyVim usa lazy.nvim por default.

Veja também: [[07 - lazy.nvim]], [[04 - LazyVim tour]].

### Plugin spec
Descrição de um plugin em formato tabela Lua, usada pelo lazy.nvim. Campos comuns: URL/source, `opts` (config passada ao setup), `config` (callback de init custom), `event`/`cmd`/`ft`/`keys` (triggers de lazy-load), `dependencies`.

Veja também: [[07 - lazy.nvim]], [[08 - Customizando LazyVim]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/07 - lazy.nvim.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/07 - lazy.nvim.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/07 - lazy.nvim.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 07 — lazy.nvim"
```

---

## Task 10: Nota 08 — Customizando LazyVim

**Files:**
- Create: `03-Dominios/Terminal/Editor/08 - Customizando LazyVim.md`

**Conteúdo-chave do spec (§5, Adepto):**

> Adicionar plugin novo. Override de `opts` de plugin existente (merge profundo). Desabilitar plugin. Override e criação de keymaps. Habilitar Extras. Debug de conflitos.

**Verbetes referenciados:** keymap, leader key, plugin spec, distribuição.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://www.lazyvim.org/configuration/plugins
WebFetch: https://www.lazyvim.org/configuration/recipes
WebFetch: https://www.lazyvim.org/extras
```

Capturar: regras de merge `opts` (deep merge via tabela), Extras canônicos.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Customizando LazyVim"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - customization
  - lazyvim
aliases:
  - Customizando LazyVim
  - LazyVim override
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "LazyVim é override-friendly: você cria arquivos em `lua/plugins/` que estendem ou sobrescrevem os defaults. Para plugin novo: spec completa. Para customizar existente: spec parcial com `opts` que faz merge profundo."
- **O que é / Como funciona:**
  - **Adicionar plugin novo:** criar `lua/plugins/<nome>.lua` que retorna a spec (já mostrado em 07). LazyVim importa automático.
  - **Override de plugin LazyVim:**
    - Em `lua/plugins/<override>.lua`, retornar spec que aponta pro mesmo URL do plugin LazyVim:
      ```lua
      return {
        "nvim-telescope/telescope.nvim",
        opts = {
          defaults = {
            layout_strategy = "vertical",
          },
        },
      }
      ```
    - lazy.nvim faz deep merge de `opts` com o default LazyVim. Nested tables são combinadas; valores primitivos são sobrescritos.
  - **Desabilitar plugin LazyVim:**
    ```lua
    return { "rcarriga/nvim-notify", enabled = false }
    ```
  - **Override de keymap LazyVim:**
    - Default LazyVim define `<leader>ff` (find files via Telescope). Pra remover/alterar:
      ```lua
      return {
        "nvim-telescope/telescope.nvim",
        keys = {
          { "<leader>ff", false }, -- remove o default
          { "<leader>ff", "<cmd>Telescope find_files hidden=true<cr>", desc = "Find files (hidden)" },
        },
      }
      ```
    - `false` na posição de `rhs` desabilita o keymap.
  - **Novo keymap global** (sem plugin) em `lua/config/keymaps.lua`:
    ```lua
    vim.keymap.set("n", "<leader>w", "<cmd>w<CR>", { desc = "Save" })
    ```
  - **Extras:** módulos opcionais de LazyVim. Habilitar via `:LazyExtras` (TUI interativa) ou em `lua/config/lazy.lua` adicionando `{ import = "lazyvim.plugins.extras.lang.typescript" }`. Categorias: `lang/*` (TS, Python, Rust…), `dap/*` (debuggers), `editor/*` (mini.surround, harpoon…), `ui/*` (mini.animate, edgy…).
  - **Debugging de conflitos:**
    - `:Lazy profile` — quais plugins demoram pra carregar
    - `:Lazy log <plugin>` — log de um plugin específico
    - `:checkhealth` — geral, mostra healthchecks de cada plugin
    - `:LazyExtras` — habilitar/desabilitar Extras visualmente
- **Na prática:**
  - **Exemplo 1: customizar tema** (`lua/plugins/colorscheme.lua`):
    ```lua
    return {
      { "folke/tokyonight.nvim", opts = { style = "moon" } },
      { "LazyVim/LazyVim", opts = { colorscheme = "tokyonight" } },
    }
    ```
  - **Exemplo 2: adicionar formatter por linguagem** (`lua/plugins/conform.lua`):
    ```lua
    return {
      "stevearc/conform.nvim",
      opts = {
        formatters_by_ft = {
          python = { "ruff_format", "ruff_fix" },
        },
      },
    }
    ```
  - **Exemplo 3: desabilitar bufferline** (`lua/plugins/disable-bufferline.lua`):
    ```lua
    return { "akinsho/bufferline.nvim", enabled = false }
    ```
  - **Exemplo 4: habilitar Extra de TypeScript** (em `lua/config/lazy.lua` adicionar dentro de `spec`):
    ```lua
    spec = {
      { "LazyVim/LazyVim", import = "lazyvim.plugins" },
      { import = "lazyvim.plugins.extras.lang.typescript" },
      { import = "plugins" },
    },
    ```
- **Armadilhas:**
  - (1) **`opts = nil` sobrescreve o default** — se você escrever `return { "telescope", opts = nil }`, LazyVim entende que você quer `opts` vazio, perdendo defaults. Use `opts = {}` se for o caso, ou omita.
  - (2) **Função em `opts` quebra o merge** — `opts` precisa ser tabela pra deep merge. Se é função, lazy.nvim chama com `opts` original. Caso ambíguo: ler doc de Recipes.
  - (3) **Adicionou Extra mas plugins não aparecem** — Extras adicionam *novos* plugins à spec; precisa `:Lazy sync` (`S`) pra baixar. `:checkhealth` confirma.
  - (4) **`{ "<leader>ff", false }` esquecido antes da redefinição** — sem remover o default, lazy.nvim mantém os dois mappings (o seu pode ou não vencer dependendo de ordem). Sempre `false` antes de redefinir.
- **Em inglês:** customização (customization), override, mesclagem profunda (deep merge), desabilitar (disable), atalho do plugin (plugin keymap), módulo extra (extra/extension). 5-10 termos.
- **Veja também:** 06 (estrutura), 07 (spec ref), 09 (LSP custom é caso especial), MOC, dicionário.
- **Referências:** LazyVim plugins, recipes, extras, Folke dotfiles, Discussions.

Tamanho-alvo: 400-500 linhas.

- [ ] **Step 4: Verbetes** — todos já criados (keymap, leader key, plugin spec, distribuição). Só verificar que existem; sem criar novos. Atualizar `updated:` por safety.

- [ ] **Step 5: Validar config local (critério #8)**

Validar que os exemplos da nota carregam sem erro num scratch dir (não tocar a config do usuário):

```bash
NVIM_APPNAME=nvim-test-lazyvim mkdir -p ~/.config/nvim-test-lazyvim
# (mais simples: deixar como exercício de validação manual)
echo "Verificação manual: rodar :Lazy reload em ~/.config/nvim/ e confirmar 0 errors em :messages."
```

Alternativa: se o usuário aceitar, copiar um exemplo (ex: `colorscheme.lua` desabilitado) pro `~/.config/nvim/lua/plugins/_test.lua`, rodar `:Lazy sync`, verificar `:messages`, depois remover. **Não fazer sem confirmação.**

- [ ] **Step 6: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/08 - Customizando LazyVim.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/08 - Customizando LazyVim.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 7: Commit**

```bash
git add "03-Dominios/Terminal/Editor/08 - Customizando LazyVim.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 08 — Customizando LazyVim"
```

---

## Task 11: Nota 09 — LSP no Neovim

**Files:**
- Create: `03-Dominios/Terminal/Editor/09 - LSP no Neovim.md`

**Conteúdo-chave do spec (§5, Adepto):**

> O que é LSP. Mason. Config de server (override settings, on_attach). Completion via nvim-cmp. Format on save via conform.nvim. Keymaps LSP default LazyVim. Diagnostic flow. Troubleshooting.

**Verbetes referenciados:** LSP, language server, Mason, nvim-lspconfig, nvim-cmp, code action, diagnostic, formatter, linter, format on save.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://www.lazyvim.org/configuration/lsp
WebFetch: https://github.com/neovim/nvim-lspconfig
WebFetch: https://github.com/williamboman/mason.nvim
WebFetch: https://github.com/stevearc/conform.nvim
```

Capturar: API canônica `lspconfig.X.setup()`, defaults LazyVim (server map automático, `on_attach`).

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "LSP no Neovim"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - lsp
  - mason
  - completion
aliases:
  - LSP
  - Language Server Protocol
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Language Server Protocol (LSP) é cliente-servidor: editor (cliente) fala JSON-RPC com servidor da linguagem (TypeScript, Rust, etc.) pra hover, completions, refactor. Em LazyVim: Mason instala servers, lspconfig configura, nvim-cmp completa, conform formata."
- **O que é / Como funciona:**
  - **Protocolo:** spec da Microsoft. Editor envia (`textDocument/hover`, `textDocument/definition`), server responde. Transporte: JSON-RPC over stdio.
  - **Capabilities:** cada cliente declara o que entende, cada server o que faz. Negociação inicial em `initialize`.
  - **Stack LazyVim:**
    - **Mason** — instala/atualiza language servers, formatters, linters, DAP adapters. `:Mason` abre TUI.
    - **nvim-lspconfig** — configs padronizadas pra ~200 servers. Em LazyVim, configura via spec do plugin.
    - **nvim-cmp** — engine de completion. Sources: LSP, buffer, path, snippets.
    - **conform.nvim** — formatter dispatcher (chama prettier, ruff, gofmt…).
    - **nvim-lint** — linter dispatcher (chama eslint_d, ruff…). (Bundle do LazyVim para alguns langs.)
  - **Keymaps default LazyVim** (mesmos da 04):
    - `gd` go to definition
    - `gr` references (Telescope)
    - `gI` implementations
    - `gy` type definition
    - `K` hover
    - `<leader>ca` code action
    - `<leader>cr` rename
    - `<leader>cf` format
    - `]d`/`[d` diagnostic next/prev
    - `]e`/`[e` errors next/prev
    - `]w`/`[w` warnings next/prev
  - **Diagnostic flow:** server emite `textDocument/publishDiagnostics` → cliente renderiza com `vim.diagnostic.*` (signs no gutter, virtual text inline, underline). `:lopen` ou Telescope `<leader>xd` lista.
  - **Troubleshooting:**
    - `:LspInfo` — clients ativos no buffer
    - `:Mason` — verificar se server está instalado
    - `:checkhealth lsp` — diagnose geral
    - `:ConformInfo` — qual formatter dispara
    - `:LspLog` — log do client (em `~/.local/state/nvim/lsp.log`)
- **Na prática:**
  - **Exemplo 1: customizar settings de um server** (`lua/plugins/lsp.lua`):
    ```lua
    return {
      "neovim/nvim-lspconfig",
      opts = {
        servers = {
          ts_ls = {
            settings = {
              typescript = {
                inlayHints = {
                  parameterNames = { enabled = "all" },
                  parameterTypes = { enabled = true },
                },
              },
            },
          },
        },
      },
    }
    ```
  - **Exemplo 2: adicionar formatter customizado** (`lua/plugins/conform.lua`):
    ```lua
    return {
      "stevearc/conform.nvim",
      opts = {
        formatters_by_ft = {
          markdown = { "prettier", "markdownlint" },
        },
        formatters = {
          markdownlint = {
            prepend_args = { "--fix" },
          },
        },
      },
    }
    ```
  - **Exemplo 3: on_attach pra keymap por server:**
    ```lua
    return {
      "neovim/nvim-lspconfig",
      opts = {
        servers = {
          ts_ls = {
            on_attach = function(client, bufnr)
              vim.keymap.set("n", "<leader>co", "<cmd>TypescriptOrganizeImports<cr>",
                { buffer = bufnr, desc = "Organize imports" })
            end,
          },
        },
      },
    }
    ```
  - **Exemplo 4: instalar server via Mason** — `:Mason` → escrolla até `lua-language-server` → `i` (install).
- **Armadilhas:**
  - (1) **Mason install ≠ ativo** — Mason instala o binary, mas pra ativar você precisa de spec em lspconfig. LazyVim auto-configura servers comuns; pra langs exotic, criar spec.
  - (2) **`ts_ls` vs `tsserver`** — TypeScript language server foi renomeado `tsserver → ts_ls` em 2024. Tutoriais antigos usam `tsserver` e quebram. Verificar no Mason qual nome está atual.
  - (3) **Format on save vs LSP format vs conform** — em LazyVim, `:w` chama conform por default; LSP format só se o filetype não tem formatter conform. Confusão comum: "por que `:lua vim.lsp.buf.format()` faz coisa diferente de `:w`?". Resposta: conform tem prioridade.
  - (4) **Diagnostic flood em mono-repo** — server pode reportar erros em arquivos não-abertos. Configurar `root_dir` corretamente. Em TS: `tsconfig.json` define raiz.
  - (5) **`null-ls` em tutoriais 2023** — null-ls foi arquivado; substituído por conform (formatting) + nvim-lint (linting) no LazyVim moderno. Tutoriais antigos confundem.
- **Em inglês:** servidor de linguagem (language server), capabilities (capacidades), diagnóstico (diagnostic), refatorar renomeando (rename symbol), formatador (formatter), linter (linter, sem tradução elegante), gutter (gutter — sign column). 5-10 termos.
- **Veja também:** 04 (LSP keys default), 06 (config), 07 (lazy.nvim spec), 12 (Treesitter complementa), 13 (DAP irmão), MOC, dicionário.
- **Referências:** LazyVim LSP, nvim-lspconfig, mason.nvim, nvim-cmp, conform.nvim, LSP spec, TJ DeVries LSP.

Tamanho-alvo: 450-550 linhas (densa por natureza).

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## LSP & dev`:

```markdown
### Diagnostic
Mensagem de problema (erro, warning, info, hint) emitida por um language server ou linter sobre um arquivo. Em Neovim: rendered como sign no gutter, virtual text inline, underline. Listada via `:lopen` ou Telescope `<leader>xd`.

Veja também: [[09 - LSP no Neovim]].

### Formatter
Ferramenta que reformata código segundo regras (prettier, ruff, gofmt, stylua…). Em LazyVim moderno, dispatcher é conform.nvim. Acionado em `:w` (format on save) ou explicitamente via `<leader>cf`.

Veja também: [[09 - LSP no Neovim]].

### Language server
Processo separado que implementa a Language Server Protocol pra uma linguagem específica (ex: `ts_ls` pra TypeScript, `lua_ls` pra Lua, `rust_analyzer` pra Rust). Editor é cliente; server responde requests sobre o código (hover, definition, refactor).

Veja também: [[09 - LSP no Neovim]].

### Linter
Ferramenta que analisa código por padrões problemáticos sem necessariamente quebrar build (eslint, ruff, shellcheck…). Em LazyVim, dispatcher é nvim-lint. Diagnostics aparecem no mesmo flow do LSP.

Veja também: [[09 - LSP no Neovim]].

### Mason
Plugin de Neovim que gerencia instalação/atualização de language servers, formatters, linters e DAP adapters. `:Mason` abre TUI. Bundle do LazyVim.

Veja também: [[09 - LSP no Neovim]], [[13 - Snippets e DAP]].

### nvim-cmp
Engine de completion pra Neovim. Aceita múltiplas sources (LSP, buffer, path, snippet). Renderiza popup em insert mode. Bundle do LazyVim.

Veja também: [[09 - LSP no Neovim]].

### nvim-lspconfig
Plugin que provê configs padronizadas pra ~200 language servers em Neovim. Em LazyVim, customização via `opts.servers.<nome> = { settings = {...} }`.

Veja também: [[09 - LSP no Neovim]].
```

(LSP, code action, format on save já existem.)

Atualizar `updated:`.

- [ ] **Step 5: Validar config local (critério #8)**

```bash
nvim --headless -c 'lua print(vim.lsp.get_clients() and "ok: LSP API available" or "FAIL")' -c 'q'
```

Expected: `ok: LSP API available`. Se LSP API não existe, Neovim é muito antigo (<0.10). **Bloquear o galho até atualizar Neovim.**

Mostrar ao usuário (manual): abrir um arquivo TS no Neovim, esperar 2s, `:LspInfo` deve listar `ts_ls` ativo. Se não, Mason precisa instalar.

- [ ] **Step 6: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/09 - LSP no Neovim.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/09 - LSP no Neovim.md"
```

Expected: ≥8 wikilinks. Rubrica completa.

- [ ] **Step 7: Commit**

```bash
git add "03-Dominios/Terminal/Editor/09 - LSP no Neovim.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 09 — LSP no Neovim"
```

---

## ✅ Checkpoint Adepto

Após Task 11, a fase **Adepto** está completa. Antes de seguir pra Magus:

- [ ] **Verificar coverage da barra de qualidade #4-5** (spec §4):
  4. Editar `~/.config/nvim/` sem medo — coberto por 05, 06, 07, 08
  5. Diagnosticar problema de LSP — coberto por 09
- [ ] **Inspecionar Dicionário** — verbetes adicionados nesta fase: Lua, init.lua, autocmd, keymap, leader key, lazy-loading, lazy.nvim, plugin manager, plugin spec, diagnostic, formatter, language server, linter, Mason, nvim-cmp, nvim-lspconfig.
- [ ] **Brief intermediate review** com o usuário se em modo subagent-driven.

---

## Task 12: Nota 10 — Registers, marks, macros

**Files:**
- Create: `03-Dominios/Terminal/Editor/10 - Registers, marks, macros.md`

**Conteúdo-chave do spec (§5, Magus):**

> Classes de registers (named, numbered, sistema, expression, search, command, black hole). Uso prático. Marks locais vs globais. Gravar/editar macros. Macros aninhados.

**Verbetes referenciados:** register, mark, macro.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://neovim.io/doc/user/change.html
WebFetch: https://www.brianstorti.com/vim-registers/
WebFetch: https://neovim.io/doc/user/repeat.html
```

Capturar: lista oficial de registers, sintaxe de marks, recording API.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Registers, marks, macros"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - editor
  - magus
  - registers
  - marks
  - macros
aliases:
  - Registers
  - Marks
  - Macros
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Vim tem dezenas de 'clipboards' (registers), bookmarks dentro/entre arquivos (marks), e gravação de keystroke pra replay (macros). Combinados, multiplicam edição. Saber os 5-10 essenciais já automatiza muito."
- **O que é / Como funciona:**
  - **Registers — classes:**
    - **Named** (`a`-`z`, `A`-`Z`): explícitos. `"ayy` yank linha pra `a`. `"AY` *appenda* à `a` (uppercase = append).
    - **Unnamed** (`""`): default. Todo yank/delete/change que não especifica register vai pra cá. `p` pasta dele.
    - **Numbered** (`0`-`9`): histórico de yanks. `"0` é o último yank (não delete). `"1` a `"9` são histórico de deletes (`"1` = mais recente delete, `"9` = mais antigo).
    - **Sistema** (`+`, `*`): clipboard do OS. `"+y` copia pro clipboard (acessível em outros apps). `*` é selection primária no Linux X11.
    - **Expression** (`=`): avalia expressão Vimscript/Lua. `"=2+2<CR>p` cola `4`.
    - **Search** (`/`): última busca. `:put /` injeta no buffer.
    - **Command** (`:`): último comando Ex.
    - **Black hole** (`_`): joga fora. `"_dd` deleta linha sem ir pra register algum (não polui histórico).
    - **Listar:** `:registers` ou `:reg`. Em LazyVim com which-key, `"<Espera>` mostra dump.
  - **Marks:**
    - **Locais** (`a`-`z`): scope buffer atual. `ma` cria mark `a` na linha+coluna atual. `'a` salta pra linha; `` `a `` salta pra linha+coluna exata.
    - **Globais** (`A`-`Z`): cross-file, persistem entre sessões (no `shada`). Útil pra "lembrar de voltar nesse arquivo".
    - **Especiais:** `'.` última edição, `''` posição antes do último jump, `'^` última posição em insert, `'<`/`'>` início/fim da última visual selection.
    - **Listar:** `:marks`, Telescope `<leader>sm`.
  - **Macros:**
    - Gravar: `q<reg>` (começa), execute keys, `q` (para). Salva em `<reg>`.
    - Reproduzir: `@<reg>` (uma vez), `@@` (repete último), `5@a` (5 vezes).
    - **Macro é register** — `:reg a` mostra o conteúdo. Editável: `"ap` (cola no buffer), edita, `"ay$` (yank de volta).
    - **Macros aninhados:** dentro de um macro, `@b` chama outro macro. Risco: loop infinito; mitigar com fallback ou contagem fixa.
- **Na prática:**
  - **Exemplo 1: registers cotidiano:**
    - Yank código pra register `c`: `"cyap` (yank around paragraph).
    - Em outro buffer: `"cp` cola sem perder o yank atual.
    - Copiar pra clipboard do OS pra colar no Slack: `"+yy`.
  - **Exemplo 2: marks pra refactor cross-file:**
    - Em `src/utils.ts`: `mU` (cria mark global `U`).
    - Em `tests/utils.test.ts`: edita.
    - Pula de volta: `` `U `` — direto pro mesmo ponto em `utils.ts`.
  - **Exemplo 3: macro pra renumerar lista:**
    - Buffer com `- item N` em N linhas, quer trocar por `1. item N`, `2. item N`, etc.
    - `gg` (topo), `qq` (grava `q`): `0cw1.<Esc>+` (substitui prefixo, vai pra próxima linha não-vazia)... mas precisa incrementar. Usar truque: `<C-a>` em modo normal incrementa número sob cursor. Variar: troca por `1. item N` em linha 1; depois `5j @q` ou outra técnica.
    - Versão mais simples: `:%s/^- /1. /` e depois usar `g<C-a>` em visual sobre os números pra incrementar sequencialmente.
  - **Exemplo 4: editar macro pra corrigir:**
    - Macro gravada errada em `a`. `:put a` cola conteúdo no buffer. Edita. Visual line sobre as linhas, `"ay$` ou `0"ay$` pra rerregister.
- **Armadilhas:**
  - (1) **`dd` polui o unnamed register** — pra deletar sem perder o yank atual, `"_dd` (black hole). Especialmente útil ao colar repetidamente (`p` cola o último yank, mas `dd` antes do `p` substitui).
  - (2) **Macro grava `:` errado** — se durante gravação você abre Telescope (que abre prompt fora do buffer), o macro pode capturar movimento que não replay. Testar antes de confiar.
  - (3) **Marks globais somem** — se o arquivo é movido/renomeado fora do Neovim, o mark global aponta pra path obsoleto. Reset: `delmarks A` ou `:delmarks!` (todos).
  - (4) **`<C-a>` incrementa número errado em padrões mistos** — `foo123` com cursor antes de `f`: `<C-a>` pula até `123` e incrementa. Em visual + `g<C-a>` incrementa sequencialmente cada selecionado.
- **Em inglês:** registrador (register), marca (mark), gravar (record), reproduzir (replay/playback), aninhado (nested), buraco negro (black hole — manter), append vs sobrescrever (append vs overwrite). 5-10 termos.
- **Veja também:** 02 (operadores escrevem em registers), 03 (yank/delete/paste base), 11 (quickfix usa pattern register-like), MOC, dicionário.
- **Referências:** `:help registers`, `:help mark-motions`, `:help recording`, Brian Storti, ThePrimeagen macros, Practical Vim caps macros.

Tamanho-alvo: 400-500 linhas.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Vim / Neovim core`:

```markdown
### Macro
Sequência de teclas gravada e replicável em Neovim. Gravar: `q<reg>` + teclas + `q`. Replay: `@<reg>` (uma vez), `@@` (último), `N@<reg>` (N vezes). O macro é um register editável — `:put a` mostra/edita.

Veja também: [[10 - Registers, marks, macros]].

### Mark
Posição salva (linha + coluna) em um buffer. Locais (`a`-`z`, scope buffer) ou globais (`A`-`Z`, persistem entre arquivos e sessões). Criar: `m<letra>`. Saltar: `'<letra>` (linha) ou `` `<letra> `` (linha+coluna). Listar: `:marks`.

Veja também: [[10 - Registers, marks, macros]].

### Register
"Clipboard" nomeado do Vim. Yank/delete/change escrevem em registers; paste lê. Classes: named (`a`-`z`), numbered (`0`-`9`, histórico), system (`+`/`*`), expression (`=`), search (`/`), command (`:`), black hole (`_`). Listar: `:reg`.

Veja também: [[10 - Registers, marks, macros]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/10 - Registers, marks, macros.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/10 - Registers, marks, macros.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/10 - Registers, marks, macros.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 10 — Registers, marks, macros"
```

---

## Task 13: Nota 11 — Workflow avançado

**Files:**
- Create: `03-Dominios/Terminal/Editor/11 - Workflow avançado.md`

**Conteúdo-chave do spec (§5, Magus):**

> Quickfix vs location list. Populando via grep/Telescope. Navegação. Edição em massa (`:cdo`). Refactoring pesado. Sessions com persistence.nvim. todo-comments.

**Verbetes referenciados:** quickfix list.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://neovim.io/doc/user/quickfix.html
WebFetch: https://github.com/folke/persistence.nvim
WebFetch: https://github.com/folke/todo-comments.nvim
```

Capturar: comandos canônicos quickfix, integração Telescope `<C-q>`, `:cdo`/`:cfdo`.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Workflow avançado"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - editor
  - magus
  - quickfix
  - workflow
  - refactoring
aliases:
  - Workflow avançado
  - Quickfix
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Quickfix é a lista global de 'lugares pra ir/editar' em Neovim. Telescope manda resultados pra ela; `:cdo` aplica edição em todos. Sessions trazem layout de volta. Workflow que substitui muita ferramenta de IDE."
- **O que é / Como funciona:**
  - **Quickfix list vs location list:**
    - **Quickfix:** uma só por sessão. Global.
    - **Location list:** uma por window. Local ao split.
    - Mesma API com `c` vs `l` prefix: `:copen`/`:lopen`, `:cnext`/`:lnext`, etc.
  - **Populando a quickfix:**
    - `:grep <pattern>` — grep externo (configurar `grepprg`; ripgrep recomendado).
    - `:vimgrep /<pattern>/ **/*.ts` — grep interno do Neovim.
    - Telescope `<C-q>` — manda resultados visíveis pra quickfix.
    - LSP references → `<C-q>` em Telescope manda tudo pra qf.
    - Externamente: `make` com `errorformat`. Compile errors caem na qf.
  - **Navegação:**
    - `:copen` abre o split, `:cclose` fecha.
    - `:cnext`/`:cprev` próximo/anterior. Em LazyVim, `]q`/`[q` é o keymap default.
    - `:cc N` pula pro item N.
    - `:cdo <cmd>` — executa `<cmd>` em cada item da qf list.
    - `:cfdo <cmd>` — executa em cada arquivo único da qf list (uma vez por arquivo, não por item).
  - **Edição em massa:**
    - **Padrão refactor LSP:**
      1. `gr` em símbolo → Telescope mostra references.
      2. `<C-q>` → quickfix.
      3. `:cdo s/oldName/newName/g | update`
    - **Padrão refactor grep:**
      1. `:grep -F oldName .` → qf populada.
      2. `:cdo s/oldName/newName/g | update`.
    - **Diff seguro:** abrir cada arquivo modificado e revisar; `:cfdo` faz uma passada por arquivo.
  - **Sessions:**
    - LazyVim bundle inclui `persistence.nvim`. Atalho: `<leader>qs` restore session (cwd), `<leader>ql` last, `<leader>qd` don't save.
    - Session = snapshot do layout (windows, buffers, tabs, marks, registers). NÃO inclui contents (arquivos são lidos de disco).
    - Cada cwd tem sua session em `~/.local/state/nvim/sessions/`.
    - Múltiplas sessions por projeto: usar `:mksession <nome>.vim` + `:source <nome>.vim`.
  - **todo-comments.nvim:**
    - Bundle LazyVim. Highlight de `TODO:`, `FIXME:`, `HACK:`, etc. no buffer.
    - `:TodoTelescope` ou `<leader>st` busca.
    - `:TodoQuickFix` envia tudo pra qf — combinável com `:cdo` se quiser remover/atualizar em massa.
- **Na prática:**
  - **Exemplo 1: refactor de método em projeto TS:**
    ```vim
    " Cursor no método `oldName`
    gr                           " LSP references in Telescope
    " <Tab> multi-select se quiser excluir alguns
    <C-q>                        " send to quickfix
    :cdo s/\<oldName\>/newName/g | update
    ```
  - **Exemplo 2: grep + filter + edit:**
    ```vim
    :grep -F "throw new" src/
    :copen                       " revisa
    " Edita a list (qf é editável com plugin como cdo+vim-qf — sem plugin, só nav)
    :cdo s/throw new Error/throw new AppError/g | update
    ```
  - **Exemplo 3: session pra projeto:**
    ```bash
    cd ~/projects/my-app
    nvim                         " abre LazyVim
    <leader>qs                   " restore session anterior (se existiu)
    " ... trabalha ...
    " Ao sair, persistence.nvim salva automático
    ```
  - **Exemplo 4: TODOs como qf:**
    ```vim
    :TodoQuickFix
    :copen
    " Lista todos os TODO/FIXME/HACK do projeto
    ]q / [q                       " navega
    ```
- **Armadilhas:**
  - (1) **`:cdo` em arquivos não-salvos** — se algum buffer da qf tem unsaved changes que conflitam com a edit, `:cdo` falha. Usar `update` (que só salva se mudou) ou `wall` antes.
  - (2) **Confundir `:cnext` (quickfix) com `:lnext` (location)** — comandos parecidos, listas diferentes. `]q` e `]l` no LazyVim diferenciam.
  - (3) **Telescope `<C-q>` envia só os visíveis (pós-filter)** — se você fuzzy-filtra `gr` e manda pra qf, a qf reflete o filtro, não todas as references. Pra todas: limpar input antes do `<C-q>`.
  - (4) **`:grep` overwrite sem confirm** — se houver qf carregada com refactor pendente, `:grep` sobrescreve sem aviso. Salvar com `:copen` + yank, ou usar `:lvimgrep` (location list) pra não tocar a qf.
  - (5) **Sessions não salvam buffers terminal** — terminais embutidos não persistem. Aceitável (recompõe rápido).
- **Em inglês:** lista de quickfix (quickfix list), correção em massa (bulk edit/find-and-replace), refatoração (refactoring), referências (references), sessão (session), restaurar (restore). 5-10 termos.
- **Veja também:** 03 (search base), 09 (LSP refs alimenta qf), 12 (Treesitter dá outro caminho de refactor), MOC, dicionário.
- **Referências:** `:help quickfix`, `:help session-file`, persistence.nvim, todo-comments.nvim, Steve Losh Vimscript hard way.

Tamanho-alvo: 400-500 linhas.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Vim / Neovim core`:

```markdown
### Quickfix list
Lista global de "lugares pra ir" no Neovim (resultados de grep, compile errors, LSP references, TODOs…). Editável em massa via `:cdo <cmd>`. Comandos: `:copen` (abre), `:cnext`/`:cprev` (navega), `:cc N` (item N). Em LazyVim: `]q`/`[q` é keymap default.

Veja também: [[11 - Workflow avançado]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/11 - Workflow avançado.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/11 - Workflow avançado.md"
```

Expected: ≥5 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/11 - Workflow avançado.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 11 — Workflow avançado"
```

---

## Task 14: Nota 12 — Treesitter avançado

**Files:**
- Create: `03-Dominios/Terminal/Editor/12 - Treesitter avançado.md`

**Conteúdo-chave do spec (§5, Magus):**

> O que Treesitter resolve. Textobjects ts-aware. Motion via textobjects. Swap/move. Queries customizadas. `:InspectTree`. Override de highlight.

**Verbetes referenciados:** Treesitter, AST, query, text object.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://github.com/nvim-treesitter/nvim-treesitter
WebFetch: https://github.com/nvim-treesitter/nvim-treesitter-textobjects
WebFetch: https://neovim.io/doc/user/treesitter.html
WebFetch: https://tree-sitter.github.io/tree-sitter/using-parsers
```

Capturar: textobjects canônicos (`@function.outer`, `@class.inner`), query syntax, install API.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Treesitter avançado"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - editor
  - magus
  - treesitter
  - ast
  - textobjects
aliases:
  - Treesitter
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "Treesitter dá ao Neovim AST por linguagem em tempo real. Beneficia highlight (preciso vs regex), text objects estruturais (`af` = around function), navegação por nó, e queries customizadas pro seu workflow."
- **O que é / Como funciona:**
  - **O problema que resolve:** highlight tradicional usa regex sobre regions de syntax. Frágil pra linguagens com sintaxe rica (TS, JSX, Rust). Treesitter usa parser por linguagem que gera AST incremental — re-parsa apenas o nó editado.
  - **AST:** árvore sintática abstrata. Cada nó tem `kind` (`function_declaration`, `if_statement`), `range` (linha/col start/end), e filhos.
  - **Highlight via TS:** `nvim-treesitter` consulta `highlights.scm` por linguagem e mapeia capture (`@function`, `@string.special`) pra grupos `Function`, `String`.
  - **Textobjects estruturais** (com `nvim-treesitter-textobjects`):
    - `af` (around function), `if` (inner function)
    - `ac` (around class), `ic` (inner class)
    - `aa` (around argument), `ia` (inner argument)
    - `al`/`il` (loop), `aB`/`iB` (block) — variam por language
  - **Motions estruturais:**
    - `]f`/`[f` — próxima/anterior função
    - `]c`/`[c` — próxima/anterior classe
    - `]a`/`[a` — argumento
  - **Swap/move:**
    - `<leader>a` swap argumento next; `<leader>A` swap previous (LazyVim default Extra).
    - `<leader>p` paste before; `<leader>P` paste after (estrutural).
  - **`:InspectTree`** — visualiza AST do buffer (split). Útil pra escrever queries.
  - **`:Inspect`** — sob o cursor: mostra capture e highlight group.
  - **Queries** (`.scm` files):
    - Linguagem de pattern matching da Tree-sitter. Sintaxe S-expression.
    - Captures: `(function_declaration name: (identifier) @function.name)`
    - Predicates: `(#match? @function.name "^test_")` filtra por regex.
    - Use cases: highlight custom, textobject custom, structural search.
  - **Override de highlight via query:**
    - Adicionar `~/.config/nvim/after/queries/<lang>/highlights.scm`:
      ```scheme
      ;; extends
      (call_expression
        function: (identifier) @function.builtin
        (#match? @function.builtin "^(it|describe|test)$"))
      ```
    - `;; extends` adiciona ao default; sem `extends`, substitui.
- **Na prática:**
  - **Exemplo 1: navegação estrutural em TS:**
    ```ts
    // cursor numa função grande
    // af + d → deleta a função inteira
    // ]f → próxima função
    ```
  - **Exemplo 2: rename argument com swap:**
    ```ts
    function foo(name, age) { ... }
    // cursor em `name` → <leader>a → vira: function foo(age, name) { ... }
    ```
  - **Exemplo 3: query custom pra destacar funções de teste:**
    Criar `~/.config/nvim/after/queries/typescript/highlights.scm`:
    ```scheme
    ;; extends
    (call_expression
      function: (identifier) @keyword.test
      (#any-of? @keyword.test "describe" "it" "test"))
    ```
    Recarregar com `:e` no buffer TS.
  - **Exemplo 4: usar `:InspectTree` pra entender estrutura:**
    Abrir um arquivo TS, `:InspectTree`. Move cursor em código → split mostra nó atual e ancestrais. Base pra escrever query.
- **Armadilhas:**
  - (1) **Parser não instalado** — sem o parser da linguagem, TS não funciona. `:TSInstall <lang>` (ou `:TSUpdate` pra atualizar todos). LazyVim auto-instala parsers comuns.
  - (2) **Highlight piora ao desabilitar TS** — alguns "feature" highlights (JSX attributes coloridos diferente) vêm de TS. Desabilitar volta a regex-based syntax (`syntax on`) que perde precisão.
  - (3) **Query syntax frágil** — vírgula extra, parêntese errado e a query inteira falha silenciosa (highlight não aplica). `:checkhealth nvim-treesitter` e logs ajudam.
  - (4) **`af` em filetype sem parser** — silenciosamente faz nada (ou volta ao default `af` se outro plugin definir). Verificar com `:InspectTree`.
  - (5) **Performance em arquivos enormes** — TS re-parseia incrementalmente, mas arquivo de 50k linhas pode lagger. `vim.treesitter.stop()` pra desabilitar buffer-local.
- **Em inglês:** árvore sintática (AST), parser, captura (capture), consulta (query), nó (node), filho (child), declaração de função (function declaration), bloco (block), incremental (incremental). 5-10 termos.
- **Veja também:** 02 (text objects base), 09 (LSP refs/symbols complementam — TS dá estrutura local; LSP dá semântica), 11 (refactor LSP+qf), MOC, dicionário.
- **Referências:** nvim-treesitter, treesitter-textobjects, `:help treesitter`, Tree-sitter query lang, TJ DeVries TS talks.

Tamanho-alvo: 450-550 linhas.

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Ecossistema LazyVim` (Treesitter, AST, query são jargão geral de editor moderno):

```markdown
### AST
Abstract Syntax Tree — árvore sintática abstrata. Representação hierárquica da estrutura de um código por um parser. Em Neovim, fornecida por Treesitter por linguagem; viabiliza highlight preciso, text objects estruturais e navegação por nó.

Veja também: [[12 - Treesitter avançado]].

### Query
Pattern em Tree-sitter (sintaxe S-expression em arquivos `.scm`) que casa contra a AST. Usada pra definir highlights, text objects, captures custom. Composta de patterns, captures (`@nome`) e predicates (`#match?`, `#any-of?`).

Veja também: [[12 - Treesitter avançado]].

### Treesitter
Biblioteca de parsing incremental (do GitHub). No Neovim, integrada via `nvim-treesitter` — gera AST por linguagem em tempo real, usada pra highlight preciso, text objects estruturais (`af`, `ic`), navegação por nó. Parsers instaláveis via `:TSInstall <lang>`.

Veja também: [[12 - Treesitter avançado]].
```

(text object já existe.)

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/12 - Treesitter avançado.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/12 - Treesitter avançado.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/12 - Treesitter avançado.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 12 — Treesitter avançado"
```

---

## Task 15: Nota 13 — Snippets e DAP

**Files:**
- Create: `03-Dominios/Terminal/Editor/13 - Snippets e DAP.md`

**Conteúdo-chave do spec (§5, Magus):**

> Snippets: estrutura (trigger, tabstops, placeholders, choice, transformations), LuaSnip básico, friendly-snippets, expansão integrada com nvim-cmp, criar snippet próprio.
> DAP: modelo cliente-servidor, adapter por linguagem, Extras de Debug, breakpoints, step, REPL/watch, `launch.json` interop, dap-ui.

**Verbetes referenciados:** snippet, LuaSnip, DAP.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://github.com/L3MON4D3/LuaSnip
WebFetch: https://github.com/mfussenegger/nvim-dap
WebFetch: https://github.com/rcarriga/nvim-dap-ui
WebFetch: https://microsoft.github.io/debug-adapter-protocol/
```

Capturar: spec de snippet (LuaSnip API + vscode JSON), DAP spec (events, requests).

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Snippets e DAP"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - editor
  - magus
  - snippets
  - luasnip
  - dap
  - debugging
aliases:
  - DAP
  - Snippets
  - LuaSnip
---
```

- [ ] **Step 3: Escrever a nota completa**

**Cobrir:**

- **TL;DR:** "LuaSnip é o snippet engine do LazyVim — expande triggers em código com tabstops navegáveis. DAP é Debug Adapter Protocol — debugger plugado no Neovim com breakpoints, step e REPL. Ambos opcionais mas multiplicam quando o flow é repetitivo (boilerplate) ou crítico (debug)."
- **Snippets — O que é:**
  - **Trigger:** texto que dispara a expansão (ex: `func` → `function foo() {}`).
  - **Tabstops:** `$1`, `$2`, `$0` — cursor pula entre eles com `<Tab>`/`<S-Tab>` (default LazyVim).
  - **Placeholders:** texto default no tabstop. `${1:name}` mostra `name` selecionado; digite pra substituir.
  - **Choice:** `${1|a,b,c|}` mostra menu com opções.
  - **Transformations** (LuaSnip Lua-side): tabstop derivado via função. Ex: gerar nome de teste a partir de nome de função.
- **Snippets — Na prática:**
  - **LuaSnip + friendly-snippets (default LazyVim):** já vem com snippets pra TS, JS, Lua, Markdown, etc. Listar: `:lua print(vim.inspect(require("luasnip").available()))`.
  - **Expansão:** em insert, digita trigger, `<Tab>` expande. Já dentro, `<Tab>`/`<S-Tab>` navega entre tabstops.
  - **Criar snippet vscode-style** (mais portável) em `~/.config/nvim/snippets/typescript.json`:
    ```json
    {
      "Test boilerplate": {
        "prefix": "test",
        "body": [
          "describe(\"$1\", () => {",
          "  it(\"$2\", () => {",
          "    $0",
          "  });",
          "});"
        ],
        "description": "Jest/Vitest test"
      }
    }
    ```
    Registrar via `lua/plugins/luasnip.lua` (opts ou config).
  - **Criar snippet em Lua puro:**
    ```lua
    local ls = require("luasnip")
    ls.add_snippets("typescript", {
      ls.snippet("log",
        ls.text_node({ "console.log('", "': ', " }):extend({ ls.insert_node(1, "msg"), ls.text_node("' ', " }), ls.insert_node(0), ls.text_node(");") })
    })
    ```
    (Forma simplificada acima — sintaxe real da LuaSnip API tem mais boilerplate; ver DOC.md pra exatidão.)
- **DAP — O que é:**
  - **Debug Adapter Protocol** (Microsoft, spec aberta). Editor é cliente; adapter por linguagem traduz pra debugger nativo (gdb, node inspector, debugpy…).
  - **Adapters:** node-debug2, debugpy (Python), codelldb (Rust/C++), delve (Go).
  - **Plugins core:**
    - `nvim-dap` — cliente DAP em Neovim
    - `nvim-dap-ui` — UI (scopes, watches, breakpoints, stacks)
    - `mason-nvim-dap` — instala adapters via Mason
  - **LazyVim Extras de Debug** — `:LazyExtras` → `dap/core`, `dap/<lang>` (TS, Python, Rust, Go, etc.).
- **DAP — Na prática:**
  - **Habilitar Extra:** `:LazyExtras` → toggle `lang.typescript` (já trazia LSP — Extra ativa também o dap quando disponível). Sync com `:Lazy sync`.
  - **Keymaps default LazyVim (após Extra habilitado):**
    - `<leader>db` toggle breakpoint
    - `<leader>dB` conditional breakpoint (prompt pra expressão)
    - `<leader>dc` continue
    - `<leader>di` step into
    - `<leader>do` step out
    - `<leader>dO` step over
    - `<leader>dr` toggle REPL
    - `<leader>du` toggle UI
  - **`launch.json` interop:** se o projeto tem `.vscode/launch.json`, DAP no Neovim lê automaticamente (via `nvim-dap-vscode-js` ou plugin equivalente). Configs de VS Code funcionam direto.
  - **Fluxo de debug:**
    1. Coloca breakpoint na linha (`<leader>db`).
    2. Roda config (`<leader>dc` ou `<leader>dn` pra "nearest test").
    3. Stop no breakpoint — `dap-ui` abre splits com scopes/watches/stacks.
    4. Inspect: hover sobre variável em scope; `<leader>du` toggle UI.
    5. Continue/step até resolver.
- **Armadilhas:**
  - **(snippets) 1:** Conflito com nvim-cmp — em LazyVim default, `<Tab>` faz cmp-confirm em popup. Se cmp não abre, `<Tab>` vai pra snippet. Se ambos esperam `<Tab>` no mesmo contexto, ordem de fallback importa — definida em `lua/plugins/nvim-cmp.lua`.
  - **(snippets) 2:** Snippets vscode-style precisam de path setado — `require("luasnip.loaders.from_vscode").lazy_load({ paths = "./snippets" })` em config. LazyVim faz isso default pra `friendly-snippets`; pra custom dir, override.
  - **(snippets) 3:** `$0` é tabstop final (cursor para aqui). Se esquecer, cursor fica no último `$N` declarado, surpresa.
  - **(DAP) 4:** Adapter não instalado — `:Mason` mostra disponíveis; pra Node TS, `js-debug-adapter`. Sem ele, "session ended early" ou "no adapter found".
  - **(DAP) 5:** Breakpoint condicional com syntax da linguagem errada — DAP pede expressão na linguagem do programa, não em Lua. Ex: em TS, `count > 10`, não `count > 10n` (BigInt) salvo se aplicável.
  - **(DAP) 6:** `launch.json` parse parcial — alguns campos VS Code-specific (`preLaunchTask`) não suportados em DAP Neovim. Verificar logs DAP (`:DapShowLog` em alguns Extras).
- **Em inglês:** trecho de código (snippet), gatilho (trigger), parada de tab (tabstop), placeholder, expansão (expansion), depurador (debugger), ponto de parada (breakpoint), passo (step), depurar (debug), REPL (REPL, sem tradução). 5-10 termos.
- **Veja também:** 04 (cmp+snippets keys default), 09 (LSP irmão; conform e mason compartilham infra), 12 (queries cobrem AST; DAP cobre runtime), MOC, dicionário.
- **Referências:** LuaSnip, friendly-snippets, nvim-dap, nvim-dap-ui, LazyVim Extras, DAP spec, TJ DeVries DAP overview.

Tamanho-alvo: 500-600 linhas (nota larga — aceitar; se uma das duas metades se mostrar autônoma o suficiente, perguntar ao usuário antes de splitar).

- [ ] **Step 4: Criar verbetes**

No Dicionário, bloco `## Avançado`:

```markdown
### DAP
Debug Adapter Protocol — protocolo open source (Microsoft) que padroniza comunicação entre editores e debuggers. Em Neovim: `nvim-dap` (cliente) + adapter por linguagem (instalável via Mason). UI: `nvim-dap-ui`.

Veja também: [[13 - Snippets e DAP]].

### LuaSnip
Snippet engine pra Neovim, escrita em Lua. Suporta snippets em Lua puro (mais expressivo) e em formato VS Code JSON (mais portável, pacotes como `friendly-snippets`). Integra com `nvim-cmp`.

Veja também: [[13 - Snippets e DAP]].

### Snippet
Trecho de código parametrizável que expande a partir de um trigger. Tabstops (`$1`, `$2`, `$0`) permitem navegação ordenada entre campos editáveis. Em Neovim moderno: LuaSnip (engine) + friendly-snippets (catálogo VS Code-style).

Veja também: [[13 - Snippets e DAP]].
```

Atualizar `updated:`.

- [ ] **Step 5: Validar rubrica**

```bash
test -f "03-Dominios/Terminal/Editor/13 - Snippets e DAP.md"
grep -c '\[\[' "03-Dominios/Terminal/Editor/13 - Snippets e DAP.md"
```

Expected: ≥6 wikilinks. Rubrica completa.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Editor/13 - Snippets e DAP.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-editor): add nota 13 — Snippets e DAP"
```

---

## ✅ Checkpoint Magus

Após Task 15, **todas as 13 notas estão escritas**. Antes da finalização:

- [ ] **Verificar coverage da barra de qualidade #6-10** (spec §4):
  6. Registers e marks rotineiramente — coberto por 10
  7. Gravar e editar macros — coberto por 10
  8. Refactoring de projeto (Telescope → quickfix → cdo) — coberto por 11
  9. Query Treesitter pra textobject customizado — coberto por 12
  10. Habilitar e usar DAP em uma linguagem — coberto por 13

---

## Task 16: Pass final no MOC

**Files:**
- Modify: `03-Dominios/Terminal/Editor/index.md`

**Objetivo:** Verificar que todos os wikilinks do MOC apontam pra notas existentes, atualizar `updated:`, declarar versão exata do LazyVim observada na sessão de execução.

- [ ] **Step 1: Verificar arquivos referenciados**

Run:
```bash
for n in "01 - Modal editing" \
         "02 - Motions, operadores e text objects" \
         "03 - Edição e navegação" \
         "04 - LazyVim tour" \
         "05 - Lua para Neovim" \
         "06 - Estrutura de config" \
         "07 - lazy.nvim" \
         "08 - Customizando LazyVim" \
         "09 - LSP no Neovim" \
         "10 - Registers, marks, macros" \
         "11 - Workflow avançado" \
         "12 - Treesitter avançado" \
         "13 - Snippets e DAP"; do
  test -f "03-Dominios/Terminal/Editor/${n}.md" && echo "ok: $n" || echo "MISSING: $n"
done
```

Expected: 13 linhas `ok:`. Qualquer `MISSING` = nota faltando, voltar à task correspondente.

- [ ] **Step 2: Capturar versão exata de LazyVim**

Pedir ao usuário (ou rodar no terminal interativo dele):
```vim
:Lazy
" Olhar header — mostra commit/data do LazyVim
```

Ou:
```bash
cd ~/.local/share/nvim/lazy/LazyVim 2>/dev/null && git log -1 --format="%h %ad" --date=short
```

Capturar a string (ex: `abc1234 2026-05-15`) pra inserir no MOC.

- [ ] **Step 3: Editar o MOC**

Edit em `03-Dominios/Terminal/Editor/index.md`:

- Trocar `updated: 2026-05-19` por `updated: 2026-XX-XX` (data da execução).
- Na seção `## Versões assumidas`, atualizar `LazyVim:` com a string capturada:
  ```markdown
  - **LazyVim:** `<hash> <data>` (capturado em <data execução>)
  ```

- [ ] **Step 4: Validar e commitar**

Run:
```bash
grep -c '\[\[' "03-Dominios/Terminal/Editor/index.md"
```

Expected: ≥15 wikilinks (13 notas + Dicionário + tronco + outras).

```bash
git add "03-Dominios/Terminal/Editor/index.md"
git commit -m "docs(terminal-editor): finaliza MOC do galho com versões e wikilinks ativos"
```

---

## Task 17: Pass final no Dicionário

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md`

**Objetivo:** Garantir alfabetização dentro de cada bloco temático, completar "Veja também" em todos verbetes, validar coverage (≥30 verbetes), atualizar `updated:`.

- [ ] **Step 1: Listar verbetes presentes**

Run:
```bash
grep -E '^### ' "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: ≥30 entradas (`###`). Lista esperada (do spec §7):

- **Vim/Neovim core:** modal editing, modo, motion, operador, text object, register, mark, macro, jump list, quickfix list, undotree, leader key, keymap, autocmd, buffer (≥15)
- **Ecossistema LazyVim:** distribuição, LazyVim, plugin manager, lazy.nvim, lazy-loading, plugin spec, Telescope, neo-tree, which-key, Treesitter, AST, query (≥12)
- **LSP & dev:** LSP, language server, Mason, nvim-lspconfig, nvim-cmp, code action, diagnostic, formatter, linter, format on save (≥10)
- **Avançado:** snippet, LuaSnip, DAP, Lua, init.lua (≥5)

Total esperado: ~42 verbetes.

- [ ] **Step 2: Verificar alfabetização dentro de cada bloco**

Inspecionar visualmente — cada `###` dentro de `##` deve estar em ordem alfabética (case-insensitive). Se houver fora de ordem, mover.

Script auxiliar:
```bash
python3 << 'EOF'
import re
content = open('03-Dominios/Terminal/Dicionário do Terminal.md').read()
blocks = re.split(r'^## ', content, flags=re.MULTILINE)[1:]
for b in blocks:
    name, *rest = b.split('\n', 1)
    body = rest[0] if rest else ''
    entries = re.findall(r'^### (.+?)$', body, re.MULTILINE)
    sorted_entries = sorted(entries, key=str.lower)
    if entries != sorted_entries:
        print(f'BLOCK "{name}" out of order:')
        for e, s in zip(entries, sorted_entries):
            mark = '!' if e != s else ' '
            print(f'  {mark} {e}  ->  {s}')
    else:
        print(f'ok: block "{name}" sorted ({len(entries)} entries)')
EOF
```

Expected: todas linhas começam com `ok:`. Qualquer `BLOCK ... out of order` = reordenar manualmente (Edit) e re-rodar o script.

- [ ] **Step 3: Verificar "Veja também" em cada verbete**

Cada verbete deve ter pelo menos uma linha `Veja também: [[<nota>]]` ao final.

```bash
python3 << 'EOF'
import re
content = open('03-Dominios/Terminal/Dicionário do Terminal.md').read()
verbetes = re.split(r'^### ', content, flags=re.MULTILINE)[1:]
missing = []
for v in verbetes:
    name = v.split('\n', 1)[0]
    if 'Veja também' not in v.split('\n###', 1)[0]:
        missing.append(name)
if missing:
    print('VERBETES sem "Veja também":')
    for m in missing:
        print(f'  - {m}')
else:
    print(f'ok: todos {len(verbetes)} verbetes têm "Veja também"')
EOF
```

Expected: `ok: ...`. Caso contrário, adicionar manualmente o "Veja também" ao verbete faltante.

- [ ] **Step 4: Atualizar `updated:`**

Edit no frontmatter:
```yaml
updated: 2026-XX-XX  # data da execução
```

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "docs(terminal): pass final no Dicionário — alfabetização e Veja também coverage"
```

---

## Task 18: Atualizar tronco — ativar wikilink do Editor

**Files:**
- Modify: `03-Dominios/Terminal/index.md`

**Objetivo:** Substituir o bullet de texto puro `Editor — galho 1 (planejado): ...` por wikilink ativo `[[03-Dominios/Terminal/Editor/index|Editor]]`, atualizar `updated:`.

- [ ] **Step 1: Ler o estado atual**

Run:
```bash
grep -n "Editor" "03-Dominios/Terminal/index.md"
```

Expected: encontra a linha `- Editor — galho 1 (planejado): Neovim + LazyVim (modal editing, plugins, LSP)`.

- [ ] **Step 2: Editar com Edit**

`old_string`:
```markdown
- Editor — galho 1 (planejado): Neovim + LazyVim (modal editing, plugins, LSP)
```

`new_string`:
```markdown
- [[03-Dominios/Terminal/Editor/index|Editor]] — galho 1: Neovim + LazyVim (modal editing, plugins, LSP, Treesitter, DAP)
```

- [ ] **Step 3: Atualizar `updated:`**

Edit no frontmatter:

`old_string`:
```yaml
updated: 2026-05-18
```

`new_string`:
```yaml
updated: 2026-XX-XX  # data da execução
```

- [ ] **Step 4: Validar wikilink**

Run:
```bash
test -f "03-Dominios/Terminal/Editor/index.md" && echo "ok: target existe"
grep -c '\[\[03-Dominios/Terminal/Editor' "03-Dominios/Terminal/index.md"
```

Expected: `ok: target existe`; count = 1.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Terminal/index.md"
git commit -m "feat(terminal): ativa wikilink do Editor no tronco — galho 1 entregue"
```

---

## Task 19: Validação final — build Quartz + verificar wikilinks

**Files:** nenhum (validação só).

**Objetivo:** Confirmar que tudo publica no Quartz sem erro e que não há red links no graph do galho.

- [ ] **Step 1: Listar artefatos do galho**

Run:
```bash
ls "03-Dominios/Terminal/Editor/"
ls "03-Dominios/Terminal/" | grep -i dicion
git log --oneline -25
```

Expected:
- 14 arquivos em `Editor/` (13 notas + `index.md`).
- 1 `Dicionário do Terminal.md` em `Terminal/`.
- ~17 commits novos (Task 1-15 + 16-18 finalização) com prefixos `feat(terminal-editor)`, `feat(terminal)`, `docs(terminal-editor)`, `docs(terminal)`.

- [ ] **Step 2: Build local do Quartz**

(Se Quartz não estiver clonado/configurado localmente, **pular este step e validar visualmente via `obsidian-cli` ou abrir no Obsidian**.) 

Assumindo que o site Quartz vive em `~/repos/personal/josenaldo.github.io/`:

```bash
cd ~/repos/personal/josenaldo.github.io
# Sync content do vault (script depende do setup; tipicamente):
npm run sync  # ou make sync, conforme o repo
npx quartz build
```

Expected: build sem erros. Se acusar wikilink quebrado:
- Investigar — provável typo de nome de arquivo.
- Corrigir no arquivo de origem.
- Re-commitar como `fix(terminal-editor): corrige wikilink quebrado em <nota>`.

- [ ] **Step 3: Verificar wikilinks usando skill verificar-wikilinks (se disponível)**

Se a skill `verificar-wikilinks` (mencionada no roadmap) estiver registrada como invocável:

```
/verificar-wikilinks 03-Dominios/Terminal/Editor/
```

Caso contrário, fallback bash:

```bash
# Lista wikilinks únicos referenciados nas notas do galho
grep -hoE '\[\[[^]|#]+' "03-Dominios/Terminal/Editor/"*.md | sort -u | sed 's/^\[\[//' | head -50
```

Para cada wikilink, conferir que o destino existe (arquivo `.md` correspondente). Esta validação é heurística — wikilinks pra verbetes do dicionário (`[[Dicionário do Terminal#Termo]]`) precisam do arquivo do dicionário existir (já existe) e do anchor existir (verbete dentro). Inspeção manual via Obsidian é mais confiável aqui.

- [ ] **Step 4: Validar critérios de aprovação (spec §12)**

Checklist final:

```
- [ ] 14 arquivos em 03-Dominios/Terminal/Editor/ (Step 1 confirmou)
- [ ] Dicionário do Terminal criado com ≥30 verbetes (Task 17 confirmou)
- [ ] Todos com publish: true (verificar: grep publish: nos arquivos)
- [ ] MOC tem TL;DR + Iniciado/Adepto/Magus + Rotas + Veja também (Task 16)
- [ ] Cada nota satisfaz rubrica (verificado em cada Task 3-15)
- [ ] Tronco com wikilink ativo do Editor (Task 18)
- [ ] Quartz publica sem erro (este Step)
- [ ] Pelo menos 4 notas testaram config localmente (notas 04, 06, 08, 09 tiveram step)
```

Run:
```bash
grep -L "publish: true" "03-Dominios/Terminal/Editor/"*.md "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Expected: vazio (sem arquivos sem `publish: true`). Qualquer output = corrigir frontmatter.

- [ ] **Step 5: Commit "wrap-up" (opcional)**

Se houve correções aqui (typos, wikilinks), commitar:

```bash
git add -A
git status
git commit -m "fix(terminal-editor): correções pós-validação"
```

Se nenhuma correção, **não criar commit vazio** — passar pra Task 20.

---

## Task 20: Wrap-up e handoff

**Files:** nenhum.

- [ ] **Step 1: Sumário ao usuário**

Reportar:
- 13 notas + 1 MOC + 1 Dicionário criados.
- Total de verbetes no Dicionário: N (rodar `grep -c '^### ' "03-Dominios/Terminal/Dicionário do Terminal.md"`).
- Total de commits criados nesta sessão (rodar `git log --oneline | grep terminal | wc -l`).
- Build Quartz: passou / falhou (com detalhes).
- Critérios da spec §12 atendidos / abertos (lista).

- [ ] **Step 2: Confirmar com usuário se quer push**

**NÃO fazer `git push` sem confirmação explícita do usuário** (regra geral — push afeta estado remoto).

Perguntar: "Galho 1 pronto. Push para origin/main, ou quer revisar antes?"

- [ ] **Step 3: Sugestão de próxima sessão**

Se o usuário quiser continuar o roadmap, próximo galho recomendado conforme o tronco: **Shell (galho 2)** — Zsh + Oh-My-Zsh + Powerlevel10k. Criar arquivo `docs/superpowers/specs/PROXIMA-SESSAO-galho-2-shell.md` análogo (opcional, perguntar antes — usuário pode preferir saltar pra outro galho).

---

## Critério de pronto

O galho 1 está pronto quando **todas** as Tasks 0-20 têm seus steps marcados (`- [x]`), e:

- 14 arquivos em `03-Dominios/Terminal/Editor/` (13 notas + index.md)
- 1 dicionário em `03-Dominios/Terminal/Dicionário do Terminal.md` com ≥30 verbetes
- Tronco `Terminal/index.md` com wikilink ativo do Editor
- Build local do Quartz passa (Task 19 Step 2) **ou** validação manual de wikilinks foi feita
- Nenhum commit do galho leva `Co-Authored-By: Claude`
- Nenhum arquivo do galho referencia conteúdo do apocrypha
- A barra de qualidade #1-10 do spec §4 está coberta (verificada em Checkpoints Iniciado/Adepto/Magus)

## Não faz parte deste plano

- Criar pastas de outros galhos (Shell, Multiplexer, etc.) — cada galho tem sessão própria.
- Atualizar dashboards/bases que listam todas as notas publicadas — verificar fora deste plano.
- Push pra remoto sem confirmação do usuário.
- Apagar `docs/superpowers/specs/PROXIMA-SESSAO-galho-1-editor.md` — já foi removido em pré-sessão; se ressurgir, é bug.
- Renomear ou splitar notas grandes (04, 13) **sem perguntar** primeiro — decisão na execução, com input do usuário.
