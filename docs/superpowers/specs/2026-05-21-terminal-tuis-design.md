---
title: "Spec — Galho 4 da trilha Terminal (TUIs de Dev / Lazygit + Lazydocker)"
date: 2026-05-21
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 4 da trilha Terminal (TUIs de Dev / Lazygit + Lazydocker)

## 1. Contexto e motivação

Este é o **quarto galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`; galhos 1-3 já entregues). Pressupõe leitura do roadmap — tríade Iniciado/Adepto/Magus, tronco/galho e iteração vertical não são repetidos.

O usuário está em **adoção em curso** de ambas as ferramentas. Já instalou Lazygit e Lazydocker mas ainda não rodou em workflow diário com elas — não configurou `config.yml` custom, não escreveu `customCommands`, não usou `bisect` via UI. Os exemplos das notas devem ser um mix: neutros (`alice`, `myproj`) ou hipotéticos explícitos (`# hipotético: ...`) pra coisas que ele ainda não testou, e ancorados em situações que ele vai começar a fazer com base nas próprias notas. Sem fabricação de uso pessoal — se um caso de uso não foi vivido, escrever em terceira pessoa ou hipotético.

Lazygit e Lazydocker são TUIs do mesmo autor (Jesse Duffield) com filosofia semelhante: keyboard-first, painéis discoverable, integração nativa com docker-compose / git workflow. Por estarem no mesmo galho — mesmo o conteúdo sendo independente — 7 notas atendem (5 Lazygit + 2 Lazydocker), com proporção 2 Iniciado / 3 Adepto / 2 Magus. Lazygit ganha mais notas porque tem mais features estabelecidas e customização mais profunda (`customCommands`, `keybinding`, `gui.theme`, `git.paging`).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **7 notas atômicas + 1 MOC do galho + expansão do Dicionário do Terminal** em `03-Dominios/Terminal/TUIs/` e `03-Dominios/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (2 Iniciado + 3 Adepto + 2 Magus).

A trilha precisa ser:

- **Operacional** — leitor consegue rodar Lazygit e Lazydocker confiantemente após Iniciado; configurar e customizar após Adepto; estender com `customCommands` e debug docker-compose após Magus.
- **Honesta** — keybindings testados, configs verificáveis. Sem invenção de comandos ou features. Custom commands citados devem ser sintaxe válida no `config.yml` atual.
- **Atômica** — cada nota cobre um tópico bem-delimitado; wikilinks ricos pro restante do galho e pro Dicionário.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Terminal/TUIs/`)

Pasta nova, flat. 7 notas + 1 MOC:

#### Iniciado (2 notas)

| # | Nota |
|---|------|
| 01 | Lazygit — overview e operações essenciais |
| 02 | Lazydocker — overview e operações comuns |

#### Adepto (3 notas)

| # | Nota |
|---|------|
| 03 | Lazygit — operações intermediárias (rebase, cherry-pick, hunks) |
| 04 | Lazygit — config e customização (`config.yml`) |
| 05 | Lazydocker — config, customização e workflow |

#### Magus (2 notas)

| # | Nota |
|---|------|
| 06 | Lazygit — operações avançadas (bisect, custom commands, hooks) |
| 07 | Lazydocker — debugging avançado e docker-compose |

### 3.2. MOC do galho

`03-Dominios/Terminal/TUIs/index.md`:
- `type: moc`, `status: growing`, `progresso: andamento`
- Frontmatter padrão (`title: "TUIs de Dev"`, tags `terminal/tuis/lazygit/lazydocker/moc`, aliases `TUIs de Dev`/`Lazygit`/`Lazydocker`)
- Conteúdo agrupado em 3 H3 (Iniciado/Adepto/Magus)
- 2-3 rotas alternativas:
  - **Apenas Lazygit**: 01 → 03 → 04 → 06
  - **Apenas Lazydocker**: 02 → 05 → 07
  - **Onboarding completo**: 01 → 02 → 03 → 05 → 06
- Bloco "Versões assumidas" com Lazygit e Lazydocker versions capturadas no pré-flight

### 3.3. Expansão do Dicionário do Terminal

`03-Dominios/Terminal/Dicionário do Terminal.md` ganha **novo bloco** `## TUIs de Dev / Lazygit / Lazydocker` (após `## Multiplexer / Zellij`), com 14 verbetes em ordem alfabética case-insensitive:

