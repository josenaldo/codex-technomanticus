# Galho 3 — Multiplexer (Zellij) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar o galho 3 da trilha Terminal — 7 notas atômicas (3 Iniciado + 2 Adepto + 2 Magus) sobre Zellij em `03-Dominios/Terminal/Multiplexer/`, MOC do galho, expansão do Dicionário do Terminal com bloco `## Multiplexer / Zellij`, e ativação do wikilink no tronco.

**Architecture:** Mesmo padrão consolidado no galho 2 (Shell). Cada nota segue estrutura H2 fixa (TL;DR, O que é/Como funciona, Na prática, Armadilhas, Em inglês, Veja também, Referências). Fluxo SDD: implementer subagent → reviewer combinado → fix subagent quando houver issues Critical/Important. Pesquisa-âncora em docs oficiais Zellij antes de cada nota.

**Tech Stack:** Obsidian + Quartz (vault público), Markdown + frontmatter YAML, wikilinks. Ferramenta-alvo das notas: Zellij (terminal multiplexer, Rust + WASM plugins).

---

## Spec de referência

`docs/superpowers/specs/2026-05-21-terminal-multiplexer-design.md`

## Restrições absolutas (carregadas em todos os subagent prompts)

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `user`, `myproj`) ou hipotéticos explícitos (`# hipotético: ...`). NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de plugins/funções/repos. Cada plugin Zellij citado por nome deve ser verificado (URL retorna 200, README confirma features citadas).
3. **Sem `Co-Authored-By: Claude`** em commits. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em `## Veja também`.
6. **Tronco wikilink obrigatório** em toda `## Veja também`: `[[03-Dominios/Terminal/index|Trilha Terminal]]`.
7. **MOC wikilink** em toda `## Veja também`: `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`.
8. **≥5 armadilhas** por nota, cada uma com os 4 labels (`**Causa:**` / `**Sintoma:**` / `**Como detectar:**` / `**Solução:**`).
9. **"Em inglês" em bullets** `- **PT** — *EN*. "frase técnica curta."` com 8-10 termos. **NUNCA tabela.**
10. **Code fences corretos:** ` ```kdl ` pra KDL; ` ```bash ` pra comandos shell genéricos; ` ```zsh ` quando exclusivamente Zsh; ` ```lua ` pra config Neovim.
11. **Defaults documentados** — se um comportamento é default no Zellij atual, mencionar.
12. **Plugins citados** — mínimo 2, máximo 3 em Magus 06, com URL do repo e status (ativo/manutenção).

---

## Task 0: Pré-flight

**Files:**
- (nenhum — só captura de informações)

**Objetivo:** capturar versões reais que vão preencher o MOC no Task 10.

- [ ] **Step 1: Capturar versão Zellij**

```bash
zellij --version 2>&1 || echo "(zellij não instalado)"
```

Anotar resultado. Se não instalado, marcar e prosseguir — versões vão usar "0.40+" como placeholder com aviso, e os exemplos seguem doc oficial.

- [ ] **Step 2: Capturar paths de config**

```bash
ls -la ~/.config/zellij/ 2>&1 | head -20
test -f ~/.config/zellij/config.kdl && echo "config existe" || echo "config default (sem custom)"
ls -1 ~/.config/zellij/layouts/ 2>&1 | head -10
ls -1 ~/.config/zellij/plugins/ 2>&1 | head -10
```

Anotar o que existir.

- [ ] **Step 3: Anotar versões num scratch local**

Não commitar. Anotar mentalmente / num arquivo temp; será usado pelo controller no Task 10 ao preencher o MOC.

Exemplo (substitua pelos valores reais):

```
Zellij: 0.41.2
Config: ~/.config/zellij/ existe; sem config.kdl custom; sem layouts custom; sem plugins
```

---

## Task 1: MOC do galho Multiplexer — esqueleto

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/index.md`

**Objetivo:** criar o MOC do galho com placeholders pros 7 wikilinks de notas (que ainda não existem). Versões usam placeholders explícitos `<COMMIT_X>` / `<DATA_X>` resolvidos no Task 10.

- [ ] **Step 1: Criar pasta + arquivo**

```bash
mkdir -p "03-Dominios/Terminal/Multiplexer"
```

- [ ] **Step 2: Escrever MOC**

Use `Write` em `03-Dominios/Terminal/Multiplexer/index.md`:

```markdown
---
title: "Multiplexer"
type: moc
publish: true
created: 2026-05-21
updated: 2026-05-21
status: growing
progresso: andamento
tags:
  - terminal
  - multiplexer
  - zellij
  - moc
aliases:
  - Multiplexer
  - Zellij
---
# Multiplexer

> [!abstract] TL;DR
> Galho 3 da trilha Terminal. Domínio de Zellij como multiplexer primário, em 3 fases (3 + 2 + 2 = 7 notas): do "Zellij vs tmux" ao escrever layout KDL e estender com plugin WASM.

Esse galho cobre o multiplexer end-to-end: por que Zellij e quando tmux ainda ganha (Iniciado); modelo mental de sessions/tabs/panes; modos básicos e keybindings essenciais; sessões persistentes e layouts declarativos em KDL (Adepto); modos avançados, plugins WASM e integração com Neovim e shell (Magus).

## Conteúdo

### Iniciado

- [[01 - Zellij vs tmux vs screen]]
- [[02 - Modelo mental — sessions, tabs, panes]]
- [[03 - Modos básicos e keybindings essenciais]]

### Adepto

- [[04 - Sessões persistentes — detach, attach, gerenciamento]]
- [[05 - Layouts declarativos em KDL]]

### Magus

- [[06 - Modos avançados, plugins e copy-mode]]
- [[07 - Integração com Neovim e shell]]

## Rotas alternativas

- **Daily-driver enxuto** (Iniciado completa + sessions): `01` → `02` → `03` → `04`
- **Config-first** (saltar pra layouts cedo): `02` → `05` → `04`
- **Maestria** (motor + integração): `03` → `04` → `05` → `06` → `07`

## Versões assumidas

- **Zellij:** `<VERSAO_ZELLIJ>` (capturada no pré-flight)
- Plugins externos: versões `master` em 2026-05-21

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/index.md"
git commit -m "feat(terminal-multiplexer): MOC do galho 3 — esqueleto"
```

---

## Task 2: Dicionário — bloco "Multiplexer / Zellij" esqueleto

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md`

**Objetivo:** adicionar header `## Multiplexer / Zellij` (sem verbetes ainda) ao Dicionário, após o bloco `## Shell / Zsh / OMZ`. Verbetes individuais entram com cada nota.

- [ ] **Step 1: Localizar fim do bloco Shell/Zsh/OMZ**

Use `Read` em `03-Dominios/Terminal/Dicionário do Terminal.md` no final do arquivo (provavelmente após o verbete `### Zstyle`, último alfabético do bloco anterior).

- [ ] **Step 2: Inserir header**

Após o último verbete do bloco Shell/Zsh/OMZ (e antes do próximo `## ` se houver, ou no fim do arquivo), inserir:

```markdown
## Multiplexer / Zellij

```

Use `Edit` com `old_string` = última linha do bloco anterior + 1 linha vazia + (próxima seção ou EOF) e `new_string` = mesma coisa com `## Multiplexer / Zellij\n\n` inserido.

- [ ] **Step 3: Atualizar `updated:` do dicionário pra `2026-05-21`**

Se ainda não estiver `2026-05-21`, Edit do frontmatter.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): adiciona bloco 'Multiplexer / Zellij' ao Dicionário"
```

---

## Task 3: Nota 01 — Zellij vs tmux vs screen

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/01 - Zellij vs tmux vs screen.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: Multiplexer)

**Conteúdo-chave:** comparação Zellij vs tmux vs screen, diferenciais (modos discoverable, layouts KDL, plugin WASM, defaults sensatos), quando tmux ainda ganha, tabela comparativa, público-alvo.

- [ ] **Step 1: Pesquisa-âncora**

WebFetch em paralelo:
```
WebFetch: https://zellij.dev/about/
WebFetch: https://zellij.dev/documentation/
```

Capturar: lista de features oficial, defaults documentados, comparação com tmux do próprio Zellij about page.

- [ ] **Step 2: Criar frontmatter + esqueleto**

```yaml
---
title: "Zellij vs tmux vs screen"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - multiplexer
  - zellij
  - tmux
  - iniciado
aliases:
  - Zellij vs tmux
