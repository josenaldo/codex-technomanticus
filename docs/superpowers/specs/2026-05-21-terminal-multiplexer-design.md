---
title: "Spec — Galho 3 da trilha Terminal (Multiplexer / Zellij)"
date: 2026-05-21
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 3 da trilha Terminal (Multiplexer / Zellij)

## 1. Contexto e motivação

Este é o **terceiro galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`; galhos 1 e 2 já entregues). Pressupõe leitura do roadmap — a tríade Iniciado/Adepto/Magus, a estrutura tronco/galho e a iteração vertical por galho não são repetidas aqui.

O usuário está em **adoção em curso** do Zellij como multiplexer. Já instalou, conhece o básico, mas ainda não rodou sessions persistentes em workflow diário, não escreveu layout KDL próprio, nem mexeu em plugins. Os exemplos das notas devem ser um mix: neutros (ou hipotéticos explícitos) pra coisas que ele ainda não testou, e ancorados em situações que ele vai começar a fazer com base nas próprias notas. Sem fabricação de uso pessoal — se um caso de uso não foi vivido, escrever em terceira pessoa ou hipoteticamente.

Zellij é mais enxuto que o stack Zsh+OMZ+P10k do galho 2: uma única ferramenta, com modelo mental claro (server → sessions → tabs → panes), modos discoverable e config em KDL. Por isso 7 notas são suficientes (vs 10 do galho 2), com proporção 3 Iniciado / 2 Adepto / 2 Magus.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **7 notas atômicas + 1 MOC do galho + expansão do Dicionário do Terminal** em `03-Dominios/Tecnologia/Terminal/Multiplexer/` e `03-Dominios/Tecnologia/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (3 Iniciado + 2 Adepto + 2 Magus).

A trilha precisa ser:

- **Operacional** — leitor consegue rodar Zellij confiantemente após Iniciado; configurar layouts e sessions após Adepto; estender com plugins e integrar com Neovim após Magus.
- **Honesta** — exemplos verificados (commands rodam, plugins existem, sintaxe KDL é validada). Sem fabricação de uso pessoal nem invenção de plugins/funcionalidades.
- **Atômica** — cada nota cobre um tópico bem-delimitado, com wikilinks ricos pro restante do galho e pro Dicionário.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Terminal/Multiplexer/`)

Pasta nova, flat. 7 notas + 1 MOC:

#### Iniciado (3 notas — usar Zellij no dia-a-dia)

| # | Nota |
|---|------|
| 01 | Zellij vs tmux vs screen — por que Zellij |
| 02 | Modelo mental — sessions, tabs, panes |
| 03 | Modos básicos e keybindings essenciais |

#### Adepto (2 notas — dominar uso operacional)

| # | Nota |
|---|------|
| 04 | Sessões persistentes — detach, attach, gerenciamento |
| 05 | Layouts declarativos em KDL |

#### Magus (2 notas — maestria e integração)

| # | Nota |
|---|------|
| 06 | Modos avançados, plugins e copy-mode |
| 07 | Integração com Neovim e shell |

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Terminal/Multiplexer/index.md`:
- `type: moc`, `status: growing`, `progresso: andamento`
- Frontmatter padrão (`title: "Multiplexer"`, tags `terminal/multiplexer/zellij/moc`, aliases `Multiplexer`/`Zellij`)
- Conteúdo agrupado em 3 H3 (Iniciado/Adepto/Magus)
- 2-3 rotas alternativas (e.g. "Daily-driver" = 01→02→03→04; "Config-first" = 02→05→04; "Maestria" = 03→04→05→06→07)
- Bloco "Versões assumidas" com Zellij version capturada no pré-flight

### 3.3. Expansão do Dicionário do Terminal

`03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` ganha **novo bloco** `## Multiplexer / Zellij` (após `## Shell / Zsh / OMZ`), com 16 verbetes em ordem alfabética case-insensitive:

| Verbete | Resumo |
|---|---|
| Attach | Reconectar a sessão Zellij em background |
| Detach | Desconectar da sessão sem matar |
| Floating pane | Pane sobreposto (não ocupa grid) |
| KDL | Linguagem declarativa (Cuddly Document Language) |
| Layout (Zellij) | Definição declarativa de tabs/panes/splits em KDL |
| Locked mode | Modo que desliga keybindings do Zellij (passthrough) |
| Mode (Zellij) | Estado modal (normal, pane, tab, resize, scroll, search, session, move, locked) |
| Multiplexer | Programa que divide 1 terminal em múltiplas sessions/panes (genérico) |
| Pane | Divisão interna de uma tab |
| Pipe API | Interface WASM Zellij ↔ plugin pra comunicação assíncrona |
| Plugin (Zellij) | Módulo WASM que estende Zellij |
| Session (Zellij) | Instância nomeada, sobrevive a detach |
| Stacked pane | Modo de empilhamento (1 expandido + outros minimizados) |
| Status bar | Barra de info (modo, tabs, atalhos) — implementada por plugin |
| Tab (Zellij) | Agrupamento horizontal de panes dentro de uma session |
| Tmux compat mode | Modo de keybindings que emula prefixo tmux (`Ctrl-b`) |

Cada verbete tem `Veja também:` apontando pra nota canônica do tópico.

### 3.4. Tronco — ativar wikilink

`03-Dominios/Tecnologia/Terminal/index.md`: trocar `- Multiplexer — galho 3 (planejado): Zellij` por `- [[03-Dominios/Tecnologia/Terminal/Multiplexer/index|Multiplexer]] — galho 3: Zellij (sessions, layouts KDL, plugins WASM)`.

## 4. Convenções por nota

Mesmo padrão consolidado no galho 2:

### 4.1. Frontmatter

```yaml
---
title: "<título da nota>"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - terminal
  - multiplexer
  - zellij
  - <fase>
  - <tags específicas>
aliases:
  - <aliases>
---
```

### 4.2. Estrutura H2 obrigatória

- `## TL;DR` — 2-4 frases que entregam o conceito
- `## O que é / Como funciona` — modelo + mecanismo (com H3s quando faz sentido)
- `## Na prática` — exemplos runnable, configs, snippets
- `## Armadilhas` — **≥5**, cada uma com os 4 labels:
  - `**Causa:**`
  - `**Sintoma:**`
  - `**Como detectar:**`
  - `**Solução:**`
- `## Em inglês` — bullets `- **PT** — *EN*. "frase técnica curta."` (8-10 termos). **NUNCA tabela.**
- `## Veja também` — wikilinks **sem backticks**; inclui sempre:
  - Notas relacionadas do mesmo galho
  - `[[03-Dominios/Tecnologia/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]`
  - Wikilinks pros verbetes do Dicionário usados na nota
- `## Referências` — docs oficiais Zellij + posts canônicos verificados

### 4.3. Restrições absolutas

Carregadas do galho 2 e do CLAUDE.md/memórias:

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `user`, `myproj`) ou hipotéticos explícitos (`# hipotético: ...`). NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de plugins/funções/repos. Cada plugin Zellij citado por nome deve ser verificado (existe, URL canônica). Casos passados que vazaram no galho 2: `_omz_completion` (não existe), `zsh-users/zsh-vim-mode` (repo não existe).
3. **Sem `Co-Authored-By: Claude`** em commits. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Isolamento público** — nenhum link/menção a apocrypha.
6. **Wikilinks sem backticks** em `## Veja também`.
7. **Tronco wikilink obrigatório** em toda `## Veja também`.
8. **Code fences corretos:** ` ```kdl ` pra KDL; ` ```bash ` pra comandos shell; ` ```zsh ` quando exclusivamente Zsh; ` ```lua ` pra config Neovim.
9. **Defaults documentados** — se um comportamento já é default em Zellij moderno, mencionar.
10. **Comandos verificáveis** — testar/conferir antes de claim.
11. **Plugins citados** — mínimo 2, máximo 3 em Magus 06, com URL do repo e status (ativo/manutenção).

## 5. Conteúdo por nota (síntese)

### Iniciado

