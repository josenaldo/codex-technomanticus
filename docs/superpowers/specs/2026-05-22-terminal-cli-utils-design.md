---
title: "Spec — Galho 6 da trilha Terminal (CLI Utils)"
date: 2026-05-22
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 6 da trilha Terminal (CLI Utils)

## 1. Contexto e motivação

Este é o **sexto galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`; galhos 1-5 já entregues: Editor, Shell, Multiplexer, TUIs de Dev, Dotfiles). Pressupõe leitura do roadmap.

O usuário tem **adoção zero** em todas as 14 ferramentas previstas (`fzf`, `ripgrep`, `bat`, `eza`, `zoxide`, `atuin`, `jq`, `yq`, `tldr`, `cheat`, `delta`, `dust`, `btop`, `htop`). Sistema tem `rg 14.1.0`, `jq 1.7`, `htop 3.3.0`, `fdfind 9.0.0` instalados como dependências indiretas, mas nenhuma é usada conscientemente. A trilha é pedagógica de verdade — começa do "ao adotar X, o ganho central é Y" e termina em composição cross-tool.

O master roadmap previu **9 notas** (4+3+2). Após brainstorm, o escopo é expandido pra **13 notas** (4+4+5):

- Iniciado mantém 4 (fzf, rg+fd, bat, eza) — fd vem junto com rg como ferramentas irmãs, em vez de aparecer solto na nota magus de monitores.
- Adepto vira 4 (zoxide, atuin, jq, yq separados) — jq tem DSL própria; yq tem armadilha das **duas implementações populares** (Mike Farah Go vs kislyuk Python) que justifica nota dedicada.
- Magus vira 5 (tldr+cheat, delta, monitores, **stack interativo**, **pipeline JSON/YAML**) — duas notas capstone de composição, capturando workflows reais.

**Todos os exemplos** das notas são neutros (`alice`, `myproj`, `example.com`) ou hipotéticos explícitos (`# hipotético: ...`). Sem fabricação de uso pessoal — o usuário ainda não usa nenhuma das ferramentas.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **13 notas atômicas + 1 MOC do galho + expansão do Dicionário do Terminal** em `03-Dominios/Tecnologia/Terminal/CLI Utils/` e `03-Dominios/Tecnologia/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (4 Iniciado + 4 Adepto + 5 Magus).

A trilha precisa ser:

- **Pedagógica** — leitor sem conhecimento prévio entende o ganho de adotar fzf ao final da nota 01; o trade-off rg vs grep ao final de 02; a confusão das duas yq ao final de 08. Capstone (12-13) mostra o sistema operando junto.
- **Honesta** — comandos testáveis, comparações justas (`quando X vence` E `quando Y vence`), versões hedged ("0.4x+; verifique localmente") em vez de pins específicos que envelhecem.
- **Atômica** — cada nota cobre um tópico bem-delimitado; cross-references ricos via wikilinks e Dicionário.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Terminal/CLI Utils/`)

Pasta nova, flat. 13 notas + 1 MOC:

#### Iniciado (4 notas — núcleo dia-a-dia)

| #  | Nota |
|----|------|
| 01 | fzf — fuzzy finder universal |
| 02 | ripgrep e fd — buscar conteúdo (rg) e nomes (fd) |
| 03 | bat — cat moderno com syntax highlight |
| 04 | eza — ls moderno |

#### Adepto (4 notas — produtividade interativa + dados)

| #  | Nota |
|----|------|
| 05 | zoxide — cd inteligente baseado em frecency |
| 06 | atuin — history shell em SQLite com sync E2E |
| 07 | jq — processor JSON com DSL própria |
| 08 | yq — processor YAML (e a armadilha das duas implementações) |

#### Magus (5 notas — composição e operacional)

| #  | Nota |
|----|------|
| 09 | tldr e cheat — docs práticas em fluxo |
| 10 | delta — pager moderno pra git diff |
| 11 | Monitores e disco — btop + htop + dust |
| 12 | Stack interativo — composição fzf + zoxide + atuin |
| 13 | Pipeline JSON e YAML — composição jq + yq + fzf + curl/kubectl |

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Terminal/CLI Utils/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "CLI Utils"`, tags `terminal/cli-utils/moc`, aliases `["MOC CLI Utils", "Galho 6"]`)
- TL;DR callout (galho cobre subs UNIX modernas + fluxo interativo + processamento estruturado)
- Conteúdo agrupado em 3 H3 (Iniciado / Adepto / Magus) com wikilinks pras 13 notas
- **Tabela de substituições clássicas → modernas** (cat→bat, ls→eza, grep→rg, find→fd, cd→zoxide, history→atuin, du→dust, top→btop/htop, man→tldr/cheat, git diff→delta) — substitui a necessidade de uma nota "migration map" dedicada
- Bloco "Versões assumidas" preenchido no pré-flight
- "Veja também": tronco + Shell (galho 2) + Dicionário