---
```

- [ ] **Step 3: Escrever a nota completa**

Estrutura H2 obrigatória (TL;DR, O que é / Como funciona, Na prática, Armadilhas, Em inglês, Veja também, Referências).

**Cobrir:**

- **TL;DR:** "Multiplexer divide 1 terminal em múltiplas sessions/panes que sobrevivem a detach. Zellij é o novo (2020+), com modos discoverable (status bar mostra atalhos) e config declarativa em KDL. tmux é o padrão (universal em servidores, ecossistema maduro). screen é o legado (sempre instalado, baixo nível). Zellij vence pra workstation de dev; tmux vence pra servidor remoto."

- **O que é / Como funciona:**

  ### Multiplexer — o conceito
  - Programa que roda como server e cria múltiplas "sessões" (cada uma com tabs/panes).
  - Você anexa (`attach`) e desanexa (`detach`) — o server segue rodando, comandos seguem executando.
  - Diferente de "abrir várias abas do terminal" — sobrevive a fechar o emulador, SSH drop, reboot do tmux server.

  ### Os 3 concorrentes
  Tabela comparativa (Zellij | tmux | screen) com colunas pra:
  - **Discoverabilidade** — status bar mostra atalhos (Zellij sim, tmux não, screen não)
  - **Config** — KDL declarativo / .tmux.conf imperativo / .screenrc imperativo
  - **Sessions persistentes** — todos têm
  - **Plugins** — WASM (Zellij) / TPM/scripts shell (tmux) / nenhum (screen)
  - **Performance** — Zellij ~ tmux > screen (geralmente)
  - **Ubiquidade em servidores** — screen >> tmux > Zellij
  - **Versão atual** — citar versões aproximadas verificáveis
  - **Maturidade** — screen (1987), tmux (2007), Zellij (2020)

  ### Diferenciais do Zellij
  - Status bar com hints de modo
  - Modos discoverable (você não precisa decorar `Ctrl-b ?`)
  - Defaults sensatos (mouse on, copy-on-select, status visível)
  - Layouts em KDL — declarativo, versionável
  - Plugin system em WASM (sandbox, multilang)
  - "tmux mode" opcional pra quem quer keybindings familiares

  ### Quando tmux ainda ganha
  - **Servidores remotos:** quase sempre tem tmux; raramente tem Zellij. Aprender 1 ferramenta universal > 2 contextuais.
  - **Ecossistema:** TPM tem centenas de plugins; ecossistema Zellij é menor.
  - **Performance em sessões enormes:** tmux tem 18 anos de otimização.
  - **Documentação madura:** mais blog posts, stack overflow, dotfiles.

  ### Público-alvo de cada
  - Zellij: workstation dev local, dotfiles modernos, quem prefere discoverability sobre minimalismo.
  - tmux: tudo (default seguro).
  - screen: sysadmin, servidores embedded, situações onde só tem screen.

- **Na prática:**

  ### Instalação rápida (Linux)
  ```bash
  # Zellij — arquivo binário do GitHub releases
  curl -L https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-unknown-linux-musl.tar.gz | tar -xz
  sudo mv zellij /usr/local/bin/

  # ou via cargo
  cargo install --locked zellij
  ```

  ### Primeira sessão
  ```bash
  zellij               # cria/anexa default
  zellij -s myproj     # cria session nomeada
  zellij ls            # lista sessions
  ```

  ### Side-by-side com tmux (transição)
  - Aprender os 9 modos do Zellij em vez dos prefixos do tmux.
  - Manter tmux pra SSH; Zellij pro local.
  - Ou ativar `tmux_compatibility = true` no Zellij pra usar `Ctrl-b` familiar (com tradeoffs — abordado em nota 06).

- **Armadilhas (≥5; CADA UMA com 4 labels):**

  1. **Achar que Zellij é tmux+chrome**
     - **Causa:** marketing/tutoriais focam em "tmux mais bonito".
     - **Sintoma:** frustração quando keybindings não casam.
     - **Como detectar:** você vai automaticamente pra `Ctrl-b`.
     - **Solução:** aprender os 9 modos (nota 03); ativar tmux compat só se realmente precisar (nota 06).

  2. **Instalar via apt em distros antigas**
     - **Causa:** repos podem ter Zellij 0.32 enquanto upstream está 0.41+.
     - **Sintoma:** features documentadas não funcionam (e.g. floating panes).
     - **Como detectar:** `zellij --version` mostra versão antiga.
     - **Solução:** instalar via GitHub releases ou cargo.

  3. **Misturar Zellij com keybindings de Vim**
     - **Causa:** muito do navegação interna (busca, scroll) usa keys parecidas mas em outros modos.
     - **Sintoma:** você está no scroll mode e Ctrl-d não funciona como em Vim.
     - **Como detectar:** confusão do que tá em qual modo.
     - **Solução:** ler nota 03 sobre modos; lembrar que status bar mostra atalhos do modo ativo.

  4. **Tentar usar Zellij via SSH em servidor que não tem**
     - **Causa:** Zellij é binário stand-alone — não vem com nada.
     - **Sintoma:** `zellij: command not found` no servidor remoto.
     - **Como detectar:** SSH e tente `which zellij`.
     - **Solução:** usar tmux no servidor; ou copiar binário Zellij pro servidor (statically-linked do release musl funciona em muitos Linux).

  5. **Esperar plugin ecosystem do tamanho do tmux**
     - **Causa:** Zellij é jovem (2020+); plugin system WASM ainda mais novo.
     - **Sintoma:** plugin equivalente ao tmux-yank, tmux-resurrect etc. não existe ou é menos polido.
     - **Como detectar:** procure por feature X em github.com/zellij-org/awesome-zellij e não encontra.
     - **Solução:** features built-in cobrem muito (copy-on-select default; sessions persistentes default); pra o resto, escrever plugin próprio (nota 06).

- **Em inglês (8-10 bullets):**

  Formato: `- **PT** — *EN*. "frase técnica curta."`

  Termos sugeridos: multiplexer; session; pane; tab; detach; attach; layout; discoverable; status bar; plugin.

- **Veja também (wikilinks SEM backticks):**
  - `[[02 - Modelo mental — sessions, tabs, panes]]` — próxima nota
  - `[[03 - Modos básicos e keybindings essenciais]]` — modos = diferencial chave
  - `[[06 - Modos avançados, plugins e copy-mode]]` — tmux compat mode
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#Multiplexer|multiplexer]]`

- **Referências:**
  - Zellij about — https://zellij.dev/about/
  - Zellij docs — https://zellij.dev/documentation/
  - tmux — https://github.com/tmux/tmux

- [ ] **Step 4: Adicionar verbete ao Dicionário**

Inserir no bloco `## Multiplexer / Zellij`:

```markdown
### Multiplexer
Programa que divide 1 terminal em múltiplas sessions, tabs e panes que sobrevivem a detach (desconexão do emulador). Server roda em background; cliente anexa/desanexa via `attach`/`detach`. Exemplos: Zellij, tmux, screen.

Veja também: [[01 - Zellij vs tmux vs screen]].
```

- [ ] **Step 5: Validar a rubrica**

```bash
test -f "03-Dominios/Terminal/Multiplexer/01 - Zellij vs tmux vs screen.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/01 - Zellij vs tmux vs screen.md"
grep -E "^### Multiplexer$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥6 wikilinks, verbete Multiplexer visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/01 - Zellij vs tmux vs screen.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): add nota 01 — Zellij vs tmux vs screen"
```

---

## Task 4: Nota 02 — Modelo mental: sessions, tabs, panes

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/02 - Modelo mental — sessions, tabs, panes.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Session (Zellij), Tab (Zellij), Pane, Floating pane, Stacked pane)

**Conteúdo-chave:** hierarquia 1 server → N sessions → N tabs → N panes (+ floating); como cada nível se comporta on detach; diferença entre suspended e closed; floating vs stacked vs split.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zellij.dev/documentation/overview
WebFetch: https://zellij.dev/documentation/panes
WebFetch: https://zellij.dev/documentation/tabs
WebFetch: https://zellij.dev/documentation/sessions
```

Capturar: hierarquia exata, comportamento em detach, definição de cada conceito.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Modelo mental — sessions, tabs, panes"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - multiplexer
  - zellij
  - iniciado
  - modelo-mental
aliases:
  - Modelo mental Zellij
  - Sessions tabs panes
---
```

- [ ] **Step 3: Escrever a nota**

**Cobrir:**

- **TL;DR:** "Zellij organiza tudo em 3 níveis: 1 server roda em background → N sessions nomeadas sobrevivem a detach → cada session tem N tabs → cada tab tem N panes (split, stacked, floating). Você sempre interage com 1 pane ativo; troca de pane/tab/session via keybindings."

- **O que é / Como funciona:**

  ### Hierarquia
  Diagrama ASCII (use 12-15 linhas):
  ```
  zellij server (background process)
   ├── session "default"
   │    ├── tab 1
   │    │    ├── pane A (active)
   │    │    └── pane B
   │    └── tab 2
   │         ├── pane C (split horizontal)
   │         ├── pane D (split vertical)
   │         └── pane E (floating, sobreposto)
   └── session "myproj"
        └── tab 1
             └── pane F (stacked com G, H minimized)
  ```

  ### Server
  - Inicia automático na primeira invocação de `zellij`.
  - Roda como processo separado; cliente comunica via Unix socket.
  - 1 server por user (por default); mata com `zellij kill-all-sessions` ou matando o processo.

  ### Session
  - Container nomeado. Sobrevive a fechar emulador, SSH drop, ou `detach`.
  - Default: nome aleatório (ex `quirky-llama`). Use `-s <nome>` pra controlar.
  - Lista com `zellij ls`. Anexa com `zellij attach <nome>`.
  - Comandos rodando dentro continuam rodando após detach.

  ### Tab
  - Agrupamento horizontal dentro de uma session.
  - Cada tab tem layout próprio de panes.
  - Mostra nome no topo (renomeable com Ctrl-t depois r).

  ### Pane — 3 tipos
  - **Split pane** — divisão padrão (vertical ou horizontal). Ocupa retângulo do grid da tab.
  - **Floating pane** — sobreposto, não ocupa grid. Movível, redimensionável. Útil pra terminal extra temporário sem reorganizar layout.
  - **Stacked pane** — múltiplos panes empilhados, 1 expandido + outros minimizados (mostra só barra de título). Útil quando você quer 5 logs visíveis mas só 1 em foco.

  ### Lifecycle: detach vs close
  - **Detach:** session segue rodando no server; panes seguem com comandos ativos. `Ctrl-o + d`.
  - **Close pane:** pane fecha; comando termina (SIGTERM). `Ctrl-p + x`.
  - **Close tab:** todos panes da tab fecham.
  - **Suspend** (não existe nativamente; floating panes "minimizados" são o mais próximo).