| Verbete | Resumo |
|---|---|
| Bisect (Lazygit) | UI visual do `git bisect` no Lazygit |
| Cherry-pick | Copiar commit de branch A pra branch B |
| Command log | Painel do Lazygit que mostra cada comando git executado |
| Custom command (Lazygit) | Atalho YAML mapeando key → shell command com prompts |
| Docker-compose | Orquestrador multi-container Docker |
| Editor preset | Preset YAML do Lazygit pra abrir arquivo no editor configurado |
| Exec (Lazydocker) | Abrir shell interativo dentro de container rodando |
| Hunk | Bloco contíguo de mudanças num diff |
| Interactive rebase | `git rebase -i` com UI Lazygit (reorder/squash/edit/drop) |
| Lazydocker | TUI pra Docker (containers, images, logs, stats) |
| Lazygit | TUI pra git (status, branches, commits, stash) |
| Reflog | Log de movimentos de HEAD (visualizado com `Y` no Lazygit) |
| TUI | Terminal User Interface (UI keyboard-first dentro do terminal) |
| Worktree | Múltiplos working dirs do mesmo repo |

Cada verbete tem `Veja também:` apontando pra nota canônica do tópico.

### 3.4. Tronco — ativar wikilink

`03-Dominios/Terminal/index.md`: trocar `- TUIs de Dev — galho 4 (planejado): Lazygit, Lazydocker` por `- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev]] — galho 4: Lazygit + Lazydocker (operações, config, debugging)`.

## 4. Convenções por nota

Mesmo padrão consolidado nos galhos 2 e 3:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - terminal
  - tuis
  - lazygit | lazydocker
  - <fase>
  - <tags específicas>
aliases:
  - <aliases>
---
```

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout)
- `## O que é / Como funciona` — H3s conforme necessário
- `## Na prática` — exemplos runnable, configs YAML
- `## Armadilhas` — **≥5**, cada uma com os 4 labels:
  - `**Causa:**`
  - `**Sintoma:**`
  - `**Como detectar:**`
  - `**Solução:**`
- `## Em inglês` — bullets bilíngues `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
- `## Veja também` — wikilinks SEM backticks; inclui sempre:
  - Notas relacionadas do galho
  - `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - Wikilinks pros verbetes do Dicionário usados na nota
- `## Referências` — docs oficiais Lazygit/Lazydocker + posts canônicos

### 4.3. Restrições absolutas

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos. NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de keybindings/features. Cada keybinding e flag de config deve ser verificável via doc oficial.
3. **Sem `Co-Authored-By: Claude`**. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em "Veja também".
6. **Tronco wikilink obrigatório** em "Veja também".
7. **MOC wikilink** em "Veja também": `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`.
8. **Code fences corretos:** ` ```yaml ` pra config, ` ```bash ` pra shell, ` ```text ` ou ` ```diff ` pra exemplos de diff/hunk.
9. **Defaults documentados** — se comportamento é default na versão atual, mencionar.
10. **Custom commands com sintaxe válida** — verificar contra https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Command_Keybindings.md.
11. **Keybindings citados COM contexto** — Lazygit muda atalhos por painel (Files / Branches / Commits / Stash). Sempre indicar painel.

## 5. Conteúdo por nota (síntese)

### Iniciado

**01 — Lazygit: overview e operações essenciais**
- Quem é Lazygit (Jesse Duffield, Go, TUI keyboard-first pra git)
- Layout dos painéis: Status / Files / Local branches / Commits / Stash / Diff / Command log
- Navegação Vim-like entre painéis (h/l ou tab, j/k dentro do painel)
- Operações diárias por painel: `space` (stage hunk/file), `c` (commit), `a` (amend), `p`/`P` (pull/push), `b` (branch ops), `s` (stash), `d` (delete)
- `?` mostra help contextual
- Quando Lazygit ganha: muitos commits parciais (hunks), branch switching frequente, stash heavy, viz de history
- Quando `git` CLI ainda ganha: scripts, automações, contextos remotos sem TTY
- Quando IDE GUI ainda ganha: blame inline em código, integration com PR review na própria UI

**02 — Lazydocker: overview e operações comuns**
- Quem é Lazydocker (mesmo autor, mesma filosofia)
- Layout: Project (top), Containers / Images / Volumes / Networks (left), Main / Logs / Stats (right)
- Operações: `space` (start/stop/restart conforme contexto), `d` (remove), `r` (restart), `e` (exec /bin/sh), `l` (logs full screen), `R` (remove with volumes)
- Dashboard ao vivo: CPU/mem por container (Stats tab)
- Quando Lazydocker ganha: dev local com docker-compose, debug crash loop, tail logs cross-container
- Quando `docker` CLI ainda ganha: scripts CI/CD, automação, scripting de containers
- Quando portainer/portainer-like ainda ganha: equipe não-dev, gerenciamento remoto multi-host