### 3.3. Expansão do Dicionário do Terminal

`03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` ganha **novo bloco** `## CLI Utils` (após `## Dotfiles`, linha 562+), com ~40 verbetes em ordem alfabética case-insensitive (sem acento).

**Verbetes já existentes que apenas serão wikilinkados** (sem duplicar):

| Verbete existente | Onde está | Notas que linkam |
|---|---|---|
| Nerd Font | `## Shell / Zsh / OMZ` | 03 (bat), 04 (eza) |
| Whitelist (.gitignore) | `## Dotfiles` | 02 (rg+fd) — conceito relacionado |
| Telescope | `## Ecossistema LazyVim` | 01 (fzf) — fuzzy finder no Neovim |

**Verbetes novos** (~40, listados aqui em ordem alfabética conforme aparecerão no bloco):

| Verbete | Resumo (esqueleto) | Origem |
|---|---|---|
| anchors e aliases (YAML) | Mecanismo YAML pra reusar nós (`&name`, `*name`); preservação difere entre yq Go e Python | 08, 13 |
| atuin | History shell em SQLite com fuzzy search e sync E2E-encrypted opcional | 06, 12 |
| bat | cat moderno com syntax highlight, line numbers, integração git | 03, 09, 10 |
| BAT_THEME | Env var pra tema do bat; lista em `bat --list-themes` | 03 |
| batcat | Nome do binário do bat no Debian/Ubuntu (colisão com `bacula-console`) | 03 |
| btop | TUI moderna de monitoramento; gráficos, mouse, presets em `~/.config/btop` | 11 |
| cheatsheet | Folha de uso prático curta e runnable (cheat.sh, cheat CLI) | 09 |
| delta | Pager pra git diff/show/log/blame com syntax highlight | 10 |
| dust | du moderno em árvore por tamanho com gráfico horizontal | 11 |
| E2E encryption (history sync) | Encryption fim-a-fim aplicada ao histórico de shell sincronizado | 06 |
| eza | ls moderno; fork ativo do exa (arquivado) | 04 |
| exa (legado) | ls moderno original; arquivado em 2023; sucessor é eza | 04 |
| EZA_COLORS | Env var de cores customizadas pro eza; sintaxe ≠ LS_COLORS | 04 |
| extended search syntax (fzf) | Linguagem de match do fzf: `^prefix`, `suffix$`, `'exact`, `!neg` | 01, 12 |
| fd | find moderno; respeita .gitignore por padrão; sintaxe simples | 02, 12, 13 |
| fdfind | Nome do binário fd no Debian/Ubuntu (colisão com daemon antigo) | 02 |
| frecency | Métrica combinada de frequency + recency; zoxide e atuin usam | 05, 06 |
| fuzzy finder | Ferramenta de match aproximado em listas; fzf é o canônico | 01, 12 |
| FZF_DEFAULT_OPTS | Env var com flags default do fzf; aplica em toda invocação | 01, 12, 13 |
| gitignore-aware | Comportamento de respeitar `.gitignore` por padrão (rg, fd, eza --git) | 02, 04 |
| htop | Monitor clássico de processos com TUI; leve e ubíquo | 11 |
| init script (shell) | Trecho que tools (zoxide/atuin/fzf) injetam em `.zshrc`/`.bashrc` | 05, 06, 12 |
| jq | Processor JSON com DSL de pipeline de filtros | 07, 13 |
| MANPAGER | Env var pra pager de manpages; comum apontar pra bat | 03 |
| OSC 8 | Escape sequence pra hyperlinks clicáveis em terminais que suportam | 10 |
| pipefail | Opção shell (`set -o pipefail`) que propaga exit code de pipes | 13 |
| preview window (fzf) | Painel auxiliar do fzf que renderiza preview do item highlighted | 01, 12 |
| raw output (jq -r) | `-r` em jq emite strings sem aspas; essencial pra pipar texto | 07 |
| ripgrep | grep moderno em Rust; .gitignore-aware, regex Rust, paralelismo | 02, 13 |
| slurp (jq -s) | `-s` em jq lê stdin inteiro como array (vs streaming por documento) | 07 |
| smart-case | Matching case-insensitive até aparecer maiúscula na query | 02 |
| syntax pager | Pager que aplica syntax highlight (bat, delta) | 03, 10 |
| tldr-pages | Repo comunitário de pages curtas e práticas; cliente `tldr` | 09 |
| TTY detection | Detecção de stdout=terminal vs pipe; ferramentas mudam output conforme | 03 |
| xargs -r | Flag pra não executar comando quando lista de entrada é vazia | 13 |
| YAML multi-doc | Múltiplos documentos YAML separados por `---` em um arquivo | 08 |
| yq (Go) | Impl yq de Mike Farah, em Go; sintaxe estilo jq; default em brew | 08, 13 |
| yq (Python/kislyuk) | Impl yq de Andrey Kislyuk, em Python; wrappa jq; sintaxe = jq | 08 |
| zoxide | cd inteligente baseado em frecency; substitui `cd` no shell | 05, 12 |
| zsh widget | Função zsh registrada pra responder a keypress (zoxide/atuin/fzf usam) | 12 |