**01 — Zellij vs tmux vs screen — por que Zellij**
- Diferenciais: modos discoverable (status bar mostra atalhos), layouts em KDL, plugin system WASM, defaults sensatos (mouse on, copy-on-select).
- Quando tmux ainda ganha: universalidade (instalado em qualquer servidor), ecossistema maduro, performance.
- Tabela comparativa (3 colunas): Zellij / tmux / screen → linhas em discoverabilidade, config, sessions, plugins, performance, comunidade.
- Quem é o público de cada.

**02 — Modelo mental: sessions, tabs, panes**
- Hierarquia: 1 Zellij server → N sessions → N tabs → N panes (+ floating panes paralelos).
- Diagrama ASCII da hierarquia.
- Cada nível: como é criado, como sobrevive a detach, lifecycle.
- Diferença entre "minimizar" (suspended) e "fechar".
- Floating panes vs stacked panes vs split panes.

**03 — Modos básicos e keybindings essenciais**
- 9 modos: normal, locked, pane, tab, resize, scroll, search, session, move — overview com proposito de cada.
- Aprofundar normal, pane, tab (Iniciado).
- Cheatsheet das ~20 primeiras keybindings que valem a pena memorizar.
- Como descobrir keybinding sem decorar (status bar mostra).

### Adepto

**04 — Sessões persistentes — detach, attach, gerenciamento**
- `zellij` cria/anexa default; `-s <nome>` nomeia.
- `zellij attach <nome>`, `zellij attach --create <nome>` (idempotente).
- `zellij list-sessions` — formato + status (current, exited).
- `zellij delete-session <nome>`, `zellij delete-all-sessions`, `--force`.
- `zellij kill-session <nome>` (mata mas mantém histórico).
- Sessões mortas vs ativas — cleanup periódico.
- Workflow: 1 session por projeto.

**05 — Layouts declarativos em KDL**
- Sintaxe KDL básica: nós, propriedades, children, comentários.
- Estrutura de layout Zellij: `layout { tab { pane ... } }`.
- Propriedades: `size`, `split_direction`, `cwd`, `command`, `args`.
- Stacked panes via `pane stacked=true { pane; pane; pane }`.
- Floating panes via `floating_panes`.
- `default_layout` em `~/.config/zellij/config.kdl`.
- Layouts customizados em `~/.config/zellij/layouts/`, carregar com `zellij --layout <nome>`.
- Templates: dev (editor + shell + watcher), monitor (top + logs + journalctl).

### Magus

**06 — Modos avançados, plugins e copy-mode**
- Locked mode — quando ativar (apps com conflito de Ctrl-G/Ctrl-S como Emacs/Vim interno).
- Scroll mode + search mode — navegação no scrollback + busca regex.
- Tmux compat mode — `tmux_compatibility = true` no config; tradeoffs.
- Arquitetura de plugins WASM:
  - Wasmtime runtime
  - Pipe API (mensagens bidirecionais Zellij ↔ plugin)
  - Permissões (`permissions`, capability-based)
  - Lifecycle (`load`, `update`, `render`)
- 2-3 plugins concretos. Candidatos prováveis (sujeitos a verificação no Step 1 da nota — URL retorna 200, último commit recente, README ainda lista features citadas):
  - **zjstatus** (dj95/zjstatus) — status bar customizável
  - **room** (rvcas/room) ou similar — gerenciador de panes/tabs
  - **vim-zellij-navigator** (hiasr/vim-zellij-navigator) — mencionado brevemente aqui como exemplo de plugin; cobertura profunda fica pra nota 07
  - Se algum não passar verificação, substituir por outro com mesma categoria
- Configurar e debuggar plugin (`zellij action launch-plugin`).

**07 — Integração com Neovim e shell**
- Focus events: Zellij propaga focus pra Neovim (autocmd `FocusGained`/`FocusLost`).
- vim-zellij-navigator: Ctrl-h/j/k/l navega Neovim splits + Zellij panes com mesma keybinding (similar a vim-tmux-navigator).
- Status bar dinâmico: zjstatus mostrando branch git, modo Neovim, contexto.
- Shell integration: `zellij action write-chars` pra abrir comando em pane novo programaticamente.
- Send keys cross-pane via `zellij action send-keys`.
- Pre-detach hooks pra salvar estado.