- **Na prática:**

  ### Criar a hierarquia
  ```bash
  # Start session nomeada
  zellij -s myproj

  # Dentro do Zellij:
  # Ctrl-t n — nova tab
  # Ctrl-p n — split pane direita
  # Ctrl-p d — split pane abaixo
  # Ctrl-p w — toggle floating pane
  # Ctrl-p s — toggle stacked
  ```

  ### Inspecionar sessions sem entrar
  ```bash
  zellij ls
  # Output:
  # myproj [Created 12m ago]
  # default [Created 3h ago] (EXITED - attach to resurrect)
  ```

  ### Mental model rápido
  - Quer separar projetos? → 1 session por projeto.
  - Quer separar "fases de trabalho" dentro do projeto? → tabs.
  - Quer ver várias coisas ao mesmo tempo? → splits.
  - Quer um terminal "extra" sem mexer no layout? → floating.
  - Quer 5 logs lado a lado mas só interagir com 1? → stacked.

- **Armadilhas (≥5):**

  1. **Confundir "fechar emulador" com "matar session"**
     - **Causa:** session persiste; matar emulador só desanexa.
     - **Sintoma:** processos seguem consumindo CPU após fechar terminal.
     - **Como detectar:** `zellij ls` mostra sessions vivas.
     - **Solução:** `zellij delete-session <nome>` se quiser realmente matar.

  2. **Acumular sessions abandonadas**
     - **Causa:** cada `zellij` sem `-s` cria session nova aleatória.
     - **Sintoma:** `zellij ls` mostra dezenas com nomes que você não reconhece.
     - **Como detectar:** olhar lista.
     - **Solução:** habituar-se ao `-s <nome>`; periódicamente `zellij delete-all-sessions` ou auto-attach pra default (nota 04).

  3. **Achar que floating pane sobrevive a detach diferente de split**
     - **Causa:** floating é só layout, não lifecycle.
     - **Sintoma:** espera que ao reattach o floating volte "minimizado" pré-configurado.
     - **Como detectar:** detach + reattach e ver layout.
     - **Solução:** floating pane volta onde estava ao detach; lifecycle igual ao split.

  4. **Esperar zoom/maximize de pane = stacked**
     - **Causa:** "stacked" Zellij ≠ "zoom" tmux.
     - **Sintoma:** queria full-screen do pane atual, ativou stacked e ficou com vários minimizados.
     - **Como detectar:** múltiplos panes minimizados aparecem na lateral.
     - **Solução:** usar zoom (`Ctrl-p +`/`Ctrl-p f` depending on version); stacked é pra agrupamento permanente.

  5. **Tab name confundido com window title**
     - **Causa:** tab Zellij ≠ tab do emulador (kitty/wezterm/foot tabs).
     - **Sintoma:** abre 2 tabs no Zellij, fecha o emulador, abre de novo e "tabs sumiram".
     - **Como detectar:** notar que Zellij tabs estão na barra interna Zellij, não na barra do emulador.
     - **Solução:** session contém tabs; reanexar session restaura tabs.

- **Em inglês:** session (session); pane (pane); tab (tab); detach (detach); attach (attach); split (split); floating (floating); stacked (stacked); server (server); foreground/active (foreground/active).

- **Veja também:**
  - `[[01 - Zellij vs tmux vs screen]]` — overview
  - `[[03 - Modos básicos e keybindings essenciais]]` — como criar/navegar
  - `[[04 - Sessões persistentes — detach, attach, gerenciamento]]` — lifecycle profundo
  - `[[05 - Layouts declarativos em KDL]]` — definir layout de panes/tabs em KDL
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#Session (Zellij)|session]]`, `[[Dicionário do Terminal#Tab (Zellij)|tab]]`, `[[Dicionário do Terminal#Pane|pane]]`, `[[Dicionário do Terminal#Floating pane|floating pane]]`, `[[Dicionário do Terminal#Stacked pane|stacked pane]]`

- **Referências:**
  - Zellij — Panes: https://zellij.dev/documentation/panes
  - Zellij — Tabs: https://zellij.dev/documentation/tabs
  - Zellij — Sessions: https://zellij.dev/documentation/sessions

- [ ] **Step 4: Adicionar 5 verbetes ao Dicionário**

Inserir em ordem alfabética no bloco `## Multiplexer / Zellij`:

```markdown
### Floating pane
Pane que aparece sobreposto ao grid de outros panes, sem ocupar espaço deles. Pode ser movido e redimensionado livremente. Útil pra terminal extra temporário (e.g. consultar `man` enquanto outro pane roda código).

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### Pane
Divisão interna de uma tab Zellij, rodando um shell ou comando. 3 tipos: split (ocupa grid), floating (sobreposto), stacked (empilhado). Pane ativa recebe input; outras seguem rodando.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### Session (Zellij)
Container nomeado de uma instância Zellij. Sobrevive a detach (fechar emulador, SSH drop). Contém N tabs, cada uma com N panes. Criar com `zellij -s <nome>`; listar com `zellij ls`; anexar com `zellij attach <nome>`.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]], [[04 - Sessões persistentes — detach, attach, gerenciamento]].

### Stacked pane
Modo de empilhamento de panes onde 1 é expandido e os outros aparecem só como barra de título (minimizados). Útil pra agrupar múltiplos logs/jobs com apenas 1 em foco.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### Tab (Zellij)
Agrupamento horizontal de panes dentro de uma session Zellij. Cada tab tem layout próprio. Mostra nome na barra superior. Diferente de tab do emulador (kitty/wezterm) — tabs Zellij vivem dentro da session.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Multiplexer/02 - Modelo mental — sessions, tabs, panes.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/02 - Modelo mental — sessions, tabs, panes.md"
grep -E "^### (Floating pane|Pane|Session \(Zellij\)|Stacked pane|Tab \(Zellij\))$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥8 wikilinks, 5 verbetes presentes.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/02 - Modelo mental — sessions, tabs, panes.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): add nota 02 — Modelo mental"
```

---

## Task 5: Nota 03 — Modos básicos e keybindings essenciais

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/03 - Modos básicos e keybindings essenciais.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Mode (Zellij), Status bar)

**Conteúdo-chave:** 9 modos do Zellij (normal, locked, pane, tab, resize, scroll, search, session, move) — overview; aprofundar normal, pane, tab; cheatsheet das ~20 keybindings iniciais.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zellij.dev/documentation/keybindings
WebFetch: https://zellij.dev/documentation/keybindings-modes
```

Capturar: lista exata dos modos, keybindings default de cada, como ativar.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Modos básicos e keybindings essenciais"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - multiplexer
  - zellij
  - iniciado
  - keybindings
aliases:
  - Modos Zellij
  - Keybindings Zellij
---
```

- [ ] **Step 3: Escrever a nota**

**Cobrir:**

- **TL;DR:** "Zellij é modal: você sempre está num modo (normal, pane, tab, etc.). Cada modo tem keybindings próprios — a status bar mostra todos. `Ctrl-<letra>` entra num modo; depois letras isoladas executam ações. Memorize 4 modos pra começar (normal, pane, tab, session) e ~20 keybindings."