Cada verbete tem `Veja também:` apontando pras notas canônicas.

### 3.4. Tronco — ativar wikilink

`03-Dominios/Tecnologia/Terminal/index.md` linha 32: trocar `- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…` por `- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|CLI Utils]] — galho 6: substituições modernas de utilitários UNIX (cat/ls/grep/find/du/top) + fluxo interativo (fzf/zoxide/atuin) + processamento estruturado (jq/yq)`.

## 4. Convenções por nota

Mesmo padrão consolidado nos galhos 2-5.

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - terminal
  - cli-utils
  - <fase>
  - <tags específicas, ex: fzf, ripgrep, json, yaml, monitor>
aliases:
  - <aliases>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2)
- `## O que é / Como funciona` — H3s conforme tópico
- `## Na prática` — exemplos runnable, configs reais; framing "ao adotar X, o ganho é Y" (NUNCA "no meu setup")
- `## Armadilhas` — **≥5**, cada uma com **formato bold-label** (`### (N) Título` + 4 labels: `**Causa:**`, `**Sintoma:**`, `**Como detectar:**`, `**Solução:**`). NUNCA callouts Obsidian.
- `## Em inglês` — bullets bilíngues `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
- `## Veja também` — wikilinks SEM backticks; sempre inclui:
  - Notas relacionadas do galho
  - `[[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]`
  - `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
  - Wikilinks pros verbetes do Dicionário
- `## Referências` — docs oficiais + posts canônicos

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `myproj`, `example.com`) ou hipotéticos explícitos (`# hipotético: ...`). NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de comandos/flags. Cada flag/opção verificável via doc oficial (WebFetch obrigatório no Step 1 de cada nota).
3. **Sem `Co-Authored-By: Claude`** em commits. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em "Veja também".
6. **Tronco wikilink obrigatório** em "Veja também".
7. **MOC wikilink obrigatório** em "Veja também".
8. **Code fences corretos:** ` ```bash ` pra shell, ` ```json ` pra JSON, ` ```yaml ` pra YAML, ` ```jq ` quando suportado (fallback `bash`), ` ```text ` pra ASCII/output. Sempre fechadas.
9. **Defaults documentados** quando relevante (ex: rg respeita .gitignore por default; fd ignora hidden por default).
10. **Comparações justas** — quando comparar com alternativa clássica (rg vs grep, eza vs ls), incluir "quando esta vence" E "quando a clássica vence". Sem hype, sem desmerecimento.
11. **Versões hedged** — "fzf 0.4x+; verifique `fzf --version` localmente" em vez de pin específico que envelhece.
12. **Tom pedagógico** — assume zero conhecimento prévio em Iniciado; sobe gradualmente até Magus.
13. **Stage explícito por arquivo** — `git add <path>` nominal; NUNCA `git add -A` (working tree pode ter mudanças não-relacionadas).

## 5. Conteúdo por nota (síntese)

### Iniciado

**01 — fzf**
- O que é: fuzzy finder universal — lê stdin, escreve stdout selecionado. Vira motor de seleção pra qualquer pipeline.
- Como funciona: algoritmo fuzzy + extended search syntax (`^prefix`, `suffix$`, `'exact`, `!negate`, `|` alternation), preview window (`--preview`), key-bindings shell, integração com Vim/Neovim.
- Na prática: Ctrl-R (history), Ctrl-T (file), Alt-C (cd); shell integration (Zsh key-bindings + completion); `FZF_DEFAULT_OPTS`, `FZF_DEFAULT_COMMAND`; preview com bat (`--preview 'bat --color=always {}'`); composição custom (`git branch | fzf`, `ps aux | fzf`).
- Armadilhas: extended syntax confusa (`'exact` vs `^prefix`); preview lento sem nohidden; FZF_DEFAULT_COMMAND ignorando .gitignore se for `find` cru (use `fd` ou `rg --files`); bindings conflitando com Zellij; binários no preview quebrando layout.
- Verbetes que contribui: fuzzy finder, extended search syntax, preview window, FZF_DEFAULT_OPTS.