## 6. Pesquisa por nota (âncoras)

Cada nota começa com **Step 1: Pesquisa-âncora** — WebFetch em paralelo de docs canônicas, capturar exemplos e sintaxe antes de escrever.

- **Todas:** https://zellij.dev/documentation/
- **01:** https://zellij.dev/about/, https://github.com/tmux/tmux. Posts comparativos opcionais — só citar se forem canônicos e verificáveis; preferir docs oficiais como base.
- **02:** https://zellij.dev/documentation/sessions, https://zellij.dev/documentation/panes
- **03:** https://zellij.dev/documentation/keybindings
- **04:** https://zellij.dev/documentation/commands
- **05:** https://zellij.dev/documentation/layouts, https://kdl.dev/
- **06:** https://zellij.dev/documentation/plugins, https://github.com/zellij-org/zellij/tree/main/zellij-utils/assets/plugins, plugin repos verificados
- **07:** https://zellij.dev/news/version-0.40.0, https://github.com/hiasr/vim-zellij-navigator

## 7. Plano de execução (preview — detalhado no execution.md)

**Pré-flight (Task 0):** capturar `zellij --version`, paths de config (`~/.config/zellij/`), plugins instalados se houver.

**Esqueletos (Tasks 1-2):**
- Task 1: `Multiplexer/index.md` (MOC com placeholders de versão)
- Task 2: Bloco `## Multiplexer / Zellij` vazio (apenas header) no Dicionário, antes do bloco final ou após Shell/Zsh/OMZ

**Notas (Tasks 3-9):** uma task por nota, em ordem fase-progressiva (3-5 Iniciado, 6-7 Adepto, 8-9 Magus). Cada task:
- Implementer subagent (Sonnet) com spec completo da nota + restrições absolutas + lista das armadilhas mínimas
- Reviewer combinado (Sonnet) — spec compliance + code/conteúdo quality
- Fix subagent (Sonnet) se Critical/Important encontrado
- Mark complete

**Passes finais (Tasks 10-13):**
- Task 10: Pass final MOC — substituir placeholders por versões reais
- Task 11: Pass final Dicionário — alfabético case-insensitive + "Veja também" em cada verbete
- Task 12: Tronco — Edit em `Terminal/index.md` ativando wikilink
- Task 13: Validação final — `verificar-wikilinks` em `Multiplexer/`, sanity check geral

## 8. Critério de pronto

- 8 arquivos em `03-Dominios/Tecnologia/Terminal/Multiplexer/`: 7 notas + `index.md`
- ≥15 verbetes novos no bloco `## Multiplexer / Zellij` do Dicionário
- Tronco `Terminal/index.md` com wikilink ativo pro Multiplexer
- `verificar-wikilinks` em `Multiplexer/` sem broken links
- Quartz build limpo (verificação cross-repo — fora do escopo desta sessão; usuário roda separado)
- Todos commits sem `Co-Authored-By: Claude`
- Cada nota com ≥5 armadilhas, 4 labels cada; ≥8 wikilinks; "Em inglês" em bullets
- Cada verbete com "Veja também"

## 9. Risco e mitigação

- **Plugins WASM instáveis:** plugins citados em Magus 06 podem ter API mudada ou ter sido descontinuados. Mitigação: Step 1 da nota 06 verifica cada plugin (URL retorna 200, último commit recente, README ainda lista features citadas).
- **Sintaxe KDL pode evoluir:** Zellij usa versão específica do KDL. Mitigação: capturar versão Zellij no pré-flight; testar layouts em ambiente local antes de commitar.
- **Integrações dependem de versão:** vim-zellij-navigator e zjstatus mudam APIs. Mitigação: anclar referências em commits ou versões específicas se nota dá exemplo executável.
- **Fabricação de uso pessoal:** usuário está em adoção; tentação de afirmar "no meu workflow X..." é alta. Mitigação reforçada no prompt de cada implementer subagent.