- **O que é / Como funciona:**

  ### Por que modal
  - Tmux usa prefixo (`Ctrl-b <key>`). Zellij usa modos (`Ctrl-<modo>` entra; depois keys são atalhos do modo).
  - Vantagem: status bar mostra opções do modo. Você não decora — vê.
  - Desvantagem: 2 passos pra ações (Ctrl-modo + key) em vez de 1 pra alguns.

  ### Os 9 modos
  Tabela ou lista:
  - **Normal** — padrão. Tudo passa pro shell/app no pane. Ctrl-<modo> entra em outro modo.
  - **Locked** — desliga todos os keybindings Zellij. Tudo passa pro shell. Útil pra Emacs, Helix, apps que usam Ctrl-letra. `Ctrl-g` entra; `Ctrl-g` sai.
  - **Pane** — operações de pane (split, fechar, focar, redimensionar). `Ctrl-p`.
  - **Tab** — operações de tab (nova, fechar, próxima, renomear). `Ctrl-t`.
  - **Resize** — redimensiona pane focado. `Ctrl-n`.
  - **Scroll** — scrollback (subir, descer, page up/down, search). `Ctrl-s`.
  - **Search** — busca regex no scrollback (entra de Scroll). `Ctrl-s` depois `s`.
  - **Session** — operações de session (detach, renomear, kill, attach a outras). `Ctrl-o`.
  - **Move** — move pane focado dentro do grid. `Ctrl-h`.

  ### Como descobrir keybinding
  Status bar mostra atalhos do modo ativo (depende de plugin de status bar; default vem ativo). Se a status bar está apagada, ative no config (default `pane_frames true`).

  ### Mnemônica
  - `Ctrl-p` = **p**ane
  - `Ctrl-t` = **t**ab
  - `Ctrl-s` = **s**croll/**s**earch
  - `Ctrl-o` = **o**ptions/sessi**o**n
  - `Ctrl-n` = re**n**size (mnemônica fraca; basta ver status bar)
  - `Ctrl-g` = **g**rab keys (locked)
  - `Ctrl-h` = move (vem de hjkl?)

  Você não precisa decorar — basta lembrar de "olha a status bar".

- **Na prática:**

  ### Cheatsheet das 20 primeiras keybindings
  Tabela em 4 colunas (Modo / Sequência / Ação / Quando usar):

  | Modo | Sequência | Ação | Quando |
  |---|---|---|---|
  | (qualquer) | `Ctrl-p` | Entra modo pane | Vai mexer em panes |
  | Pane | `n` | Split vertical (nova pane direita) | Comparar 2 coisas lado a lado |
  | Pane | `d` | Split horizontal (nova pane abaixo) | Log/output abaixo do editor |
  | Pane | `x` | Fecha pane focada | Limpar |
  | Pane | `f` | Toggle full-screen | Foco temporário |
  | Pane | `w` | Toggle floating pane | Terminal extra |
  | Pane | hjkl | Foca pane direção | Navegar |
  | (qualquer) | `Ctrl-t` | Entra modo tab | Vai mexer em tabs |
  | Tab | `n` | Nova tab | Separar contexto |
  | Tab | `x` | Fecha tab | Limpar |
  | Tab | `r` | Renomeia tab | Organizar |
  | Tab | `h`/`l` | Tab anterior/próxima | Navegar |
  | (qualquer) | `Ctrl-o` | Entra modo session | |
  | Session | `d` | Detach (session continua) | Sair preservando |
  | Session | `w` | Lista sessions, anexa | Trocar de session |
  | (qualquer) | `Ctrl-s` | Entra modo scroll | Olhar histórico |
  | Scroll | `Ctrl-d`/`Ctrl-u` | Page down/up | |
  | Scroll | `s` | Vai pra search mode | Buscar regex |
  | (qualquer) | `Ctrl-g` | Lock keys (passa tudo pro app) | Emacs/Helix |
  | Locked | `Ctrl-g` | Desloga | Sair do locked |

  ### Workflow exemplo (primeiros 5min em Zellij)
  ```text
  1. Abre terminal, digita `zellij`
  2. Está no modo normal — digite comandos normalmente
  3. Quer split? `Ctrl-p` então `n` (vertical)
  4. Quer escrever no novo pane? Aperte `h`/`l` ou clique
  5. Quer voltar pra normal? ESC ou Ctrl-c ou (modo) repetido
  ```

- **Armadilhas (≥5):**

  1. **Ficar no modo errado e digitar atalhos**
     - **Causa:** entra modo pane, esquece, digita `x` querendo digitar `x` no shell.
     - **Sintoma:** pane fechou inesperadamente.
     - **Como detectar:** status bar mostra modo atual.
     - **Solução:** olhar status bar antes de cada keystroke até virar hábito; ESC volta pra normal.

  2. **Tentar usar locked mode achando que "trava o cursor"**
     - **Causa:** nome confuso; "locked" = atalhos Zellij desligados, não input.
     - **Sintoma:** confusão sobre o que locked faz.
     - **Como detectar:** ler doc.
     - **Solução:** usar locked SÓ quando app no pane precisa de Ctrl-letra (Emacs, Helix).

  3. **Status bar desligada**
     - **Causa:** plugin de status bar desabilitado no config, ou tema custom sem.
     - **Sintoma:** não sabe em que modo está; difícil descobrir atalhos.
     - **Como detectar:** olhar borda inferior do Zellij — se vazia, status bar está off.
     - **Solução:** ativar default status bar plugin (default no Zellij stock). Se config customizado, conferir `default_layout` (nota 05).

  4. **Confundir Ctrl-letra com prefixo tmux**
     - **Causa:** muscle memory de tmux.
     - **Sintoma:** digita `Ctrl-b` esperando trigger; nada acontece.
     - **Como detectar:** notar que o atalho não disparou nada.
     - **Solução:** treinar Ctrl-<modo> (`p`/`t`/`s`/`o`); ou ativar tmux compat mode (nota 06, com tradeoffs).

  5. **Esperar que setas funcionem em todos os modos**
     - **Causa:** setas funcionam em alguns modos (resize, scroll), mas no normal vão pro shell/app.
     - **Sintoma:** queria navegar entre panes com setas; nada acontece.
     - **Como detectar:** testar.
     - **Solução:** modo pane + hjkl ou setas. Em normal, setas vão pro app dentro do pane.

- **Em inglês:** modal (modal); keybinding (keybinding); mode (mode); shortcut (shortcut); discoverability (discoverability); status bar (status bar); chord (chord); muscle memory (muscle memory); cheatsheet (cheatsheet); passthrough (passthrough).

- **Veja também:**
  - `[[02 - Modelo mental — sessions, tabs, panes]]` — o que os modos manipulam
  - `[[04 - Sessões persistentes — detach, attach, gerenciamento]]` — modo session
  - `[[06 - Modos avançados, plugins e copy-mode]]` — locked, scroll, search avançados
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#Mode (Zellij)|mode]]`, `[[Dicionário do Terminal#Status bar|status bar]]`

- **Referências:**
  - Zellij — Keybindings: https://zellij.dev/documentation/keybindings

- [ ] **Step 4: Adicionar 2 verbetes**

```markdown
### Mode (Zellij)
Estado modal do Zellij — controla quais keybindings estão ativas. 9 modos default: normal (default, input vai pro shell), locked (passthrough), pane, tab, resize, scroll, search, session, move. Entrar via `Ctrl-<letra>`; sair via ESC ou repetir o atalho.

Veja também: [[03 - Modos básicos e keybindings essenciais]].

### Status bar
Barra de informações na borda inferior do Zellij que mostra modo ativo, tabs abertas e atalhos disponíveis. Implementada como plugin (default ativo). Pode ser substituída por plugins custom como zjstatus.

Veja também: [[03 - Modos básicos e keybindings essenciais]], [[06 - Modos avançados, plugins e copy-mode]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Multiplexer/03 - Modos básicos e keybindings essenciais.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/03 - Modos básicos e keybindings essenciais.md"
grep -E "^### (Mode \(Zellij\)|Status bar)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥6 wikilinks, 2 verbetes.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/03 - Modos básicos e keybindings essenciais.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): add nota 03 — Modos básicos"
```

---

## ✅ Checkpoint Iniciado

Após Task 5, 3 notas de Iniciado entregues. Verificar:

```bash
ls -1 "03-Dominios/Terminal/Multiplexer/" | sort
git log --oneline | head -7
```

Esperado: 3 notas + `index.md`. Últimos commits do galho.

---

## Task 6: Nota 04 — Sessões persistentes: detach, attach, gerenciamento

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes — detach, attach, gerenciamento.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Attach, Detach)

**Conteúdo-chave:** `zellij`, `zellij attach`, `zellij ls`, `zellij delete-session`, auto-attach, resume vs new, naming, cleanup.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zellij.dev/documentation/sessions
WebFetch: https://zellij.dev/documentation/commands
```

Capturar: lista exata de subcomandos session-related, flags.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Sessões persistentes — detach, attach, gerenciamento"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - multiplexer
  - zellij
  - adepto
  - sessions
aliases:
  - Sessions Zellij
  - Detach attach
---
```

- [ ] **Step 3: Escrever a nota**

**Cobrir:**

- **TL;DR:** "Sessions são o motor de persistência. `zellij` cria/anexa default; `-s <nome>` nomeia; `zellij ls` lista; `attach <nome>` reconecta; `delete-session <nome>` mata. Detach via `Ctrl-o d` — server segue rodando, comandos seguem executando, layouts preservados. Workflow recomendado: 1 session por projeto, auto-attach no shell start."

- **O que é / Como funciona:**

  ### O que persiste
  - Layout de tabs/panes ✓
  - Comandos rodando em cada pane ✓
  - Scrollback de cada pane ✓ (até limite configurável)
  - Working directory de cada pane ✓
  - Variáveis de ambiente das shells ✓ (porque o processo segue vivo)
  - Conexões SSH abertas dentro de panes ✓ (mesmo conceito)

  ### O que NÃO persiste
  - Reboot da máquina (server morre).
  - `zellij kill-all-sessions`.
  - SIGKILL no processo do server.

  ### Comandos canônicos
  ```bash
  # Criar/anexar session com nome
  zellij -s myproj

  # Listar sessions (incluindo EXITED — não-anexáveis até resurrect)
  zellij ls
  # Output:
  # myproj [Created 2h ago] (current)
  # quirky-llama [Created 5d ago] (EXITED - attach to resurrect)

  # Anexar a session existente
  zellij attach myproj

  # Criar se não existir (idempotente)
  zellij attach --create myproj

  # Detach de dentro da session
  # (não é shell command — é keybinding) Ctrl-o + d

  # Matar session (acabou de vez)
  zellij delete-session myproj
  zellij delete-session myproj --force   # mata mesmo se ainda anexado

  # Matar todas
  zellij delete-all-sessions
  zellij delete-all-sessions --yes
  ```

  ### Kill vs Delete
  - `zellij kill-session <nome>` — mata o processo da session, mas mantém entry em "EXITED" (pode ressuscitar via `attach`).
  - `zellij delete-session <nome>` — remove de vez.

  ### Resume vs new
  - Anexar EXITED session "resurrects" — recria os panes (mas commands não rodam de novo; layout retornado, conteúdo perdido).
  - Distingue: layout retorna, output histórico não.

- **Na prática:**

  ### 1 session por projeto
  ```bash
  # No .zshrc/.bashrc (opcional)
  alias z='zellij attach --create'

  # Uso
  z myproj         # cria ou anexa
  z backend
  z notes
  ```

  ### Auto-attach default
  ```kdl
  // ~/.config/zellij/config.kdl
  on_force_close "detach"
  ```

  Mais robusto: shell init checks se está dentro de Zellij; se não, anexa/cria default:
  ```bash
  # ~/.zshrc — só se TTY interativa
  if [[ -z "$ZELLIJ" ]] && [[ -t 0 ]] && [[ -t 1 ]]; then
    zellij attach --create default
  fi
  ```

  ### Cleanup periódico
  ```bash
  zellij ls
  # Veja quais EXITED há semanas — delete

  # Mata todas EXITED de uma vez
  zellij ls --short | xargs -I{} zellij delete-session {} 2>/dev/null
  ```

  (Verificar se `--short` existe na versão atual; senão, parsear `ls` regular.)

- **Armadilhas (≥5):**

  1. **`attach` num nome typo cria session nova**
     - **Causa:** sem `--create` é attach só. Com `--create`, idempotente — risco menor.
     - **Sintoma:** "attach myporj" cria session "myporj" sem avisar.
     - **Como detectar:** `zellij ls` mostra duas sessions parecidas.
     - **Solução:** sempre `attach <nome>` (sem `--create`) primeiro; se não existir, erro claro. Ou usar `--create` sempre e aceitar typos virarem sessions.

  2. **Detach acidental matando session inteira**
     - **Causa:** confundir detach (`Ctrl-o d`) com delete-session.
     - **Sintoma:** session some.
     - **Como detectar:** `zellij ls`.
     - **Solução:** detach NÃO mata; só desconecta. Se sumiu, foi outra coisa (delete, kill-all, ou server crash).

  3. **Server crash leva todas sessions junto**
     - **Causa:** sessions vivem no server; server cai = sessions caem.
     - **Sintoma:** todas sessions sumiram do `ls` depois de reboot/crash.
     - **Como detectar:** óbvio.
     - **Solução:** Zellij não tem resurrect via dump como tmux-resurrect; aceitar e usar layouts (nota 05) pra recriar rápido.

  4. **EXITED accumulando**
     - **Causa:** session morre (e.g. comando exit do shell), entry fica EXITED até delete explícito.
     - **Sintoma:** `zellij ls` polui com EXITED.
     - **Como detectar:** olhar lista.
     - **Solução:** cleanup periódico (`delete-session` ou `delete-all-sessions`). Não tem auto-cleanup default.

  5. **Anexar uma session já anexada de outro terminal**
     - **Causa:** Zellij default permite múltiplos clients no mesmo session.
     - **Sintoma:** 2 emuladores mostrando mesma session — input/output replicado.
     - **Como detectar:** ver borda Zellij em 2 lugares.
     - **Solução:** geralmente é feature (e.g. mostrar code review pra alguém). Se não quer, detach de um lado. `delete-session --force` fecha tudo.

- **Em inglês:** session (session); detach (detach); attach (attach); persistent (persistent); resurrect (resurrect); idempotent (idempotent); cleanup (cleanup); kill (kill); delete (delete); resume (resume).

- **Veja também:**
  - `[[02 - Modelo mental — sessions, tabs, panes]]` — hierarquia
  - `[[03 - Modos básicos e keybindings essenciais]]` — modo session (Ctrl-o)
  - `[[05 - Layouts declarativos em KDL]]` — usar layouts em vez de tentar resurrect
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#Session (Zellij)|session]]`, `[[Dicionário do Terminal#Attach|attach]]`, `[[Dicionário do Terminal#Detach|detach]]`

- **Referências:**
  - Zellij — Sessions: https://zellij.dev/documentation/sessions
  - Zellij — Commands: https://zellij.dev/documentation/commands

- [ ] **Step 4: Adicionar 2 verbetes**

```markdown
### Attach
Reconectar a uma session Zellij em background. Comando: `zellij attach <nome>` ou `zellij attach --create <nome>` (idempotente). Múltiplos clients podem anexar à mesma session (input replicado).

Veja também: [[04 - Sessões persistentes — detach, attach, gerenciamento]].

### Detach
Desconectar de uma session Zellij sem matar — server segue rodando, panes seguem executando comandos. Keybinding: `Ctrl-o d` (session mode + detach). Não é destrutivo; reconectar via `zellij attach`.

Veja também: [[04 - Sessões persistentes — detach, attach, gerenciamento]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes — detach, attach, gerenciamento.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes — detach, attach, gerenciamento.md"
grep -E "^### (Attach|Detach)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes — detach, attach, gerenciamento.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): add nota 04 — Sessões persistentes"
```

---

## Task 7: Nota 05 — Layouts declarativos em KDL

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/05 - Layouts declarativos em KDL.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: KDL, Layout (Zellij))

**Conteúdo-chave:** sintaxe KDL básica; estrutura `layout { tab { pane ... } }`; propriedades; floating/stacked declarativo; default_layout; layouts customizados.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zellij.dev/documentation/layouts
WebFetch: https://kdl.dev/
```

Capturar: sintaxe canônica KDL; lista de propriedades de pane/tab.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Layouts declarativos em KDL"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - multiplexer
  - zellij
  - adepto
  - layouts
  - kdl
aliases:
  - Layouts Zellij
  - KDL Zellij
---
```

- [ ] **Step 3: Escrever a nota**

**Cobrir:**

- **TL;DR:** "Layouts Zellij são arquivos KDL que descrevem tabs/panes/splits/cwd/comando. KDL é uma linguagem declarativa: nó { propriedade=valor; child }. `default_layout = "<nome>"` no config aplica auto; `zellij --layout <nome>` aplica ad-hoc. Layouts vivem em `~/.config/zellij/layouts/<nome>.kdl`. Versioná-los nos dotfiles = setup repetível."

- **O que é / Como funciona:**

  ### KDL — sintaxe mínima
  ```kdl
  // Comentário de linha
  /* Comentário de bloco */

  // Nó com propriedade
  pane size=10

  // Nó com children (entre {})
  tab name="dev" {
      pane split_direction="vertical" {
          pane
          pane
      }
  }

  // String com aspas / sem aspas
  pane command="nvim"
  pane cwd="~/repos/myproj"
  ```

  Sites e doc: KDL = "Cuddly Document Language" — sintaxe humana, sem aspas obrigatórias na maioria das chaves.

  ### Estrutura de layout Zellij
  ```kdl
  layout {
      tab name="editor" {
          pane size="80%" {
              pane command="nvim"
          }
          pane size="20%" {
              pane
              pane
          }
      }
      tab name="logs" {
          pane command="tail" {
              args "-f" "/var/log/syslog"
          }
      }
  }
  ```

  ### Propriedades de pane mais usadas
  Tabela:
  | Propriedade | Tipo | Exemplo | Quando |
  |---|---|---|---|
  | `command` | string | `command="nvim"` | Executar comando ao abrir |
  | `args` | nó filho | `args "-f" "log"` | Args do comando |
  | `cwd` | path | `cwd="~/myproj"` | Working dir do pane |
  | `size` | string | `size="50%"` ou `size=10` | Tamanho relativo ou fixo (linhas/colunas) |
  | `split_direction` | string | `split_direction="vertical"` | Como split filhos |
  | `borderless` | bool | `borderless=true` | Sem borda visível |
  | `focus` | bool | `focus=true` | Pane que começa em foco |
  | `name` | string | `name="editor"` | Nome do pane (mostrado se borderless=false) |

  ### Floating panes em layout
  ```kdl
  layout {
      tab {
          pane
      }
      floating_panes {
          pane {
              x "20%"
              y "20%"
              width "60%"
              height "60%"
              command "btop"
          }
      }
  }
  ```

  ### Stacked panes
  ```kdl
  layout {
      pane stacked=true {
          pane name="server"
          pane name="db"
          pane name="cache"
      }
  }
  ```

  ### default_layout
  ```kdl
  // ~/.config/zellij/config.kdl
  default_layout "compact"
  // ou nome de layout customizado:
  // default_layout "my-dev"
  ```

  - Built-ins: `default`, `strider`, `compact`, `disable-status-bar`.
  - Custom: file em `~/.config/zellij/layouts/<nome>.kdl`.

- **Na prática:**

  ### Template "dev" — editor + shell + watcher
  Arquivo `~/.config/zellij/layouts/dev.kdl`:
  ```kdl
  layout {
      tab name="code" {
          pane split_direction="vertical" {
              pane size="70%" {
                  pane command="nvim" focus=true
              }
              pane size="30%" {
                  pane name="shell"
                  pane name="watch" command="npm" {
                      args "run" "dev"
                  }
              }
          }
      }
      tab name="git" {
          pane command="lazygit"
      }
  }
  ```

  Carregar:
  ```bash
  zellij --layout dev
  ```

  ### Template "monitor" — observabilidade
  ```kdl
  layout {
      tab name="monitor" {
          pane split_direction="horizontal" {
              pane command="btop"
              pane command="journalctl" {
                  args "-f" "-n" "50"
              }
          }
      }
  }
  ```

  ### Versionar layouts
  Symlink: `~/.config/zellij/layouts/` ↔ pasta no repo de dotfiles. Layouts viram parte do setup. Nota: o galho 5 (Dotfiles) cobre estratégias de symlink/stow.

- **Armadilhas (≥5):**

  1. **Esquecer aspas em comandos com espaço**
     - **Causa:** KDL tolera sem aspas pra strings simples, mas espaço quebra.
     - **Sintoma:** `command=npm run dev` é parseado como `command="npm"` + tokens extras.
     - **Como detectar:** `zellij --layout meulayout` falha ou comporta estranho.
     - **Solução:** `command="npm"` + `args "run" "dev"` (args é nó filho).

  2. **`cwd` sem expansão de `~`**
     - **Causa:** algumas versões de Zellij não expandem `~` em `cwd` automaticamente.
     - **Sintoma:** pane abre num dir errado.
     - **Como detectar:** abrir pane e `pwd`.
     - **Solução:** usar path absoluto (`/home/<user>/...` — generalize com env var no shell init em vez de hardcode), ou checar versão Zellij.

  3. **Size em % não soma 100**
     - **Causa:** Zellij não normaliza — se você puser 70% + 70%, o segundo pane sobrescreve ou crash.
     - **Sintoma:** layout torto ou erro.
     - **Como detectar:** olhar visual.
     - **Solução:** soma percentual = 100; alternativa: tamanhos fixos em linhas/colunas (`size=20`).

  4. **`focus=true` em mais de um pane**
     - **Causa:** copy-paste descuidado.
     - **Sintoma:** comportamento imprevisível — Zellij escolhe um.
     - **Como detectar:** layout abre com pane de foco "errada".
     - **Solução:** apenas 1 pane com `focus=true` por tab.

  5. **Layout custom não carrega**
     - **Causa:** arquivo no caminho errado, nome sem `.kdl`, ou sintaxe inválida.
     - **Sintoma:** `zellij --layout meulayout` falha com erro KDL.
     - **Como detectar:** ler erro stderr.
     - **Solução:** `ls ~/.config/zellij/layouts/` confirma path; `zellij setup --check` valida config; abrir KDL em editor com syntax highlighting (LSP `kdl-lsp` se existe).

- **Em inglês:** layout (layout); declarative (declarative); imperative (imperative); pane (pane); split direction (split direction); floating (floating); stacked (stacked); cwd (cwd / working directory); template (template); workspace (workspace).

- **Veja também:**
  - `[[02 - Modelo mental — sessions, tabs, panes]]` — o que está sendo declarado
  - `[[04 - Sessões persistentes — detach, attach, gerenciamento]]` — sessions usam layouts
  - `[[07 - Integração com Neovim e shell]]` — layouts pra workflows comuns
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#KDL|KDL]]`, `[[Dicionário do Terminal#Layout (Zellij)|layout]]`