**02 — ripgrep e fd**
- O que é: rg busca conteúdo recursivo; fd busca nomes de arquivo. Ambos respeitam .gitignore por padrão, Rust regex, paralelismo nativo. Ferramentas irmãs (filosofia burntsushi).
- Como funciona: smart-case; tipos de arquivo (`-t py`, `-e py`); recortes (`-A 3`, `-B 3`, `-C 3`); saída JSON pra integração (`rg --json`); composição (`fd ... -x rg ...`); `--no-ignore` quando precisa olhar tudo (incluindo `node_modules`).
- Na prática: `rg "TODO"`, `rg -t py "import requests"`, `rg --json | jq`, `fd -t f -e ts`, `fd 'config' --hidden`, `fd -t f -e py -x rg 'pdb'`.
- Armadilhas: `.gitignore` comendo arquivos esperados (use `--no-ignore`); regex flavor Rust ≠ PCRE (sem look-behind por default; `-P` ativa PCRE2 se compilado); smart-case surpreendendo com maiúscula na query; fd hidden ignorados por padrão (`-H`); **`fdfind` vs `fd` em Debian/Ubuntu** (alias necessário).
- Verbetes: ripgrep, fd, smart-case, gitignore-aware, fdfind.

**03 — bat**
- O que é: cat com syntax highlight, line numbers, paginação inteligente, integração git (mostra changes inline).
- Como funciona: `BAT_THEME`, `BAT_PAGER`, TTY detection (em pipe vira cat puro automaticamente), integração com `MANPAGER`, integração com fzf preview, modo diff (`--diff`).
- Na prática: `bat file.py`, `bat -n file`, `bat --diff file`, `MANPAGER="sh -c 'col -bx | bat -l man -p'"`; integração `git diff` (via delta na nota 10); `--plain` pra cat-puro forçado.
- Armadilhas: aliasing `cat=bat` quebra alguns scripts (TTY detection é boa mas não perfeita); `BAT_PAGER=less` precisa `-R` pra cores; binários abrindo no pager; **`batcat` vs `bat` em Debian/Ubuntu**; theme escuro/claro precisa coordenar com terminal.
- Verbetes: bat, BAT_THEME, MANPAGER, TTY detection, batcat, syntax pager.

**04 — eza**
- O que é: ls moderno; fork ativo do **exa** (arquivado em agosto 2023).
- Como funciona: `-l` (long), `-a` (all), `--tree` (árvore), `--git` (status git inline), `--icons` (Nerd Font), `--color-scale=size`; sorting (`--sort=size`, `--sort=modified`).
- Na prática: `eza -lah`, `eza --tree -L 2`, `eza -l --git`, aliases sugeridos (`alias ls=eza`, `alias ll='eza -lah --git'`, `alias tree='eza --tree'`).
- Armadilhas: ícones requerem **Nerd Font** instalada E configurada no terminal; `alias ls=eza` quebra scripts que esperam flags ls(1) clássicos (ex: `ls -la` em script CI); `--git` lento em repos grandes (cached mas primeira chamada); ordenação default ≠ lexicográfica (use `--sort=name`); `EZA_COLORS` ≠ `LS_COLORS` (sintaxe diferente).
- Verbetes: eza, exa (legado), EZA_COLORS, Nerd Font (já existe, só linka).

### Adepto

**05 — zoxide**
- O que é: cd inteligente baseado em **frecency** (frequency + recency).
- Como funciona: mantém DB local de pastas visitadas em `~/.local/share/zoxide`; pontuação combina quantas vezes e quão recente; init script no shell substitui (ou suplementa) `cd`.
- Na prática: install + add ao shell init (`eval "$(zoxide init zsh)"`); `z foo` matching substring com pontuação; `zi foo` interactive (precisa fzf); migração de autojump/`z.sh`; `zoxide query --list` (debug).
- Armadilhas: init script ordering importa (depois do plugin manager, antes de outros plugins que mudam cd); `zi` requer fzf instalado; matching surpresa em substrings curtas (`z d` pode pular pra qualquer pasta com `d`); DB não migra entre máquinas (sem sync nativo); conflito com aliases `cd` em ambientes (containers, CI).
- Verbetes: zoxide, frecency, init script (shell).