### Adepto

**03 — Lazygit: operações intermediárias (rebase, cherry-pick, hunks)**
- **Rebase interativo:** painel Commits, `e` (edit/interactive) em commit → tela de rebase → reorder com `K`/`J`, squash com `s`, fixup com `f`, drop com `d`, edit com `e`. Continue com `m` (after fix).
- **Cherry-pick:** `c` (copy) em commit (modo COPY) → ir pra branch destino → `v` (paste).
- **Staging por hunks:** `enter` no diff view de Files → entra no diff inline view → `space` stage linha individual; `tab` alterna entre +/- contextos. `enter` mais profundo na linha.
- **Discard:** `d` em arquivo Modified → menu (Discard all / Discard changes), confirmation.
- **Reflog:** `Y` em qualquer painel → painel Reflog (todas movimentações de HEAD). Útil pra recuperar branch deletada.
- **Merge conflicts:** após merge/rebase, Lazygit mostra arquivos em conflict; `enter` no arquivo abre conflict view com `space` pra escolher hunk.

**04 — Lazygit: config e customização (`config.yml`)**
- Local: `~/.config/lazygit/config.yml` (XDG_CONFIG_HOME)
- Seções principais:
  - `gui:` — theme (background, lightTheme, theme.activeBorderColor, etc.), showFileTree, scrollOffMargin
  - `git:` — paging.colorArg, paging.useConfig, log.order, log.showWholeGraph
  - `os:` — editPreset (`nvim`, `vscode`, `helix`, etc.) ou edit/editAtLine custom
  - `keybinding:` — rebind teclas (raro; defaults são bons)
  - `customCommands:` — introdução (cobertura profunda em nota 06)
- Theme custom: hex colors (em strings) e color names builtin
- `editPreset: "nvim"` integra com Neovim (galho 1) — abrir arquivo no Neovim atual ou novo
- Disable mouse, change icon set, statusBar visibility
- Versionar config no repo de dotfiles (symlink ou stow)

**05 — Lazydocker: config, customização e workflow**
- Local: `~/.config/lazydocker/config.yml`
- Seções principais:
  - `gui:` — theme
  - `commandTemplates:` — rebind `dockerCompose` (e.g. pra `podman-compose`), `runCustomCommand`
  - `customCommands:` — atalhos de teclado pra comandos shell custom
  - `logs.timestamps`, `logs.since`
- Auto-detect docker-compose: se há `docker-compose.yml` no cwd, agrupa services
- Workflow recomendado:
  - 1 pane Zellij rodando Lazydocker (sempre visível)
  - dev server num pane vizinho
  - Lazydocker pra restart container quando dep config muda
- Integração com `docker compose` v2 (espaço, não hífen) — verificar `commandTemplates` no config

### Magus

**06 — Lazygit: operações avançadas (bisect, custom commands, hooks)**
- **Bisect:** painel Commits, `b` (mark good/bad) → Lazygit dirige bisect (check out cada commit), você marca good/bad → identifica regressão.
- **Custom commands:** estrutura YAML completa:
  ```yaml
  customCommands:
    - key: "<C-r>"
      command: "git push --force-with-lease"
      context: "global"
      description: "Force-push with lease"
      prompts:
        - type: "confirm"
          title: "Force-push?"
  ```
  Exemplos verificáveis:
  - Fast PR creation via `gh pr create`
  - Conventional commit prefix prompt (`feat:`, `fix:`, etc.)
  - Force-push with lease (segurança)
  - Custom branch creation com prefixo de tipo (`feat/`, `fix/`)