- **Referências:**
  - Zellij — Layouts: https://zellij.dev/documentation/layouts
  - KDL spec: https://kdl.dev/

- [ ] **Step 4: Adicionar 2 verbetes**

```markdown
### KDL
Cuddly Document Language — linguagem de configuração declarativa com sintaxe humana (sem aspas obrigatórias na maioria das chaves, comentários nativos, suporte a tipos básicos e children). Usada pela config e pelos layouts do Zellij.

Veja também: [[05 - Layouts declarativos em KDL]].

### Layout (Zellij)
Definição declarativa em KDL de tabs, panes, splits, cwd, comandos de auto-start. Arquivo `.kdl` em `~/.config/zellij/layouts/`. Carregado via `default_layout "<nome>"` no config ou ad-hoc com `zellij --layout <nome>`.

Veja também: [[05 - Layouts declarativos em KDL]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Multiplexer/05 - Layouts declarativos em KDL.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/05 - Layouts declarativos em KDL.md"
grep -E "^### (KDL|Layout \(Zellij\))$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/05 - Layouts declarativos em KDL.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): add nota 05 — Layouts KDL"
```

---

## ✅ Checkpoint Adepto

Após Task 7, 2 notas Adepto entregues. Total no galho: 5 notas + MOC.

```bash
ls -1 "03-Dominios/Terminal/Multiplexer/" | sort
```