**06 — atuin**
- O que é: history shell em **SQLite** com fuzzy search; substitui Ctrl-R nativo; sync opcional E2E-encrypted (self-host ou atuin.sh).
- Como funciona: instalar + import history (`atuin import zsh`); modes (`prefix`, `fulltext`, `fuzzy`); `atuin stats` mostra agregados (top commands, dias mais ativos); sync = SQLite local + cliente sincronizando com servidor.
- Na prática: setup; Ctrl-R abre TUI atuin (filtros + preview); `atuin search --interactive --search-mode fuzzy "git"`; `atuin stats`; configurar `secrets_filter` em `~/.config/atuin/config.toml` pra não armazenar comandos com tokens.
- Armadilhas: `atuin import` precisa shell certo (`bash`, `zsh`, `fish`); sync sem self-host = confiar em atuin.sh (E2E mas trust do provider); segredos no histórico viajando no sync (configurar `secrets_filter` regex); SQLite lock em multi-shell heavy use (DB ocupada); reset acidental (`atuin db delete`) sem backup perde tudo.
- Verbetes: atuin, history sync, E2E encryption (history sync), frecency (já em zoxide, linka).

**07 — jq**
- O que é: processor JSON com DSL própria — pipeline de filtros sobre objetos/arrays.
- Como funciona: filtros básicos (`.`, `.foo`, `.[]`, `.foo.bar`); operadores (`|` pipe, `,` coletor); funções (`select`, `map`, `reduce`, `length`, `keys`); `-r` raw output; `--arg`/`--argjson` injeção; `-s` slurp (junta inputs em array); `-e` exit code não-zero se filtro vazio.
- Na prática: `cat data.json | jq .`, `jq '.users[] | select(.active)'`, `jq -r '.users[].email'`, `jq --arg name "alice" '.users[] | select(.name == $name)'`, `jq -s 'add' file1.json file2.json`, `jq -e '.error // empty'`.
- Armadilhas: `-r` faltando = strings com aspas (quebra pipe pra cd, ssh, etc.); `select` filtra, `map` transforma (confusão clássica); `null` em chave faltante vs erro (`?` torna opcional); números float vs int (jq não distingue, perde precisão em 64-bit ints como Twitter IDs); UTF-8 BOM no input quebra parser.
- Verbetes: jq, raw output (jq -r), slurp (jq -s).

**08 — yq**
- O que é: processor YAML/JSON/XML — **armadilha central são as DUAS implementações populares com sintaxe diferente** (Mike Farah em Go vs Andrey Kislyuk em Python wrappa jq).
- Como funciona:
  - **yq (Go)**: sintaxe própria estilo jq mas não idêntica; default em Homebrew; `yq '.foo.bar' file.yaml`; modo in-place (`-i`); merge (`*`).
  - **yq (Python/kislyuk)**: wrappa jq; sintaxe idêntica a jq mas opera em YAML; convert paths diferentes.
- Detecção: `yq --version` mostra qual é. Default em brew = Go; default em pip = Python.
- Na prática: `yq '.spec.template.spec.containers[0].image' deployment.yaml`; modificar in-place (`yq -i '.image = "nginx:latest"' file.yaml`); converter YAML→JSON pra usar com jq (`yq -o json file.yaml | jq ...`); merge multi-doc (`yq eval-all '. as $item ireduce ({}; . * $item)' *.yaml`).
- Armadilhas: **confundir as duas impls** (footgun central — copiar exemplo da web e ele não funciona pq é da outra impl); preservação de comments entre Go e Python ≠; multi-doc (`---`) suporte ≠; anchors e aliases comportamento ≠; instalar acidentalmente a outra (apt instala Python, brew instala Go, pip instala Python).
- Verbetes: yq (Go), yq (Python/kislyuk), YAML multi-doc, anchors e aliases (YAML).

### Magus

**09 — tldr e cheat**
- O que é: docs práticas em fluxo — **tldr-pages** é comunidade global de pages curtas; **cheat** é cheatsheets locais + customizáveis.
- Como funciona:
  - tldr: cliente baixa pages do repo tldr-pages (markdown); cache local pra offline; `tldr --update` atualiza cache.
  - cheat: cheatsheets em `~/.config/cheat/cheatsheets/`; community sheets em `~/.config/cheat/cheatsheets/community`; editor inline (`cheat -e <name>`); search (`cheat -s <pattern>`).
- Na prática: `tldr tar` (resumo rápido); `tldr --list-platforms`; `cheat -e tar` (cria/edita); `cheat -l` (lista); criar cheatsheet próprio pra comandos comuns.
- Armadilhas: tldr-pages podem estar desatualizadas (PRs welcome — armadilha amplificada por traduções); cheat versão Go (atual) ≠ cheat Python (legado, descontinuado); cache local de tldr quando offline (`--offline`); pages traduzidas inconsistentes com inglês (use `-L en` se prefere fonte original); tldr não substitui man — man tem invariantes, edge cases, opções completas.
- Verbetes: tldr-pages, cheatsheet.