- **Git hooks (não-Lazygit-specific):** Lazygit respeita pre-commit, commit-msg etc. Setup com pre-commit framework (https://pre-commit.com/). Lazygit NÃO tem hooks plugin-extensíveis próprios (verificar — Lazygit usa hooks git nativos).
- **Worktrees:** `w` em painel Branches abre worktree view; criar/remover. Útil pra trabalhar em 2+ branches simultaneamente sem stash.

**07 — Lazydocker: debugging avançado e docker-compose**
- **Stack docker-compose:** Lazydocker mostra services como grupo dentro de Project top. Dependências (`depends_on`), status agregado.
- **Inspect verboso:** `enter` em container → tab Config mostra env vars, ports, mounts, networks.
- **Logs filter:** Lazydocker logs tab — fast scroll, regex search (verificar atalho na versão atual), tail vs full output.
- **Exec custom:** atalho `e` (default `/bin/sh`); pra shell custom (e.g. `bash`, `zsh`) usar customCommand:
  ```yaml
  customCommands:
    containers:
      - name: "bash"
        attach: true
        command: "docker exec -it {{ .Container.ID }} bash"
  ```
- **Workflow debug crash loop:** notar container restart count crescendo → logs tab → identificar erro → fix → restart.
- **Health checks:** Lazydocker mostra status do health check em coluna; container `unhealthy` é alertado visualmente.
- **Compose overrides:** Lazydocker carrega `docker-compose.yml` + `docker-compose.override.yml` automaticamente conforme `docker compose` faz.

## 6. Pesquisa por nota (âncoras)

Cada nota começa com **Step 1: Pesquisa-âncora** — WebFetch em paralelo de docs canônicas.

- **Todas:** README oficial + docs do repo. URLs canônicas:
  - Lazygit: https://github.com/jesseduffield/lazygit (README + `/docs/` folder)
  - Lazydocker: https://github.com/jesseduffield/lazydocker (README + `/docs/`)
- **04:** https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md
- **05:** https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
- **06:** https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Command_Keybindings.md, https://pre-commit.com/
- **07:** https://docs.docker.com/compose/

## 7. Plano de execução (preview — detalhado no execution.md)

**Pré-flight (Task 0):** capturar `lazygit --version`, `lazydocker --version`, paths de config.

**Esqueletos (Tasks 1-2):**
- Task 1: `TUIs/index.md` (MOC com placeholders)
- Task 2: Bloco `## TUIs de Dev / Lazygit / Lazydocker` vazio no Dicionário

**Notas (Tasks 3-9):** uma task por nota, ordem fase-progressiva. Cada task:
- Implementer subagent (Sonnet) com spec completo + restrições
- Reviewer combinado (Sonnet)
- Fix subagent (Sonnet) se Critical/Important
- Mark complete

**Passes finais (Tasks 10-13):**
- Task 10: Pass final MOC (versões reais)
- Task 11: Pass final Dicionário (alfabético + Veja também)
- Task 12: Tronco wikilink
- Task 13: Validação final (`verificar-wikilinks`)

## 8. Critério de pronto

- 8 arquivos em `03-Dominios/Terminal/TUIs/`: 7 notas + `index.md`
- ≥12 verbetes novos no bloco `## TUIs de Dev / Lazygit / Lazydocker` do Dicionário
- Tronco `Terminal/index.md` com wikilink ativo
- `verificar-wikilinks` em `TUIs/` sem broken links
- Quartz build limpo (cross-repo — fora do escopo desta sessão)
- Todos commits sem `Co-Authored-By: Claude`
- Cada nota com ≥5 armadilhas (4 labels), ≥7 wikilinks, "Em inglês" em bullets bilíngues
- Cada verbete com "Veja também"

## 9. Risco e mitigação

- **Keybindings mudam entre versões:** Lazygit/Lazydocker evoluem ativamente; atalhos podem ter sido refeitos. **Mitigação:** Step 1 (pesquisa-âncora) de cada nota verifica keybindings via doc oficial mais recente; quando ambíguo, escrever "verifique `?` na sua versão".
- **Custom commands sintaxe muda:** schema YAML pode evoluir (campos novos como `loadingText`, `output`). **Mitigação:** verificar contra `docs/Custom_Command_Keybindings.md` antes de cada exemplo; preferir exemplos minimal.
- **`docker compose` v1 (hífen) vs v2 (espaço):** muitos sistemas ainda têm v1. **Mitigação:** mencionar ambos; documentar `commandTemplates` pra rebind se necessário.
- **Fabricação de uso pessoal:** ambos em adoção; tentação de afirmar "no meu workflow X..." é alta. **Mitigação:** reforço nos prompts de cada implementer subagent.
- **Lazygit hooks "Lazygit-specific" não existem:** o usuário pode esperar plugin system; Lazygit só respeita git hooks nativos. **Mitigação:** Magus 06 documenta explicitamente "Lazygit não tem hooks próprios extensíveis; usa git hooks nativos".