---

## Task 8: Nota 06 — Modos avançados, plugins e copy-mode

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/06 - Modos avançados, plugins e copy-mode.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Locked mode, Plugin (Zellij), Pipe API, Tmux compat mode)

**Conteúdo-chave:** locked mode (passthrough), scroll/search avançado, tmux compat mode, arquitetura plugins WASM (lifecycle, pipe API, permissions), 2-3 plugins concretos verificados.

- [ ] **Step 1: Pesquisa-âncora (CRÍTICA — VERIFICAR PLUGINS)**

```
WebFetch: https://zellij.dev/documentation/plugins
WebFetch: https://github.com/zellij-org/awesome-zellij
WebFetch: https://github.com/dj95/zjstatus
```

Pra cada plugin candidato (zjstatus, vim-zellij-navigator, plus 1 outro):
- URL retorna 200?
- Último commit < 1 ano?
- README ainda lista features que vamos citar?

Se algum não passar, substituir por outro do `awesome-zellij`.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Modos avançados, plugins e copy-mode"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - multiplexer
  - zellij
  - magus
  - plugins
  - wasm
aliases:
  - Plugins Zellij
  - Tmux compat
---
```

- [ ] **Step 3: Escrever a nota**

**Cobrir:**

- **TL;DR:** "Locked mode passa keys pro app (Emacs/Helix). Scroll + search mode = `Ctrl-s` + navegação tipo vim no scrollback. Tmux compat mode (`tmux_compatibility = true`) traz keybindings tmux-like — útil pra migração. Plugins Zellij são WASM (sandbox, qualquer linguagem que compila pra WASM); arquitetura: lifecycle `load`/`update`/`render` + Pipe API + permissões capability-based. Plugins concretos: zjstatus (status bar), [plugin 2], [plugin 3]."

- **O que é / Como funciona:**

  ### Locked mode
  - Atalho: `Ctrl-g` (de qualquer modo) → entra locked. `Ctrl-g` de novo → sai.
  - Comportamento: TODOS os keybindings Zellij desligados. Tudo (Ctrl-p, Ctrl-t, etc.) vai direto pro app no pane ativo.
  - Quando ativar: Emacs (`Ctrl-x`), Helix (`Ctrl-w`), apps shell interativos que conflitam.
  - Status bar mostra "LOCKED" claramente.

  ### Scroll mode + search mode
  - `Ctrl-s` entra Scroll. Você pode rolar com setas, page up/down, gg/G (em algumas versões), `Ctrl-d`/`Ctrl-u`.
  - Dentro do scroll, `s` entra Search mode — digite regex, Enter pra buscar, `n`/`N` pra próximo/anterior.
  - Copy-mode: dentro do scroll/search, `Ctrl-c` ou ESC sai. Selecionar texto = clique e arrasta (mouse copy default) ou keyboard (depende da versão; ver doc).

  ### Tmux compat mode
  Ativar:
  ```kdl
  // ~/.config/zellij/config.kdl
  default_mode "tmux"
  ```

  Efeito: keybindings principais se aproximam de tmux:
  - `Ctrl-b` vira prefixo (em vez de modos)
  - Após `Ctrl-b`: `c` (new tab), `n` (next), `%` (split vert), `"` (split horiz), `d` (detach), etc.

  Tradeoffs:
  - Vantagem: muscle memory tmux funciona.
  - Desvantagem: perde discoverabilidade dos modos; menos idiomático.

  Recomendação: usar SÓ se migrar de tmux e não quer aprender modos.

  ### Arquitetura de plugins WASM

  **Por que WASM:**
  - Sandbox (plugin não acessa filesystem/network arbitrariamente)
  - Multilang (Rust, Zig, Go, AssemblyScript — qualquer linguagem que compila WASM)
  - Hot reload (recarregar sem restart do Zellij)

  **Lifecycle (callbacks que o plugin implementa):**
  - `load(...)` — carrega; recebe configuração
  - `update(event)` — eventos do Zellij (mode change, pane change, etc.)
  - `render(rows, cols)` — desenha UI (retorna string que o Zellij printa no espaço alocado)

  **Pipe API:**
  - Comunicação bidirecional Zellij ↔ plugin via "pipes" nomeados
  - Plugin pode emitir mensagens (`pipe()`) e receber (`PipeMessage` event)
  - Útil pra plugins que se comunicam entre si ou com scripts shell externos (`zellij action pipe`)

  **Permissions:**
  - Capability-based: plugin declara permissões necessárias no manifest
  - Examples: `ReadApplicationState`, `ChangeApplicationState`, `OpenFiles`, `WriteToStdin`
  - User aprova na primeira carga (interativo)

- **Na prática:**

  ### Carregar plugin externo
  ```bash
  # Download
  curl -L -o ~/.config/zellij/plugins/zjstatus.wasm \
    https://github.com/dj95/zjstatus/releases/latest/download/zjstatus.wasm

  # Usar em layout
  ```

  ```kdl
  // ~/.config/zellij/layouts/custom-status.kdl
  layout {
      pane size=1 borderless=true {
          plugin location="file:~/.config/zellij/plugins/zjstatus.wasm"
      }
      pane
  }
  ```

  ### Plugin 1 — zjstatus
  (Confirmar URL e features ativas no Step 1.)
  - Repo: https://github.com/dj95/zjstatus
  - Substitui status bar built-in
  - Configurável: módulos (modo, tabs, git, hostname, datetime), cores, separadores
  - Config inline no layout via `plugin { ... }` properties

  ### Plugin 2 — [confirmar nome verificado no Step 1]
  (Sugestão inicial: `multitask` ou outro presente em awesome-zellij com último commit recente.)

  ### Plugin 3 — vim-zellij-navigator
  - Repo: https://github.com/hiasr/vim-zellij-navigator
  - Bridge entre Neovim splits e Zellij panes — Ctrl-h/j/k/l navega ambos
  - Cobertura profunda na nota 07

  ### Debugar plugin
  ```bash
  # Reload sem restart
  zellij action launch-plugin "file:~/.config/zellij/plugins/meuplugin.wasm"

  # Tail logs
  tail -f ~/.cache/zellij/<session>/zellij-log/zellij.log
  ```

- **Armadilhas (≥5):**

  1. **Locked mode + `Ctrl-g` colide com Emacs (que usa Ctrl-g pra abort)**
     - **Causa:** keybinding default colide com hotkey importante de Emacs.
     - **Sintoma:** dentro do Emacs em locked mode, `Ctrl-g` aborta em vez de sair do locked.
     - **Como detectar:** testar.
     - **Solução:** remap do unlock pra outro key no `config.kdl`; ou aceitar e usar mouse pra clicar em outro pane.

  2. **Tmux compat mode + plugin que espera modes**
     - **Causa:** alguns plugins assumem keybindings modais default; em tmux mode, não disparam.
     - **Sintoma:** plugin não responde.
     - **Como detectar:** ler README do plugin.
     - **Solução:** plugins com features customizáveis funcionam; senão, escolher entre tmux mode ou plugin.

  3. **WASM plugin com permissão negada**
     - **Causa:** primeira carga pede aprovação interativa.
     - **Sintoma:** plugin não funciona, sem mensagem clara.
     - **Como detectar:** olhar logs (`zellij.log`).
     - **Solução:** abrir plugin de novo e aprovar; ou pré-aprovar em config (`allow_permissions`).

  4. **Versão WASM incompatível**
     - **Causa:** API de plugins muda entre versões Zellij; plugin compilado pra 0.40 pode quebrar em 0.42.
     - **Sintoma:** plugin não carrega; log fala em ABI version.
     - **Como detectar:** logs.
     - **Solução:** atualizar plugin; reportar issue; downgrade temporário.

  5. **Search regex case-sensitive default**
     - **Causa:** Zellij default é case-sensitive em search mode.
     - **Sintoma:** busca "Error" não acha "error" no scrollback.
     - **Como detectar:** testar.
     - **Solução:** prefixar regex com `(?i)` (modificador case-insensitive) ou conferir config option (verificar versão).