**10 — delta**
- O que é: pager moderno pra git diff/show/log/blame com syntax highlight (engine syntect).
- Como funciona: configura em `~/.gitconfig` (`[core] pager = delta`); `[interactive] diffFilter = "delta --color-only"`; features (`navigate` = n/N keys, `side-by-side`, `line-numbers`, `hyperlinks` = OSC 8); presets via `[delta] features = ...`; integração com bat themes (`syntax-theme = ...`).
- Na prática:
  ```toml
  [core]
      pager = delta
  [interactive]
      diffFilter = delta --color-only
  [delta]
      navigate = true
      light = false
      side-by-side = true
      line-numbers = true
      syntax-theme = Dracula
  [merge]
      conflictStyle = diff3
  [diff]
      colorMoved = default
  ```
- Standalone (sem git): `diff a b | delta`.
- Armadilhas: config errada em `~/.gitconfig` é silenciosa (delta nem roda, less assume); side-by-side precisa terminal largo (>180 cols efetivos com line numbers); hyperlinks (OSC 8) só funcionam em terminais que suportam (kitty, wezterm, recent gnome-terminal); performance em diffs gigantes (`--max-line-length` ajuda); conflito com `[pager]` global que outras tools usam (ex: `git config --global pager.diff false`).
- Verbetes: delta, syntax pager (já em bat, linka), OSC 8.

**11 — Monitores e disco (btop + htop + dust)**
- O que é: três ferramentas — **btop** (TUI moderna), **htop** (clássico leve), **dust** (du em árvore por tamanho).
- Como funciona:
  - btop: TUI rica (gráficos, mouse, themes); presets configuráveis; `--tty_on` pra ssh com bandwidth baixo.
  - htop: TUI clássica; F-keys (F9 kill, F2 setup, F3 search); usa /proc; processa árvore (F5).
  - dust: árvore por tamanho com barras horizontais; `dust -d 3 -n 30` (depth 3, top 30); `--ignore-directory`.
- Na prática: htop em ssh resource-baixo (default leve); btop em workstation (mais info, persistente); dust pra "quem comeu meu disco?" (mais legível que `du -sh` em loop); flags úteis (`htop -d 1` refresh 1s; `btop --tty_on` modo TTY-friendly; `dust -d 3 -n 30 ~`).
- Armadilhas: btop em ssh com bandwidth baixo lag (`--tty_on` ajuda); htop kill em árvore (F9 em parent) pode matar wrong process (confirme com `tree` view); dust **não respeita .gitignore por padrão** (lista `node_modules` cheio — use `--ignore-directory node_modules`); btop config persistido em `~/.config/btop/btop.conf` (versionar com cuidado, é OS-específico); contagem RAM Linux ≠ "memória disponível" (cached + buffers contam como available; htop/btop mostram diferente do que parece).
- Verbetes: btop, htop, dust.

**12 — Stack interativo (fzf + zoxide + atuin)**
- O que é: **capstone** — as 3 ferramentas Iniciado/Adepto compondo o fluxo diário. Assume leitura das 3 notas individuais.
- Como funciona: zoxide pula pastas (`z foo`); atuin substitui Ctrl-R com fuzzy search; fzf é motor de seleção compartilhado (`zi` usa fzf; atuin interactive usa fzf-like layout própria); FZF_DEFAULT_OPTS aplicado em tudo.
- Na prática:
  - Shell init order (importa):
    ```bash
    # ~/.zshrc — order matters
    eval "$(zoxide init zsh)"           # zoxide primeiro
    eval "$(atuin init zsh)"            # atuin depois (sobrescreve Ctrl-R)
    [ -f ~/.fzf.zsh ] && source ~/.fzf.zsh  # fzf por último
    ```
  - Receitas combinadas:
    ```bash
    # Trocar branch via fzf
    git checkout "$(git branch --format='%(refname:short)' | fzf)"

    # zoxide-pulando com preview
    cd "$(zoxide query -l | fzf --preview 'eza --tree -L 1 {}')"

    # Atuin filtrar por dir + fzf select
    atuin search --search-mode fuzzy --cwd "$(pwd)" | fzf
    ```
  - FZF_DEFAULT_OPTS compartilhado:
    ```bash
    export FZF_DEFAULT_OPTS="--height 60% --layout=reverse --border --preview-window=right:50%:wrap"
    ```
- Armadilhas: init order quebra Ctrl-R (atuin precisa sobrescrever após plugins Zsh que também mexem em Ctrl-R); zsh widget collisions (zoxide tenta bindar mesma key que algum plugin); FZF_DEFAULT_OPTS com preview pesado lentando todo uso; atuin e zoxide ambos rastreando "lugares" de jeitos diferentes (atuin = cwd no momento do comando; zoxide = pastas onde fez cd) — não conflita mas confunde; reinstalar shell init via dotfile reset quebra silenciosamente (sem erro até abrir shell novo).
- Verbetes: zsh widget, init script (já em zoxide, linka).

**13 — Pipeline JSON e YAML (jq + yq + fzf + curl/kubectl)**
- O que é: receitas reais de pipeline composto pra processar dados estruturados em fluxos cotidianos.
- Como funciona: `curl | jq | fzf` pra explorar API; `kubectl get -o json | jq` pra filtrar k8s resources; `yq -o json | jq` pra usar yq Go com sintaxe jq; jq dentro de scripts com error handling.
- Na prática:
  - Explorar API:
    ```bash
    curl -s https://api.github.com/repos/cli/cli/issues | \
      jq -r '.[] | "\(.number)\t\(.title)"' | \
      fzf | awk '{print $1}'
    ```
  - Kubernetes filtering:
    ```bash
    # Pods com status NotReady
    kubectl get pods -o json | \
      jq -r '.items[] | select(.status.containerStatuses[]?.ready == false) | .metadata.name'

    # Images de todos os deployments
    kubectl get deploy -o json | \
      jq -r '.items[].spec.template.spec.containers[].image' | sort -u
    ```
  - YAML config → JSON pra usar com jq:
    ```bash
    yq -o json values.yaml | jq '.global.image'
    ```
  - Error handling em script:
    ```bash
    set -euo pipefail
    api_response=$(curl -sf https://api.example.com/v1/users)
    user_id=$(echo "$api_response" | jq -re '.users[0].id') || {
      echo "ERR: no users found" >&2; exit 1;
    }
    ```
- Armadilhas: `set -o pipefail` essencial em pipes (sem ele, `curl_fail | jq` retorna sucesso); `jq -e` retorna exit ≠ 0 quando filtro retorna `null`/`false`/vazio (útil mas surpreende); `kubectl -o json` vs `-o yaml` muda parser downstream (jq exige JSON; yq aceita YAML); xargs sem `-r` em lista vazia gera comando vazio (executa `cmd` sem args = comportamento indefinido); binary safety no preview fzf (jq emite JSON binário-safe mas piping pra cat sem `-A` pode quebrar terminal em raw bytes).
- Verbetes: pipefail, xargs -r.

## 6. Pesquisa por nota (âncoras)

Cada nota começa com **Step 1: Pesquisa-âncora** — WebFetch em paralelo de docs oficiais. Lista de URLs canônicos por nota:

- **01 fzf:** https://github.com/junegunn/fzf, https://github.com/junegunn/fzf/blob/master/CHANGELOG.md, https://github.com/junegunn/fzf/wiki/examples
- **02 ripgrep + fd:** https://github.com/BurntSushi/ripgrep, https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md, https://github.com/sharkdp/fd, https://github.com/sharkdp/fd#how-to-use
- **03 bat:** https://github.com/sharkdp/bat, https://github.com/sharkdp/bat#customization
- **04 eza:** https://github.com/eza-community/eza, https://github.com/eza-community/eza/blob/main/man/eza.1.md, https://the.exa.website/ (legado, contexto)
- **05 zoxide:** https://github.com/ajeetdsouza/zoxide, https://github.com/ajeetdsouza/zoxide/wiki
- **06 atuin:** https://docs.atuin.sh/, https://github.com/atuinsh/atuin
- **07 jq:** https://jqlang.github.io/jq/manual/, https://jqlang.github.io/jq/tutorial/
- **08 yq:** https://mikefarah.gitbook.io/yq/ (Go), https://github.com/kislyuk/yq (Python), https://kislyuk.github.io/yq/
- **09 tldr + cheat:** https://tldr.sh/, https://github.com/tldr-pages/tldr, https://github.com/cheat/cheat
- **10 delta:** https://github.com/dandavison/delta, https://dandavison.github.io/delta/
- **11 monitores:** https://github.com/aristocratos/btop, https://htop.dev/, https://github.com/bootandy/dust
- **12 stack interativo:** docs já fetched (fzf + zoxide + atuin), focar em compose patterns
- **13 pipeline:** jq manual + yq manual (já fetched) + https://kubernetes.io/docs/reference/kubectl/jsonpath/ (referência cruzada com jq)

## 7. Plano de execução (preview — detalhado no execution.md)

**Pré-flight (Task 0):** capturar versões de `fzf`, `rg`, `bat`, `eza`, `zoxide`, `atuin`, `jq`, `yq`, `tldr`, `cheat`, `delta`, `dust`, `btop`, `htop`, `fd`. Capturar info OS (`uname`, `lsb_release` se disponível). WebFetch das docs (paralelo) pra construir whitelist de flags.

**Esqueletos (Tasks 1-2):**
- Task 1: `CLI Utils/index.md` (MOC com 13 placeholders + tabela de substituições + "Veja também")
- Task 2: Bloco `## CLI Utils` vazio no Dicionário (header + nota interna de "preencher conforme notas")