- **Em inglês:** plugin (plugin); WASM (WebAssembly); sandbox (sandbox); hot reload (hot reload); capability (capability); permission (permission); lifecycle (lifecycle); pipe (pipe); event (event); render (render).

- **Veja também:**
  - `[[03 - Modos básicos e keybindings essenciais]]` — modos base
  - `[[05 - Layouts declarativos em KDL]]` — onde plugin é referenciado em layout
  - `[[07 - Integração com Neovim e shell]]` — vim-zellij-navigator profundo
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#Plugin (Zellij)|plugin]]`, `[[Dicionário do Terminal#Pipe API|pipe API]]`, `[[Dicionário do Terminal#Locked mode|locked mode]]`, `[[Dicionário do Terminal#Tmux compat mode|tmux compat]]`

- **Referências:**
  - Zellij — Plugins: https://zellij.dev/documentation/plugins
  - awesome-zellij: https://github.com/zellij-org/awesome-zellij
  - zjstatus: https://github.com/dj95/zjstatus
  - vim-zellij-navigator: https://github.com/hiasr/vim-zellij-navigator

- [ ] **Step 4: Adicionar 4 verbetes**

```markdown
### Locked mode
Modo do Zellij que desliga todos os keybindings internos — input vai direto pro app no pane ativo. Útil pra Emacs, Helix, apps que usam Ctrl-letra. Atalho default: `Ctrl-g` (entra e sai).

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### Pipe API
Interface bidirecional Zellij ↔ plugin pra comunicação assíncrona via "pipes" nomeados. Plugin pode emitir (`pipe()`) e receber (`PipeMessage` event); scripts shell externos podem injetar mensagens com `zellij action pipe`.

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### Plugin (Zellij)
Módulo WASM que estende Zellij (status bar, navegador entre Neovim/Zellij, plugins de produtividade, etc.). Sandbox capability-based: plugin declara permissões; user aprova na primeira carga. Lifecycle: `load`/`update`/`render`. Multilang (Rust, Zig, Go, AssemblyScript).

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### Tmux compat mode
Modo de configuração do Zellij (`default_mode "tmux"`) que ativa keybindings tmux-like (prefixo `Ctrl-b`, `c` novo tab, `%` split, etc.). Útil pra migração; tradeoff: perde discoverabilidade dos modos.

Veja também: [[06 - Modos avançados, plugins e copy-mode]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Multiplexer/06 - Modos avançados, plugins e copy-mode.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/06 - Modos avançados, plugins e copy-mode.md"
grep -E "^### (Locked mode|Pipe API|Plugin \(Zellij\)|Tmux compat mode)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/06 - Modos avançados, plugins e copy-mode.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-multiplexer): add nota 06 — Modos avançados, plugins, copy-mode"
```

---

## Task 9: Nota 07 — Integração com Neovim e shell

**Files:**
- Create: `03-Dominios/Terminal/Multiplexer/07 - Integração com Neovim e shell.md`
- (Sem verbetes novos no Dicionário — apenas referencia verbetes existentes.)

**Conteúdo-chave:** focus events, vim-zellij-navigator (Ctrl-hjkl unificado), status bar dinâmico, `zellij action write-chars`/`send-keys`, hooks pre-detach.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/hiasr/vim-zellij-navigator
WebFetch: https://zellij.dev/documentation/cli
```

Capturar: sintaxe atual de `zellij action`, instalação vim-zellij-navigator, config canônico.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Integração com Neovim e shell"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - multiplexer
  - zellij
  - magus
  - integration
  - neovim
aliases:
  - Integração Zellij Neovim
---
```

- [ ] **Step 3: Escrever a nota**

**Cobrir:**

- **TL;DR:** "Zellij integra com Neovim de duas formas principais: focus events (autocmds `FocusGained`/`FocusLost` disparam ao mudar de pane) e vim-zellij-navigator (Ctrl-hjkl navega Neovim splits + Zellij panes com mesma keybinding). Shell integration via `zellij action` permite scripts orquestrarem panes (abrir comando, enviar keys, focar)."

- **O que é / Como funciona:**

  ### Focus events
  - Zellij propaga focus pra Neovim via terminal escape sequences padrão.
  - Neovim recebe e dispara autocmd:
  ```lua
  vim.api.nvim_create_autocmd("FocusGained", {
    callback = function()
      vim.cmd("checktime")  -- recarrega buffers se mudaram no disco
    end,
  })
  ```
  - Habilita workflow: edita arquivo em outro pane (via emacs/sed/lazygit), volta pro Neovim, ele recarrega automaticamente.

  ### vim-zellij-navigator
  - Repo: https://github.com/hiasr/vim-zellij-navigator
  - Bridge bidirecional: `Ctrl-h/j/k/l` em Neovim navega splits; ao atingir borda, "atravessa" pra Zellij pane vizinho. Vice-versa.
  - Análogo ao vim-tmux-navigator pra quem migra.

  **Instalação no Neovim (lazy.nvim):**
  ```lua
  {
    "https://github.com/hiasr/vim-zellij-navigator",
    config = function()
      vim.keymap.set("n", "<C-h>", ":ZellijNavigateLeft<CR>", { silent = true })
      vim.keymap.set("n", "<C-j>", ":ZellijNavigateDown<CR>", { silent = true })
      vim.keymap.set("n", "<C-k>", ":ZellijNavigateUp<CR>", { silent = true })
      vim.keymap.set("n", "<C-l>", ":ZellijNavigateRight<CR>", { silent = true })
    end,
  }
  ```

  **Instalação no Zellij (plugin WASM):**
  Adicionar layout/keybinding chamando o plugin (ver README atualizado).

  ### Shell integration via `zellij action`
  CLI pra orquestrar Zellij de fora:
  ```bash
  # Enviar comando pra pane focado
  zellij action write-chars "ls\n"

  # Abrir comando em novo pane
  zellij action new-pane --command "htop"

  # Focar tab por nome
  zellij action go-to-tab-name "logs"

  # Send keys (raw, sem newline)
  zellij action send-keys "Ctrl-c"
  ```

  Útil pra scripts: `dev.sh` abre Zellij com layout + comandos pré-rodados.

  ### Status bar dinâmico mostrando contexto Neovim
  - zjstatus (nota 06) pode exibir variáveis arbitrárias via Pipe API.
  - Plugin Neovim pode enviar branch git, modo (NORMAL/INSERT), nome do buffer pro zjstatus periodicamente.
  - Implementação: autocmd em Neovim → `vim.fn.system("zellij action pipe ...")`.

- **Na prática:**

  ### Workflow "edita-em-outro-pane-e-volta"
  1. Em Neovim, edita `app.js`.
  2. `Ctrl-p w` (toggle floating pane); roda `lazygit`; faz stash.
  3. Volta pro Neovim (`Ctrl-p w` de novo, ou Ctrl-hjkl com navigator).
  4. Neovim detecta focus + recarrega buffer modificado. Sem perder estado.

  ### Workflow "dev session script"
  ```bash
  #!/usr/bin/env bash
  # dev.sh — abre setup completo
  zellij --layout dev -s myproj
  ```

  Combinado com layout `dev` da nota 05, o script abre Zellij com editor + shell + watcher rodando.

  ### Workflow "send command pra pane vizinho"
  ```bash
  # Da pane A, enviar `npm test` pra pane B (focando primeiro)
  zellij action focus-next-pane
  zellij action write-chars "npm test"
  zellij action write-chars $'\n'  # newline
  ```

- **Armadilhas (≥5):**

  1. **`zellij action` sem session ativa**
     - **Causa:** comandos `action` precisam de uma session current; rodar de fora do Zellij sem flag falha.
     - **Sintoma:** "no current session" ou similar.
     - **Como detectar:** rodar `zellij action ...` de shell não-Zellij.
     - **Solução:** rodar de dentro de Zellij, ou usar `zellij --session <nome> action ...` (verificar sintaxe na versão atual).

  2. **vim-zellij-navigator não navega "atravessa" — só dentro do Neovim**
     - **Causa:** plugin Zellij não instalado/configurado (só metade da bridge presente).
     - **Sintoma:** Ctrl-l no Neovim com split à direita move pra split; sem split, não vai pro pane Zellij.
     - **Como detectar:** ler logs Zellij + testar.
     - **Solução:** instalar plugin Zellij contraparte (geralmente no layout via `plugin location=...`).

  3. **Focus events não disparam em alguns emuladores**
     - **Causa:** terminal não envia escape sequence; ou Zellij não propaga.
     - **Sintoma:** `FocusGained` nunca dispara.
     - **Como detectar:** `:autocmd FocusGained` mostra registrado mas não dispara.
     - **Solução:** testar com emulador moderno (kitty, wezterm, foot, alacritty); verificar terminal envia (`infocmp -L`).

  4. **`write-chars` com escapes literais**
     - **Causa:** shell expande `\n` antes de passar; ou contrário, não expande.
     - **Sintoma:** texto literal `\n` aparece na pane em vez de newline.
     - **Como detectar:** olhar output.
     - **Solução:** usar `$'\n'` (ANSI-C quoting) ou `printf` com `%b`; ou `zellij action send-keys "Enter"` (verificar sintaxe).

  5. **Plugin Neovim de status pra zjstatus polui logs**
     - **Causa:** envio sync de status (autocmd em CursorMoved) chama `zellij action pipe` 100x/segundo.
     - **Sintoma:** Zellij lento; logs gigantes.
     - **Como detectar:** `du -sh ~/.cache/zellij/`.
     - **Solução:** debounce no Neovim (vim.defer_fn); ou trigger só em eventos esparsos (BufEnter, ModeChanged).