**Notas (Tasks 3-15):** uma task por nota, ordem fase-progressiva (01 → 13). Cada task:
- Implementer subagent (Sonnet) com spec embedado completo + restrições
- Reviewer combinado (Sonnet): nota + verbetes adicionados ao Dicionário num único subagent
- Fix subagent (Sonnet) se Critical/Important; Nits ficam pra pass final

**Passes finais (Tasks 16-19):**
- Task 16: Pass final MOC (versões reais; wikilinks resolvem; títulos batem)
- Task 17: Pass final Dicionário (alfabético; sem duplicatas com outros blocos; "Veja também" em todos)
- Task 18: Tronco wikilink ativo (`Terminal/index.md`)
- Task 19: Validação `verificar-wikilinks` (0 broken) + cross-task review subagent dispatcher (consistência, code fences, armadilhas em bold-label, duplicação 12↔13 vs notas individuais)

**Ordem sequencial** (não-paralela) pras 13 notas pq todas modificam `Dicionário do Terminal.md` adicionando verbetes — paralelismo geraria race condition.

## 8. Critério de pronto

- **14 arquivos** em `03-Dominios/Tecnologia/Terminal/CLI Utils/`: 13 notas + `index.md` (MOC)
- **~40 verbetes novos** no bloco `## CLI Utils` do Dicionário (largamente acima do mínimo de 15)
- **Tronco** `Terminal/index.md` com wikilink ativo pro galho 6
- **`verificar-wikilinks`** em `CLI Utils/` sem broken links (`--respect-public-only`)
- **Quartz build** limpo (cross-repo — fora do escopo de validação direta, mas commits não devem quebrar)
- **Todos commits sem `Co-Authored-By: Claude`**
- Cada nota com **≥5 armadilhas** (formato bold-label, NÃO callouts), **≥7 wikilinks**, "Em inglês" em **bullets bilíngues** (NÃO tabela)
- Cada verbete novo com **"Veja também"** apontando pra nota canônica
- **Cross-task review** passou sem Critical/Important

## 9. Risco e mitigação

- **Confusão das duas yq (Go vs Python):** alta probabilidade de copiar exemplo da web da impl errada e empacar. **Mitigação:** nota 08 inteira girada em torno da diferença; armadilha #1 dedicada a "detectar qual versão"; tabela comparativa lado-a-lado.
- **Fabricação de uso pessoal:** user em adoção zero das 14 ferramentas; tentação de afirmar "no meu setup X..." é alta. **Mitigação:** reforço em cada implementer prompt + exemplos sempre neutros (`alice`, `myproj`) ou hipotéticos explícitos.
- **Armadilhas em callouts em vez de bold-label** (problema recorrente — apareceu na nota 03 do galho 5): **Mitigação:** prompt do implementer cita explicitamente "NUNCA callouts Obsidian em armadilhas; SEMPRE `### (N) Título` + 4 labels `**Causa:**`, `**Sintoma:**`, `**Como detectar:**`, `**Solução:**`". Reviewer combinado checa explicitamente.
- **Code fences não fechadas** (problema na nota 05 do galho 5): **Mitigação:** reviewer combinado checa explicitamente; cross-task review faz pass final.
- **Comandos com flags inventadas:** Rust crates moderns têm muitas flags; risco de inventar. **Mitigação:** Task 0 fetcheia docs oficiais; implementer prompt exige citação de doc oficial pra cada flag não-trivial.
- **Notas 12 e 13 duplicando conteúdo das notas individuais:** capstone tende a re-explicar tudo. **Mitigação:** prompt de 12 e 13 enfatiza "assume leitura de notas individuais; foque em **composição**, não re-explicação"; cross-task review checa.
- **`git add -A` acidental:** working tree já tem mudanças não-relacionadas em `Dicionário do Terminal.md` e `Multiplexer/01 - Zellij vs tmux vs screen.md`. **Mitigação:** restrição absoluta em todos os prompts de subagent + `git add <path>` nominal explícito.
- **Versões hardcoded envelhecendo:** ferramentas mudam rápido (fzf, atuin, eza). **Mitigação:** versões hedged ("0.4x+; verifique localmente") em vez de pins; MOC tem bloco "Versões assumidas" preenchido no pré-flight.
- **Comparações tendenciosas (rg vs grep, eza vs ls):** tendência de favorecer o moderno. **Mitigação:** cada comparação lista "quando esta vence" E "quando a clássica vence" (ex: `grep` em scripts portáveis POSIX; `ls` em CI sem cores).
- **dust e .gitignore:** desconhecido se versão atual respeita. **Mitigação:** Task 0 verifica via doc/teste; armadilha ajustada conforme realidade.