- **Em inglês:** focus event (focus event); navigator (navigator); bridge (bridge); orchestrate (orchestrate); send keys (send keys); pipe (pipe); autocmd (autocmd); split (split); pane (pane); escape sequence (escape sequence).

- **Veja também:**
  - `[[06 - Modos avançados, plugins e copy-mode]]` — Pipe API e arquitetura plugin
  - `[[05 - Layouts declarativos em KDL]]` — onde plugin Zellij é referenciado
  - `[[03-Dominios/Terminal/Editor/index|Editor (Neovim)]]` — galho 1, tudo sobre Neovim
  - `[[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]`
  - `[[03-Dominios/Terminal/index|Trilha Terminal]]`
  - `[[Dicionário do Terminal#Plugin (Zellij)|plugin]]`, `[[Dicionário do Terminal#Pipe API|pipe API]]`

- **Referências:**
  - vim-zellij-navigator: https://github.com/hiasr/vim-zellij-navigator
  - Zellij — CLI: https://zellij.dev/documentation/cli

- [ ] **Step 4: Validar**

```bash
test -f "03-Dominios/Terminal/Multiplexer/07 - Integração com Neovim e shell.md"
grep -c '\[\[' "03-Dominios/Terminal/Multiplexer/07 - Integração com Neovim e shell.md"
```

Esperado: arquivo existe, ≥7 wikilinks (sem novos verbetes desta vez).

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/07 - Integração com Neovim e shell.md"
git commit -m "feat(terminal-multiplexer): add nota 07 — Integração com Neovim e shell"
```

---

## ✅ Checkpoint Magus

Após Task 9, todas as 7 notas escritas.

```bash
ls -1 "03-Dominios/Terminal/Multiplexer/" | sort
```

Esperado: 7 notas + `index.md`.

---

## Task 10: Pass final no MOC do galho

**Files:**
- Modify: `03-Dominios/Terminal/Multiplexer/index.md`

**Objetivo:** trocar `<VERSAO_ZELLIJ>` pelo valor real capturado no Task 0; confirmar wikilinks ativos.

- [ ] **Step 1: Substituir placeholder de versão**

Use `Edit` em `Multiplexer/index.md`:

`old_string`:
```markdown
- **Zellij:** `<VERSAO_ZELLIJ>` (capturada no pré-flight)
```

`new_string` (substitua `<VERSAO_REAL>` pelo valor capturado em Task 0):
```markdown
- **Zellij:** `<VERSAO_REAL>`
```

Exemplo se Zellij 0.41.2:
```markdown
- **Zellij:** 0.41.2
```

Se Zellij não estava instalado no Task 0, usar:
```markdown
- **Zellij:** 0.41+ (notas pesquisadas em docs oficiais; instalação assumida >= 0.41)
```

- [ ] **Step 2: Confirmar wikilinks ativos**

```bash
for n in "01 - Zellij vs tmux vs screen" "02 - Modelo mental — sessions, tabs, panes" "03 - Modos básicos e keybindings essenciais" "04 - Sessões persistentes — detach, attach, gerenciamento" "05 - Layouts declarativos em KDL" "06 - Modos avançados, plugins e copy-mode" "07 - Integração com Neovim e shell"; do
  test -f "03-Dominios/Terminal/Multiplexer/${n}.md" && echo "ok: $n" || echo "FALTA: $n"
done
```

Esperado: 7 linhas `ok:`.

- [ ] **Step 3: Atualizar `updated:` do MOC se necessário**

Se `updated: 2026-05-21` já está correto, sem mudança. Senão, Edit.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Multiplexer/index.md"
git commit -m "$(cat <<'EOF'
docs(terminal-multiplexer): pass final no MOC do galho

Substitui placeholder de versão Zellij pelo valor real capturado no
pré-flight. Confirma que todos os 7 wikilinks de notas estão ativos.
EOF
)"
```

---

## Task 11: Pass final no Dicionário do Terminal

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md`

**Objetivo:** garantir ordem alfabética dentro do bloco `## Multiplexer / Zellij`; cada verbete tem "Veja também"; contagem ≥15.

- [ ] **Step 1: Listar verbetes do bloco em ordem**

```bash
awk '/^## Multiplexer \/ Zellij$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Verbetes esperados (16) em ordem alfabética case-insensitive:
1. Attach
2. Detach
3. Floating pane
4. KDL
5. Layout (Zellij)
6. Locked mode
7. Mode (Zellij)
8. Multiplexer
9. Pane
10. Pipe API
11. Plugin (Zellij)
12. Session (Zellij)
13. Stacked pane
14. Status bar
15. Tab (Zellij)
16. Tmux compat mode

- [ ] **Step 2: Reordenar se necessário**

Se algum verbete estiver fora de ordem, use Edit pra mover o bloco inteiro (5 linhas: `### Nome` + def + linha vazia + `Veja também:` + linha vazia) pra posição correta.

- [ ] **Step 3: Confirmar "Veja também" em cada verbete**

```bash
awk '/^## Multiplexer \/ Zellij$/{f=1; next} /^## /{f=0}
     f && /^### / { v=$0; getline; getline; while(NF==0) getline; if ($0 !~ /^Veja também:/) print v " — sem Veja também" }' \
  "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: nenhum output. Se houver, adicionar "Veja também: ..." apontando pra nota canônica.

- [ ] **Step 4: Contagem**

```bash
awk '/^## Multiplexer \/ Zellij$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md" | wc -l
```

Esperado: 16.

- [ ] **Step 5: Atualizar `updated:` se necessário**

Já está `2026-05-21` (do Task 2 ou notas). Confirmar.

- [ ] **Step 6: Commit (se houve reordenação ou fix)**

```bash
git status --short "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Se modificado:
```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "$(cat <<'EOF'
docs(terminal): pass final no Dicionário (bloco Multiplexer / Zellij)

Garante ordem alfabética case-insensitive no bloco Multiplexer/Zellij;
cada verbete tem Veja também. Contagem final: 16 verbetes novos.
EOF
)"
```

Se sem mudanças, pular commit.

---

## Task 12: Atualizar tronco — ativar wikilink do Multiplexer

**Files:**
- Modify: `03-Dominios/Terminal/index.md`

**Objetivo:** trocar `- Multiplexer — galho 3 (planejado): Zellij` por wikilink ativo.

- [ ] **Step 1: Edit do tronco**

`old_string`:
```markdown
- Multiplexer — galho 3 (planejado): Zellij
```

`new_string`:
```markdown
- [[03-Dominios/Terminal/Multiplexer/index|Multiplexer]] — galho 3: Zellij (sessions, layouts KDL, plugins WASM)
```

- [ ] **Step 2: Atualizar `updated:` do tronco pra `2026-05-21`**

Edit do frontmatter.

- [ ] **Step 3: Confirmar mudança**

```bash
grep -n "Multiplexer" "03-Dominios/Terminal/index.md"
```

Esperado: wikilink ativo aparece; `(planejado)` desaparece.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/index.md"
git commit -m "$(cat <<'EOF'
feat(terminal): tronco com wikilink ativo pro galho 3 (Multiplexer)

Substitui bullet "Multiplexer (planejado)" por wikilink ativo
[[03-Dominios/Terminal/Multiplexer/index|Multiplexer]] após entrega do galho 3.
EOF
)"
```

---

## Task 13: Validação final

**Files:**
- (nenhum — só validação)

**Objetivo:** rodar `verificar-wikilinks` na pasta Multiplexer/ + sanity checks gerais.

- [ ] **Step 1: Verificar wikilinks**

```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py \
  "03-Dominios/Terminal/Multiplexer/" --respect-public-only
```

Lê o JSON gerado em `/tmp/wikilinks-report-*.json`. Esperado: `links_broken: 0`.

Se houver broken links, corrigir antes de declarar galho fechado.

- [ ] **Step 2: Sanity check geral**

```bash
ls -1 "03-Dominios/Terminal/Multiplexer/" | sort
git log --oneline | head -15
git log --format="%H %s" -15 | grep -i "co-authored" || echo "ok: nenhum commit com Co-Authored-By"
```

Esperado:
- 8 arquivos em Multiplexer/ (7 notas + index)
- ~13-15 commits do galho
- Nenhum Co-Authored-By

- [ ] **Step 3: Contagem final do Dicionário**

```bash
awk '/^## Multiplexer \/ Zellij$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md" | wc -l
```

Esperado: 16.

- [ ] **Step 4: Smoke test de leitura cruzada**

Abrir 1 nota Magus (06 ou 07) e seguir 2 wikilinks (pra MOC e pra outra nota). Confirmar que abrem corretamente.

(Manualmente no editor.)

- [ ] **Step 5: Declarar galho fechado**

Reporte ao usuário:
- 7 notas + MOC entregues
- 16 verbetes no Dicionário
- Tronco com wikilink ativo
- Zero wikilinks broken
- Zero commits com Co-Authored-By
- Próximo galho (4 — TUIs de Dev) quando o usuário quiser

---

## Self-review do plano

**Spec coverage:** todas as seções 3.1-3.4, 4.1-4.3, 5 do spec → tarefas atribuídas. Critério de pronto da seção 8 → coberto em Tasks 10-13.

**Placeholder scan:** verifiquei. As únicas variáveis ("substitua `<VERSAO_REAL>`", "Sugestão inicial: confirmar verificado no Step 1") são intencionais e o subagent recebe instrução clara pra resolver.

**Type consistency:** nomes de arquivos consistentes entre Tasks 1, 4, 5, 6, 10. Verbetes consistentes entre Tasks 3-9 e Task 11.

**Cobertura cross-galho:** Task 9 (nota 07) referencia galho 1 (Editor) via wikilink ao MOC dele — verificado que `03-Dominios/Terminal/Editor/index.md` existe.

Pronto pra execução.
