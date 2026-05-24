# Galho 7 — Workflow — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar o galho 7 e final da trilha Terminal — 10 notas atômicas (3 Iniciado + 4 Adepto + 3 Magus) em `03-Dominios/Terminal/Workflow/`, MOC do galho, expansão do Dicionário com bloco `## Workflow`, ativação do wikilink no tronco e fechamento da trilha (`progresso: completo`). 5 playbooks que recombinam galhos 1-6 + 4 meta-práticas + 1 capstone híbrido sintetizando a trilha.

**Architecture:** Mesmo padrão consolidado nos galhos 2-6. Estrutura H2 fixa pras notas 01-09; estrutura diferente pro capstone (10) que NÃO re-explica e compõe via cenário cronológico + fluxo + decisões em bifurcações. Tom pedagógico mas assume galhos 1-6 dominados. Exemplos sempre neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos. Fluxo SDD: implementer → reviewer combinado → fix se Critical/Important.

**Tech Stack:** Obsidian + Quartz, Markdown + frontmatter YAML, wikilinks. Ferramentas-alvo das receitas: gh CLI, git worktree, Zellij named sessions, lazygit, delta, Neovim quickfix/LSP/Telescope, rg, fzf, zoxide, eza, bat, atuin.

---

## Spec de referência

`docs/superpowers/specs/2026-05-24-terminal-workflow-design.md`

## Restrições absolutas (em TODOS os subagent prompts)

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `myproj`, `<user>`) ou hipotéticos explícitos (`# hipotético: ...`). NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de comandos/flags. Verificar via doc oficial.
3. **Sem `Co-Authored-By: Claude`**. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em `## Veja também`.
6. **Tronco wikilink obrigatório**: `[[03-Dominios/Terminal/index|Trilha Terminal]]`.
7. **MOC wikilink** em "Veja também": `[[03-Dominios/Terminal/Workflow/index|MOC do galho]]`.
8. **≥4 armadilhas** por nota regular (01-09), cada uma com 4 labels (Causa / Sintoma / Como detectar / Solução). Capstone (10) tem padrão diferente: ≥5 decisões em bifurcações.
9. **"Em inglês" em bullets bilíngues** `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
10. **Code fences corretos:** `bash` pra shell, `yaml`/`toml`/`kdl` pra config, `text` pra ASCII.
11. **Tom pedagógico** mas assume galhos 1-6. Não re-explica nvim, Zellij, lazygit, rg, etc. — referencia via wikilink.
12. **Sem hype keyboard-first.** Honesto sobre limites. Comparar com GUI/web quando apropriado.
13. **Capstone (10) NÃO re-explica.** Compõe. Tese-em-ato.
14. **`git add <path>` explícito.** NUNCA `git add -A`.
15. **Subagent dispatches em Sonnet com contexto curto.** 1M context dá erro de créditos — não usar.

---

## Task 0: Pré-flight

**Files:**
- (nenhum — só captura de versões)

- [ ] **Step 1: Capturar versões das ferramentas-alvo**

```bash
gh --version 2>&1 | head -1 || echo "(gh não instalado)"
echo "---"
git --version
echo "---"
git worktree --help 2>&1 | head -3 || echo "(git worktree indisponível)"
echo "---"
zellij --version 2>&1 || echo "(zellij não instalado)"
echo "---"
lazygit --version 2>&1 || echo "(lazygit não instalado)"
echo "---"
nvim --version 2>&1 | head -1 || echo "(nvim não instalado)"
echo "---"
uname -a
echo "---"
cat /etc/os-release 2>&1 | head -5
```

Anotar versões pra usar nas notas e MOC (Task 11).

- [ ] **Step 2: Verificar pasta destino**

```bash
ls -la "03-Dominios/Terminal/" 2>&1 | head -20
test -d "03-Dominios/Terminal/Workflow" && echo "JÁ EXISTE — abortar" || echo "ok, pasta nova"
```

Esperado: pasta `Workflow/` ainda não existe.

- [ ] **Step 3: Verificar tronco e dicionário**

```bash
grep -n "Workflow" "03-Dominios/Terminal/index.md"
grep -E "^## " "03-Dominios/Terminal/Dicionário do Terminal.md" | head -20
```

Esperado: tronco tem bullet `Workflow — galho 7 (planejado)` (linha 33); dicionário tem blocos por galho (Editor, Shell, Multiplexer, TUIs, Dotfiles, CLI Utils) mas NÃO tem ainda bloco Workflow.

- [ ] **Step 4: Criar pasta**

```bash
mkdir -p "03-Dominios/Terminal/Workflow"
ls -la "03-Dominios/Terminal/Workflow"
```

Esperado: pasta vazia criada.

- [ ] **Step 5: Commit (pasta vazia + decisão registrada)**

Não há nada pra commitar ainda — pasta vazia não é versionada por git. Pular.

---

## Task 1: Dicionário — bloco "Workflow" esqueleto

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Localizar onde inserir**

```bash
grep -n "^## " "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Identificar último bloco H2 (último galho — CLI Utils). Inserir `## Workflow` depois dele e antes de eventuais seções finais (## Veja também, ## Referências).

- [ ] **Step 2: Adicionar bloco esqueleto**

Inserir após o último bloco H2 de galho:

```markdown

## Workflow

<!-- Verbetes preenchidos task a task durante implementação do galho 7. -->

```

E bump `updated:` no frontmatter pra `2026-05-24`.

- [ ] **Step 3: Validar**

```bash
grep -E "^## Workflow$" "03-Dominios/Terminal/Dicionário do Terminal.md"
grep "^updated:" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: bloco existe; `updated: 2026-05-24`.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): bloco 'Workflow' no Dicionário (esqueleto)"
```

---

## Task 2: Nota 01 — Filosofia keyboard-first: quando vale e quando NÃO

**Files:**
- Create: `03-Dominios/Terminal/Workflow/01 - Filosofia keyboard-first — quando vale e quando não.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: keyboard-first, RSI)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://en.wikipedia.org/wiki/Modal_editor
WebFetch: https://www.gnu.org/software/emacs/manual/html_node/efaq/RSI.html
```

Capturar: origem do conceito keyboard-first, RSI básico, contraste com mouse-first.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Filosofia keyboard-first — quando vale e quando NÃO"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - workflow
  - iniciado
  - keyboard-first
aliases:
  - Keyboard-first
  - Filosofia keyboard-first
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR (callout `[!abstract]`):**
"Keyboard-first é prioritizar teclado pra navegação/edição/comando. Vale pra texto, código, busca, navegação repetitiva — onde gestos do mouse são imprecisos. NÃO vale onde a tarefa é intrinsecamente visual: graphics, ER design, exploração de canvas, layout. Custo de aprendizado é real (semanas/meses); ganho aparece em consistência e ergonomia (menos RSI), não em velocidade pura."

**O que é / Como funciona** (H3s):

### O que é keyboard-first
- Modelo onde teclado é primário pra todas as operações; mouse é opcional/secundário
- Não é "sem mouse" — é "mouse opcional"
- Vem de tradição Unix + editores modais (vi/Emacs)

### Princípios
- Atalhos hierárquicos (leader keys, prefix keys)
- Modos vs modelos (modal editor: Normal/Insert/Visual; tmux: prefix + key)
- Consistência cross-tool (Vim grammar em nvim, less, bat, zsh vi-mode)
- Pequenos gestos, alta frequência (toda movimentação é "barata")

### Quando keyboard-first compensa
- Texto e código (todo o domínio dev)
- Navegação repetitiva (mesmas pastas, mesmas operações)
- Composição (encadear comandos no shell)
- Operações reversíveis (testar é barato)

### Quando NÃO compensa
- Graphics/design ferramental visual (Figma, Photoshop)
- ER diagrams, diagramas de arquitetura desenhados à mão
- Browsing de catálogos visuais (e-commerce, galerias)
- Mídia exploratória (vídeo, áudio com timeline)
- Onde gestos contínuos > saltos discretos

### Custo real
- Curva: semanas pra modal editing virar segunda natureza
- Customização: configs que envelhecem mal, manutenção
- Lock-in cognitivo: difícil voltar quando colaborar com não-praticantes
- RSI invertido: postura ruim de teclado pode causar dor também

**Na prática** (H3s):

### Auto-teste honesto: vale pra você?
- 80%+ do seu dia é texto/código? Provavelmente sim
- Você muda de máquina com frequência? Inverte custo (cada máquina precisa setup)
- Você tem deadline em 2 semanas? Espere, não migre agora
- Você sente fadiga no pulso/cotovelo? Sim → benefício além de velocidade

### Como NÃO entrar errado
- NÃO copie config de senior dev e force adoção
- NÃO desabilite mouse "pra forçar aprendizado"
- NÃO meça progresso em "comandos por minuto"
- SIM aprenda um atalho por dia
- SIM mantenha mouse à mão pros casos onde compensa

### Caminho mínimo viável
- Dia 1: ler [[03-Dominios/Terminal/Editor/01 - Modal editing|modal editing]] e instalar Neovim
- Semana 1-2: hjkl, modes, telescope
- Mês 1: rg + fzf no shell, leader keys, prefix Zellij
- Mês 2+: customização própria, scripts

**Armadilhas (≥4):**

1. **"Keyboard-first é mais rápido" como argumento principal**
   - **Causa:** vídeos de demo medem em segundos por tarefa.
   - **Sintoma:** desânimo após 2 semanas — você ainda é mais lento que no IDE.
   - **Como detectar:** comparar tempo de tasks reais (não micro-benchmarks).
   - **Solução:** lembrar que ganho real é consistência (menos contexto-switch entre tools) e ergonomia, não velocidade pura. Velocidade aparece após meses.

2. **Forçar adoção 100% em todas as tarefas**
   - **Causa:** purismo doutrinário ("se uso mouse, falhei").
   - **Sintoma:** frustração em tasks visuais (Figma, Excel grande, browsing) que SERIAM mais fáceis com mouse.
   - **Como detectar:** se você gasta >2x o tempo de antes em uma tarefa específica, é sinal.
   - **Solução:** keyboard-first é prioridade, não dogma. Mouse pra graphics, browsing visual, drag-drop intencional.

3. **Customizar tudo antes de aprender o default**
   - **Causa:** ansiedade de "deixar do seu jeito" antes de saber qual é o jeito.
   - **Sintoma:** configs gigantes que você não lembra por que escreveu.
   - **Como detectar:** abrir config e perguntar "por que isso?" pra cada linha.
   - **Solução:** usar default por 2-4 semanas. Customizar SÓ atalhos que você usa 10+ vezes/dia e o default machuca.

4. **Ignorar RSI até doer**
   - **Causa:** "ainda não dói, então tá ok".
   - **Sintoma:** dor no pulso/cotovelo aparece subitamente após meses.
   - **Como detectar:** sentir qualquer tensão no pulso depois de 1h digitando = sinal.
   - **Solução:** pausas (técnica Pomodoro), alongamentos, keyboard ergonômico (split, ortolinear), CapsLock→Ctrl pra evitar contorção da mão esquerda.

5. **Esperar que keyboard-first salve produtividade de problemas estruturais**
   - **Causa:** querer atalho técnico pra problema organizacional.
   - **Sintoma:** "se eu aprendesse vim direito, entregaria 2x mais tasks".
   - **Como detectar:** sua bottleneck é digitação ou é decidir o quê implementar/discutir?
   - **Solução:** keyboard-first amplifica produtividade existente, não substitui processo, design ou foco.

**Em inglês (8-10 bullets bilíngues):**
Termos: keyboard-first, modal editing, leader key, mouse-first, RSI, ergonomics, prefix key, muscle memory, learning curve, lock-in. Formato `- **PT** — *EN*. "frase em PT."`.

**Veja também:**
- [[02 - Anatomia da sessão de trabalho]]
- [[06 - Ergonomia das mãos]]
- [[03-Dominios/Terminal/Editor/01 - Modal editing|Modal editing (galho 1)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#keyboard-first|keyboard-first]]
- [[Dicionário do Terminal#RSI|RSI]]

**Referências:**
- Modal editor (Wikipedia): https://en.wikipedia.org/wiki/Modal_editor
- Emacs FAQ — RSI: https://www.gnu.org/software/emacs/manual/html_node/efaq/RSI.html

- [ ] **Step 4: 2 verbetes pro Dicionário**

Inserir em ordem alfabética no bloco `## Workflow`:

```markdown
### keyboard-first
Modelo de interação onde teclado é primário pra navegação/edição/comando; mouse é opcional. Origem em editores modais (vi/Emacs) e tradição Unix. Vale pra texto/código/navegação repetitiva; não vale pra graphics, ER design, browsing visual. Ganho real é consistência e ergonomia, não velocidade pura.

Veja também: [[01 - Filosofia keyboard-first — quando vale e quando não]].

### RSI
Repetitive Strain Injury — lesão por esforço repetitivo, comum em devs por digitação intensa. Manifestações: dor/formigamento em pulso, cotovelo, antebraço. Prevenção: pausas, alongamentos, postura, teclado ergonômico, CapsLock→Ctrl. Ignorar até doer é a armadilha clássica.

Veja também: [[06 - Ergonomia das mãos]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/01 - Filosofia keyboard-first — quando vale e quando não.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/01 - Filosofia keyboard-first — quando vale e quando não.md"
grep -E "^### keyboard-first$" "03-Dominios/Terminal/Dicionário do Terminal.md"
grep -E "^### RSI$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥7 wikilinks; verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/01 - Filosofia keyboard-first — quando vale e quando não.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 01 — Filosofia keyboard-first"
```

---

## Task 3: Nota 02 — Anatomia da sessão de trabalho

**Files:**
- Create: `03-Dominios/Terminal/Workflow/02 - Anatomia da sessão de trabalho.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: ephemeral session, named session, focus mode, sessão de trabalho)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zellij.dev/documentation/sessions
WebFetch: https://zellij.dev/documentation/layouts
```

Capturar: vocabulário oficial (session, tab, pane, layout), modo focus do Zellij.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Anatomia da sessão de trabalho"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - workflow
  - iniciado
  - sessao
aliases:
  - Anatomia da sessão
  - Sessão de trabalho
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Sessão de trabalho = container persistente de tabs/panes/processos. Vocabulário: session (root), tab (área visível), pane (split dentro de tab), layout (config declarativa de tabs+panes). Zellij/tmux atuam como window manager do terminal. Modelos mentais: sessão = projeto OU sessão = task. Sessions efêmeras (descartáveis) vs persistentes (nomeadas, sobrevivem reboot)."

**O que é / Como funciona** (H3s):

### Sessão, tab, pane, layout — vocabulário
- **Session:** raiz; container de tabs. Tem nome (ou ID anônimo). Persiste após detach.
- **Tab:** área visível única; um tab por vez é renderizado.
- **Pane:** split dentro de tab; múltiplos panes simultâneos.
- **Layout:** declaração de tabs+panes; reproduz estrutura ao abrir.

### Window manager mental model
- Zellij/tmux = window manager pra terminal (gerencia janelas dentro do emulator)
- Por que importa: 1 terminal hospedeiro pode rodar N sessões; cada sessão é seu próprio "workspace"
- Permite múltiplas máquinas (SSH) compartilharem sessões

### Sessions efêmeras vs persistentes
- **Efêmera:** sem nome (ID anônimo); some no detach final ou kill. Use pra one-shot tasks (testar comando, debug rápido).
- **Persistente (named):** com nome humano (`zellij -s projeto`). Sobrevive desconexão SSH, sleep do laptop, exit do emulator. Use pra projeto contínuo.

### Modelos de organização
- **Sessão = projeto:** uma sessão por repo/cliente. Tabs por contexto (code, server, tests). Bom pra trabalho contínuo.
- **Sessão = task:** uma sessão por feature/bug. Worktree-friendly. Bom pra multi-task.
- **Sessão = papel:** uma sessão por papel (dev, ops, review). Menos comum.

### Modo focus
- Esconde UI auxiliar (status bar, tabs bar) pra maximizar área de código
- Zellij: Alt-f (no default config). tmux: equivalente é `set status off`
- Útil em pair-programming, screencast, deep work

**Na prática** (H3s):

### Comandos básicos Zellij
```bash
zellij                        # nova sessão efêmera
zellij -s projeto             # sessão nomeada "projeto"
zellij ls                     # listar sessões ativas
zellij a projeto              # attach na sessão "projeto"
zellij a -c projeto           # attach OU cria se não existe
zellij d                      # detach da sessão atual
zellij k projeto              # kill sessão "projeto"
```

### Quantos tabs e panes saudáveis
- 3-5 tabs por sessão: legível, navegável com leader+number
- 2-4 panes por tab: além disso vira poluição visual
- Cada pane = um processo persistente (não rodar comandos one-shot em pane separado)

### Escolher modelo (projeto vs task)
- Trabalho longo em monorepo grande? Sessão por projeto, tabs por subsistema.
- Múltiplas features em paralelo? Sessão por feature (com worktrees — ver nota 07).
- Job intensa de pesquisa exploratória? Sessão efêmera.

**Armadilhas (≥4):**

1. **Confundir sessão com tab/pane no vocabulário**
   - **Causa:** tmux/Zellij usam termos similares; iniciante chama tab de "janela".
   - **Sintoma:** docs/forums confundem; comandos não funcionam como esperado.
   - **Como detectar:** ler `zellij --help` ou `man tmux`; checar nomenclatura oficial.
   - **Solução:** memorizar session > tab > pane. Esquema mental: session é raiz; tab é área visível; pane é split dentro de tab.

2. **Acumular sessões persistentes "esquecidas"**
   - **Causa:** detach por costume; nunca volta a olhar `zellij ls`.
   - **Sintoma:** 15 sessões zombies consumindo RAM; nomes que você não lembra do que são.
   - **Como detectar:** `zellij ls` semanal.
   - **Solução:** higiene weekly: `zellij ls` + kill sessões inativas há +7 dias.

3. **Sessão efêmera pra trabalho que vai durar dias**
   - **Causa:** começar com `zellij` sem `-s`; perde tudo no reboot do laptop.
   - **Sintoma:** segunda-feira de manhã o estado de sexta sumiu.
   - **Como detectar:** notar que cada Monday você reabre os mesmos tabs.
   - **Solução:** se você vai voltar ao trabalho amanhã, USE `-s nome`. Hábito de nomear desde o início.

4. **Layout KDL gigante que reproduz tudo perfeitamente**
   - **Causa:** querer "setup completo num comando".
   - **Sintoma:** layout vira fonte de bugs; mudar uma coisa quebra tudo.
   - **Como detectar:** seu layout tem 50+ linhas com lógica condicional.
   - **Solução:** layout mínimo (3-4 tabs, sem comandos auto-start). Open manual é ok.

**Em inglês (8-10 bullets bilíngues):**
Termos: session, tab, pane, layout, attach, detach, focus mode, window manager, ephemeral, persistent. Formato bilíngue.

**Veja também:**
- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[04 - Setup matinal e tear-down]]
- [[07 - Worktrees + Zellij paralelos]]
- [[03-Dominios/Terminal/Multiplexer/02 - Modelo mental — sessions, tabs, panes|Modelo mental Multiplexer]]
- [[03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes|Sessões persistentes (galho 3)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#named session|named session]]
- [[Dicionário do Terminal#ephemeral session|ephemeral session]]
- [[Dicionário do Terminal#focus mode|focus mode]]
- [[Dicionário do Terminal#sessão de trabalho|sessão de trabalho]]

**Referências:**
- Zellij sessions: https://zellij.dev/documentation/sessions
- Zellij layouts: https://zellij.dev/documentation/layouts

- [ ] **Step 4: Verbetes pro Dicionário**

Inserir em ordem alfabética no bloco `## Workflow`:

```markdown
### ephemeral session
Sessão Zellij/tmux sem nome (ID anônimo) que some ao detach final ou kill. Use pra one-shot tasks; pra trabalho contínuo prefira [[Dicionário do Terminal#named session|named session]].

Veja também: [[02 - Anatomia da sessão de trabalho]].

### focus mode
Modo do Zellij/tmux que esconde UI auxiliar (status bar, tabs bar) pra maximizar área de código. Útil em deep work, pair-programming, screencast.

Veja também: [[02 - Anatomia da sessão de trabalho]].

### named session
Sessão Zellij/tmux com nome humano (`zellij -s projeto`) que sobrevive desconexão SSH, sleep, exit do emulator. Use pra projeto contínuo. Oposto de [[Dicionário do Terminal#ephemeral session|ephemeral session]].

Veja também: [[02 - Anatomia da sessão de trabalho]], [[04 - Setup matinal e tear-down]].

### sessão de trabalho
Container persistente de tabs/panes/processos no terminal. Composta por: session (raiz) > tabs (áreas visíveis) > panes (splits dentro de tab) + layout opcional. Zellij/tmux atuam como window manager do terminal.

Veja também: [[02 - Anatomia da sessão de trabalho]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/02 - Anatomia da sessão de trabalho.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/02 - Anatomia da sessão de trabalho.md"
grep -E "^### named session$" "03-Dominios/Terminal/Dicionário do Terminal.md"
grep -E "^### focus mode$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥10 wikilinks; 4 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/02 - Anatomia da sessão de trabalho.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 02 — Anatomia da sessão"
```

---

## Task 4: Nota 03 — Onboarding em projeto novo

**Files:**
- Create: `03-Dominios/Terminal/Workflow/03 - Onboarding em projeto novo.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (sem verbete novo — é playbook que reusa termos)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://www.gnu.org/software/coreutils/manual/html_node/index.html (find, head, tail)
```

Capturar: comandos exploratórios básicos. As ferramentas-alvo (zoxide, eza, rg, bat, telescope) já têm notas próprias nos galhos 1-6 — não pesquisar de novo.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Onboarding em projeto novo"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - workflow
  - iniciado
  - onboarding
  - playbook
aliases:
  - Onboarding projeto novo
  - Onboarding playbook
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Playbook: chegar em repo desconhecido → mapa mental em 30min. Fluxo: clone+cd (zoxide aprende) → eza --tree pra ver estrutura → rg \"TODO|FIXME\" + cat README → telescope live_grep pra entender entry points → lazygit log pra contexto recente. Anota perguntas em scratch; não tenta entender tudo na primeira passada."

**O que é / Como funciona** (H3s):

### Por que onboarding merece playbook
- Tendência ruim: abrir IDE, perder-se em árvore de arquivos por horas
- Tendência melhor: bater o terreno com ferramentas exploratórias rápidas
- 30min focados > 3h dispersos

### Fluxo macro
- **Fase 1 (5min):** chegar e clarear contexto (README, ESTRUTURA)
- **Fase 2 (10min):** entry points e fluxos críticos
- **Fase 3 (10min):** history recente (o que mudou semana passada?)
- **Fase 4 (5min):** anotar perguntas pra time/docs

### O que você quer no fim dos 30min
- Saber qual diretório tem entry point
- Saber linguagem(ns) e framework(s) principais
- Saber 2-3 fluxos críticos do negócio
- Lista de 5-10 perguntas pra próxima conversa

**Na prática** (H3s):

### Receita completa (30min)

```bash
# Fase 1 — Contexto (5min)
cd ~/repos/<projeto>           # zoxide aprende
eza --tree -L 2 --git-ignore   # estrutura macro (galho 6)
bat README.md                  # leitura rápida com syntax (galho 6)
bat CONTRIBUTING.md 2>/dev/null # opcional
ls -la docs/ 2>/dev/null       # docs internas?

# Fase 2 — Entry points (10min)
rg "main\|entry\|bootstrap" -t lua -t js -t py -t go | head -20
rg "TODO\|FIXME\|XXX" --stats | head
# No nvim:
nvim
# :Telescope find_files
# :Telescope live_grep "config\|database\|main"

# Fase 3 — History (10min)
lazygit
# log: ler últimos 20 commits, ver branches ativos
# Q pra sair
git log --oneline --all --decorate -20

# Fase 4 — Anotar perguntas (5min)
nvim ~/scratch/<projeto>.md
# Lista: arquitetura, deps externas, testing strategy, deploy pipeline
```

### Adapt to repo size
- Repo pequeno (<10k linhas): pula Fase 3 — leia código direto
- Repo grande (>500k linhas): foca em UM submódulo na Fase 2; Fase 3 vira "history só desse módulo"
- Monorepo: Fase 1 inclui mapear quais packages/apps existem

### Sinais ruins (volte pra README ou pergunte ao time)
- Não encontrou entry point óbvio em 10min
- README desatualizado (último commit 2 anos atrás)
- Build/test scripts ausentes
- Dependencies file (`package.json`, `Cargo.toml`) vazio ou estranho

**Armadilhas (≥4):**

1. **Tentar entender 100% antes de tocar código**
   - **Causa:** ansiedade de "não saber o suficiente".
   - **Sintoma:** 3 dias depois ainda lendo docs sem ter rodado nada.
   - **Como detectar:** marcou 30min mas estourou pra 2h.
   - **Solução:** time-box rígido. Aos 30min, mude pra "rodar o app local" mesmo que entendendo 40%. Resto se aprende fazendo.

2. **Skip do `bat README.md` por achar README inútil**
   - **Causa:** "README sempre é trash".
   - **Sintoma:** descobre conceito básico do domínio só na semana 2.
   - **Como detectar:** se README tem 5+ linhas, vale 2min de leitura.
   - **Solução:** sempre ler README na Fase 1. Mesmo trash, dá vocabulário do time.

3. **Ignorar `lazygit log` / `git log`**
   - **Causa:** "código atual basta".
   - **Sintoma:** refactor com pressuposto errado que foi removido 2 commits atrás.
   - **Como detectar:** ler últimos 5 commit messages.
   - **Solução:** Fase 3 é obrigatória. History recente revela onde o time está pensando, não onde estava.

4. **Não anotar nada (Fase 4 esquecida)**
   - **Causa:** "vou lembrar".
   - **Sintoma:** mesmo onboarding repetido na semana seguinte; perguntas recorrentes.
   - **Como detectar:** abrir o `~/scratch/<projeto>.md` na semana 2 — vazio?
   - **Solução:** Fase 4 inegociável. Mesmo 3 bullets. Vira fonte pra retrospectiva e onboarding do próximo dev.

**Em inglês (8-10 bullets bilíngues):**
Termos: onboarding, entry point, codebase, scratch file, time-box, exploration, repository, build script, dependency, contribution guide. Formato bilíngue.

**Veja também:**
- [[02 - Anatomia da sessão de trabalho]]
- [[05 - Code review no terminal]]
- [[08 - Refactoring multi-arquivo]]
- [[03-Dominios/Terminal/Editor/04 - LazyVim — instalação, tour, navegação|LazyVim — Telescope (galho 1)]]
- [[03-Dominios/Terminal/TUIs/01 - Lazygit — overview|Lazygit overview (galho 4)]]
- [[03-Dominios/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes|ripgrep (galho 6)]]
- [[03-Dominios/Terminal/CLI Utils/04 - eza — ls moderno|eza (galho 6)]]
- [[03-Dominios/Terminal/CLI Utils/05 - zoxide — cd inteligente com frecency|zoxide (galho 6)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]

**Referências:**
- (sem refs externas; é playbook que compõe galhos 1-6)

- [ ] **Step 4: Sem verbetes novos**

Esta nota NÃO adiciona verbetes ao Dicionário — playbook reusa termos já definidos.

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/03 - Onboarding em projeto novo.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/03 - Onboarding em projeto novo.md"
```

Esperado: arquivo existe; ≥10 wikilinks.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/03 - Onboarding em projeto novo.md"
git commit -m "feat(terminal-workflow): add nota 03 — Onboarding em projeto novo"
```

---

## Task 5: Nota 04 — Setup matinal e tear-down

**Files:**
- Create: `03-Dominios/Terminal/Workflow/04 - Setup matinal e tear-down.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: tear-down)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://zellij.dev/documentation/layouts
WebFetch: https://zellij.dev/documentation/commands
```

Capturar: comandos de attach/detach, layout KDL com command auto-start.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Setup matinal e tear-down"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - workflow
  - adepto
  - sessao
  - playbook
aliases:
  - Setup matinal
  - Tear-down
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Playbook: abrir o dia (setup matinal) e fechar o dia (tear-down) com sessões nomeadas Zellij. Setup: `zellij a -c projeto` com layout KDL → atuin import → lazygit em tab dedicada. Tear-down: `zellij d` (preserva estado) vs `zellij k` (descarte intencional). Hábito de ritual reduz fricção e perda de contexto entre dias."

**O que é / Como funciona** (H3s):

### Por que ritualizar
- Reduz decisões repetitivas (`onde abro o quê?`)
- Preserva contexto entre dias
- Sinal psicológico de início/fim de trabalho

### Setup matinal: passos
- Iniciar sessão nomeada (cria se não existe)
- Restore layout (se persistido) ou abrir manual
- Sync de history (atuin) entre máquinas
- Abrir lazygit em tab dedicada (status do repo)
- Foco em tab principal (nvim)

### Tear-down: passos
- Decidir: continuar amanhã (detach) ou descartar (kill)
- Detach: `zellij d` — preserva tudo
- Kill explícito: `zellij k <nome>` — limpa intencional
- Atuin sync final (se múltiplas máquinas)

### Detach vs kill
- **Detach (`d`):** processos continuam rodando em background; sessão sobrevive logout. Use 90% do tempo.
- **Kill (`k`):** processos morrem; sessão removida. Use quando: feature merged, projeto pausado, ou limpeza weekly.

**Na prática** (H3s):

### Layout KDL mínimo (`~/.config/zellij/layouts/projeto.kdl`)

```kdl
layout {
    default_tab_template {
        pane size=1 borderless=true {
            plugin location="zellij:tab-bar"
        }
        children
        pane size=2 borderless=true {
            plugin location="zellij:status-bar"
        }
    }

    tab name="code" focus=true {
        pane
    }

    tab name="git" {
        pane command="lazygit"
    }

    tab name="server" {
        pane
    }
}
```

### Setup matinal — receita

```bash
# Função no ~/.zshrc
work() {
    local proj="$1"
    cd "$(zoxide query "$proj")" || return 1
    zellij a -c "$proj" options --default-layout projeto
}

# Uso
work meu-projeto
# Sessão "meu-projeto" abre com 3 tabs (code/git/server)
# lazygit já roda em tab "git"
```

### Tear-down — receita

```bash
# Encerrar fluindo (preserva)
# Dentro do Zellij: Ctrl-Q (ou Alt+\ no default)

# Listar sessões antes de kill
zellij ls

# Kill intencional
zellij k <nome>

# Kill todas zombies (>7 dias inativas) — script
zellij ls --no-formatting | awk '/older/ {print $1}' | xargs -I{} zellij k {}
```

### Multi-máquina (laptop + desktop)
- Atuin sync (galho 6) propaga history shell
- Sessões NÃO sincronizam — cada máquina tem suas próprias sessões
- Use convenção de nomes: `<máquina>-<projeto>` (`laptop-codex`, `desktop-codex`)

**Armadilhas (≥4):**

1. **`zellij k` num sessão com trabalho não salvo**
   - **Causa:** habito de "limpar" sem checar.
   - **Sintoma:** edits abertos em nvim somem; pano não salvo perdido.
   - **Como detectar:** `zellij ls` antes de kill; mais seguro usar `d` (detach) primeiro.
   - **Solução:** detach default. Kill SÓ após attach + verificar que não tem trabalho aberto.

2. **Layout KDL com auto-start de comandos pesados**
   - **Causa:** querer "tudo pronto em 1 comando".
   - **Sintoma:** `npm run dev` em 3 tabs simultâneo trava o laptop.
   - **Como detectar:** uso de CPU spike no boot da sessão.
   - **Solução:** layout só com nomes de tab e panes vazios. Comandos pesados são manuais.

3. **Nomes de sessão genéricos que conflitam**
   - **Causa:** sempre `zellij -s work`; semana seguinte conflita com outro projeto.
   - **Sintoma:** attach abre estado errado.
   - **Como detectar:** `zellij ls` mostra sessão `work` mas você não lembra qual é.
   - **Solução:** convenção: nome do repo (`<projeto-slug>`) ou `<projeto>-<feature>` quando paralelo.

4. **Esquecer tear-down — sessões esquecidas ocupam RAM**
   - **Causa:** sempre fechar laptop sem detach (Zellij sobrevive, mas sessões inativas crescem).
   - **Sintoma:** após meses, dezenas de sessões zombies; `top` mostra zellij com 1GB+ RAM.
   - **Como detectar:** `zellij ls` weekly.
   - **Solução:** hábito sexta-feira: `zellij ls` e kill o que não vai usar segunda.

**Em inglês (8-10 bullets bilíngues):**
Termos: setup, tear-down, ritual, attach, detach, kill, layout, auto-start, idempotent, multi-machine. Formato bilíngue.

**Veja também:**
- [[02 - Anatomia da sessão de trabalho]]
- [[07 - Worktrees + Zellij paralelos]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes|Sessões persistentes (galho 3)]]
- [[03-Dominios/Terminal/Multiplexer/05 - Layouts declarativos em KDL|Layouts KDL (galho 3)]]
- [[03-Dominios/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync|atuin (galho 6)]]
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#tear-down|tear-down]]
- [[Dicionário do Terminal#named session|named session]]

**Referências:**
- Zellij layouts: https://zellij.dev/documentation/layouts
- Zellij commands: https://zellij.dev/documentation/commands

- [ ] **Step 4: Verbete pro Dicionário**

```markdown
### tear-down
Encerramento intencional da sessão de trabalho. Decide entre detach (`zellij d`, preserva estado) e kill (`zellij k <nome>`, descarta). Hábito que reduz acúmulo de sessões zombies e perda de contexto entre dias. Oposto: setup matinal.

Veja também: [[04 - Setup matinal e tear-down]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/04 - Setup matinal e tear-down.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/04 - Setup matinal e tear-down.md"
grep -E "^### tear-down$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥10 wikilinks; verbete visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/04 - Setup matinal e tear-down.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 04 — Setup matinal e tear-down"
```

---

## Task 6: Nota 05 — Code review no terminal

**Files:**
- Create: `03-Dominios/Terminal/Workflow/05 - Code review no terminal.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: `gh CLI`, PR checkout)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://cli.github.com/manual/gh_pr_checkout
WebFetch: https://cli.github.com/manual/gh_pr_review
```

Capturar: comandos gh PR (list, checkout, review, comment), workflow review oficial GitHub.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Code review no terminal"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - workflow
  - adepto
  - code-review
  - playbook
aliases:
  - Code review terminal
  - PR review
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Playbook: review de PR sem sair do terminal. `gh pr list` + `gh pr checkout <num>` → lazygit pra ver diff por arquivo → delta como pager pra cores ricas → nvim com anotações inline. Quando voltar pra UI web: threads longas, discussions, approvals coletivos. Vantagem do terminal: edita/testa enquanto revisa."

**O que é / Como funciona** (H3s):

### Por que review no terminal
- Edita/testa o código durante review (não só lê)
- Diff colorido superior (`delta`)
- Sem context-switch pra browser
- Funciona offline (depois de checkout)

### Por que voltar pra web
- Threads de discussão longas (>3 comentários aninhados)
- Approvals coletivos (UI mostra estado de N revisores)
- Discussions (não-código)
- Side-by-side rendering visual (alguns devs preferem)

### Fluxo macro
- Fase 1: descobrir PR (`gh pr list`)
- Fase 2: checkout (`gh pr checkout <num>`)
- Fase 3: ler diff (`lazygit` ou `git diff`)
- Fase 4: anotar (nvim em pane paralelo)
- Fase 5: submeter review (`gh pr review`)

**Na prática** (H3s):

### Setup uma vez

```bash
# Configurar delta como pager git
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.light false  # ou true pra terminal claro
```

### Fluxo completo

```bash
# Fase 1 — Descobrir
gh pr list                              # PRs abertas no repo atual
gh pr list --search "review-requested:@me"  # só onde sou requester

# Fase 2 — Checkout
gh pr checkout 1234

# Fase 3 — Ler diff
lazygit                                 # diff por arquivo, hunks navegáveis
# OU
git diff main...                        # com delta colorizado

# Fase 4 — Anotar enquanto lê (em pane paralelo)
nvim review-notes.md
# Layout: pane 1 = lazygit, pane 2 = nvim

# Fase 5 — Submeter review
gh pr review --approve --body "LGTM. Pequena sugestão em x.ts:42"
# OU
gh pr review --request-changes --body "$(cat review-notes.md)"
gh pr comment <num> --body "Falta cobrir caso X"
```

### Atalhos úteis lazygit (no contexto review)
- `<space>` em arquivo: stage/unstage hunk
- `d` em arquivo: ver diff completo daquele arquivo
- `s` em hunk: split hunk em chunks menores pra ver isoladamente

### Quando voltar pro browser
- PR com 10+ comentários aninhados (UI threads é melhor)
- Approval coletivo (você é 1 de N reviewers)
- Discussions sobre design (não código)
- Compartilhar diff visual com não-dev

**Armadilhas (≥4):**

1. **`gh pr checkout` em working tree sujo**
   - **Causa:** ter mudanças não-comitadas + esquecer.
   - **Sintoma:** `gh pr checkout` falha; ou merge inesperado dependendo do estado.
   - **Como detectar:** `git status` antes de checkout.
   - **Solução:** stash ou worktree (ver nota 07) antes de checkout. Hábito: `gs && gh pr checkout N`.

2. **Delta config sem `light`/`dark` correto**
   - **Causa:** terminal claro com delta config dark (ou vice-versa).
   - **Sintoma:** diff ilegível, contraste péssimo.
   - **Como detectar:** abrir qualquer diff e perguntar "consigo ler isso fluente?".
   - **Solução:** `git config --global delta.light true` (ou false). Themes específicos: `git config --global delta.syntax-theme "Monokai Extended"` (cf. galho 6).

3. **Aprovar sem rodar testes localmente**
   - **Causa:** "GitHub Actions já testou".
   - **Sintoma:** PR merged quebra integração sutil que test suite não cobria.
   - **Como detectar:** seu review tem mudança não-trivial e você só leu, não rodou.
   - **Solução:** `gh pr checkout N && <run tests>` antes de approve. Especialmente em mudanças de infra/build.

4. **Review longa em uma sentada vs múltiplas**
   - **Causa:** querer "fechar review hoje" mesmo com fadiga.
   - **Sintoma:** miss de bug óbvio na 30ª linha por exaustão.
   - **Como detectar:** review > 30min sem pausa.
   - **Solução:** time-box 30min/sessão. PR de 500 linhas vira 2-3 sessões com pausa. Detach Zellij entre sessões.

**Em inglês (8-10 bullets bilíngues):**
Termos: code review, pull request (PR), checkout, diff, hunk, approve, request changes, reviewer, syntax highlighting, pager. Formato bilíngue.

**Veja também:**
- [[03 - Onboarding em projeto novo]]
- [[07 - Worktrees + Zellij paralelos]]
- [[08 - Refactoring multi-arquivo]]
- [[03-Dominios/Terminal/TUIs/01 - Lazygit — overview|Lazygit overview (galho 4)]]
- [[03-Dominios/Terminal/TUIs/03 - Lazygit — operações intermediárias|Lazygit intermediário (galho 4)]]
- [[03-Dominios/Terminal/CLI Utils/10 - delta — pager moderno pra git diff|delta (galho 6)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#gh CLI|gh CLI]]
- [[Dicionário do Terminal#PR checkout|PR checkout]]

**Referências:**
- gh pr checkout: https://cli.github.com/manual/gh_pr_checkout
- gh pr review: https://cli.github.com/manual/gh_pr_review

- [ ] **Step 4: Verbetes pro Dicionário**

```markdown
### gh CLI
CLI oficial do GitHub. Subcomandos relevantes pra workflow: `gh pr list`, `gh pr checkout <num>`, `gh pr review`, `gh pr comment`. Permite fluxo de review sem sair do terminal.

Veja também: [[05 - Code review no terminal]].

### PR checkout
Operação `gh pr checkout <num>` que cria branch local correspondendo a um PR aberto e faz checkout nela. Exige working tree limpo (ou worktree).

Veja também: [[05 - Code review no terminal]], [[07 - Worktrees + Zellij paralelos]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/05 - Code review no terminal.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/05 - Code review no terminal.md"
grep -E "^### gh CLI$" "03-Dominios/Terminal/Dicionário do Terminal.md"
grep -E "^### PR checkout$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥10 wikilinks; 2 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/05 - Code review no terminal.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 05 — Code review no terminal"
```

---

## Task 7: Nota 06 — Ergonomia das mãos

**Files:**
- Create: `03-Dominios/Terminal/Workflow/06 - Ergonomia das mãos.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: leader key)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://www.osha.gov/ergonomics/computer-workstations
WebFetch: https://help.ableton.com/hc/en-us/articles/360010186899 (modifier keys reference; or use Apple docs)
```

Capturar: princípios ergonomia teclado + modifier keys padrão.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Ergonomia das mãos"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - workflow
  - adepto
  - ergonomia
aliases:
  - Ergonomia mãos
  - Leader keys
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Ergonomia importa pra evitar RSI e cansaço. Princípios: leader keys cross-tool (Space no nvim, prefix no Zellij), CapsLock→Ctrl (mão esquerda agradece), atalhos consistentes que valem aprender (10+ uses/dia). Customizar com critério, não por estética. Pausas e postura > customização hardcore."

**O que é / Como funciona** (H3s):

### O problema das contorções
- Ctrl-Shift-X no teclado padrão = mão esquerda em garra
- Combos pesados (Ctrl-Alt-Shift-K) usados frequentemente = RSI em meses
- Princípio: atalho frequente DEVE ser barato (1-2 dedos, sem estiramento)

### Leader keys cross-tool
- **Conceito:** uma tecla "raiz" que abre um espaço de comandos
- **Nvim:** `<Space>` (LazyVim default)
- **Zellij:** prefix `Ctrl-G` (default; configurável)
- **tmux:** `Ctrl-B` (default; muitos rebindam pra `Ctrl-A`)
- **Vantagem:** namespace de atalhos infinito sem usar Ctrl/Alt/Shift

### CapsLock como modificador
- CapsLock está em posição privilegiada (home row, mão esquerda)
- Por default só toggla maiúsculas (uso quase zero)
- Remapear pra Ctrl (ou Esc, ou modifier custom) = ganho ergonômico imediato

### Atalhos consistentes — princípios
- **Vim grammar como lingua franca:** hjkl funciona em nvim, less, bat, fzf, atuin
- **Leader+letter pra ações de domínio:** `<leader>ff` (find file) em nvim, `<prefix>n` (new tab) em Zellij
- **NÃO override defaults sem motivo:** se você customizou `dd` no nvim, vai sofrer em vim de servidor remoto

### Pausas e postura
- Pomodoro técnico: 25min trabalho + 5min pausa
- Olhar 20-20-20: a cada 20min, 20s olhando 20 metros
- Postura: punhos neutros, cotovelos 90°, monitor à altura dos olhos
- Alongamento básico: rotação de pulso, abrir/fechar mãos

**Na prática** (H3s):

### Remapear CapsLock pra Ctrl (Linux/X11)

```bash
# Persistente (~/.xprofile ou ~/.xsession)
setxkbmap -option ctrl:nocaps

# Ou via /etc/default/keyboard (Debian/Ubuntu)
# XKBOPTIONS="ctrl:nocaps"
```

### Remapear CapsLock pra Ctrl (Linux/Wayland — depende do compositor)

```bash
# GNOME
gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"

# KDE
# System Settings > Keyboard > Advanced > Caps Lock behavior > Caps Lock is Ctrl
```

### Remapear CapsLock pra Ctrl (macOS)

```text
System Preferences > Keyboard > Modifier Keys... > Caps Lock = ^ Control
```

### Verificar
```bash
xev | grep -A2 keysym  # press CapsLock; deve mostrar Control_L
```

### Atalhos que VALEM aprender (10+ uses/dia)
- nvim: `<leader>ff` (find file), `<leader>fg` (live grep), `gd` (goto definition)
- zsh: `Ctrl-R` (history), `Alt-.` (last arg), `Ctrl-A`/`Ctrl-E` (begin/end of line)
- Zellij: `<prefix>n` (new tab), `<prefix>p`/`n` (prev/next tab)
- bash/zsh viperline: `Esc` → modo vim no shell

### Atalhos que NÃO valem (use 1-2x/semana)
- Tudo que envolve Ctrl-Shift-Alt-letter
- Macros raros (memória vaza)
- Atalhos de IDE-specific que você esquecerá em 1 mês

**Armadilhas (≥4):**

1. **CapsLock→Ctrl quebra em algumas ferramentas**
   - **Causa:** software que detecta CapsLock por nome (raro mas existe).
   - **Sintoma:** uma app espera CapsLock real e não aceita Ctrl.
   - **Como detectar:** raríssimo; questione "essa app é importante?".
   - **Solução:** revert seletivo (config por-app) ou aceitar trade-off (CapsLock real via `Shift-CapsLock` em alguns layouts).

2. **Custom keybindings pesadas no leader space**
   - **Causa:** querer mapear tudo.
   - **Sintoma:** 30+ keymaps; esquece quais existem.
   - **Como detectar:** abrir config keymaps.lua e contar entradas.
   - **Solução:** princípio "10+ uses/dia ou não vale". Limpar config a cada 3 meses; tirar o que não usou.

3. **Atalhos conflitam entre nvim/Zellij**
   - **Causa:** Ctrl-H em nvim navega panes (vim-tmux-navigator); Zellij captura antes.
   - **Sintoma:** atalho funciona em um, não em outro.
   - **Como detectar:** keymap "que sempre falha".
   - **Solução:** estabelecer ordem de precedência (geralmente: terminal multiplexer > editor). Plugins existem pra resolver (vim-zellij-navigator).

4. **Trabalhar em maratona sem pausa**
   - **Causa:** "tô no flow, não posso parar".
   - **Sintoma:** após meses, dor cotidiana no pulso/cotovelo.
   - **Como detectar:** qualquer dor pós-trabalho que aparece e some — é warning.
   - **Solução:** Pomodoro (timer no Zellij ou ferramenta dedicada). Pausa de 5min é não-negociável.

**Em inglês (8-10 bullets bilíngues):**
Termos: ergonomics, leader key, prefix key, modifier key, keybinding, keymap, RSI, posture, neutral wrist, muscle memory. Formato bilíngue.

**Veja também:**
- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Editor/02 - Motions e operadores|Motions Vim (galho 1)]]
- [[03-Dominios/Terminal/Shell/06 - ZLE — Zsh Line Editor|ZLE (galho 2)]]
- [[03-Dominios/Terminal/Multiplexer/03 - Modos básicos e keybindings essenciais|Keybindings Zellij (galho 3)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#leader key|leader key]]
- [[Dicionário do Terminal#RSI|RSI]]

**Referências:**
- OSHA — Computer Workstations: https://www.osha.gov/ergonomics/computer-workstations

- [ ] **Step 4: Verbete pro Dicionário**

```markdown
### leader key
Tecla "raiz" que abre namespace de atalhos custom. Permite combinações infinitas sem usar Ctrl/Alt/Shift. Defaults comuns: `<Space>` (nvim/LazyVim), `Ctrl-G` (Zellij), `Ctrl-B` (tmux; muitos rebindam pra `Ctrl-A`).

Veja também: [[06 - Ergonomia das mãos]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/06 - Ergonomia das mãos.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/06 - Ergonomia das mãos.md"
grep -E "^### leader key$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥10 wikilinks; verbete visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/06 - Ergonomia das mãos.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 06 — Ergonomia das mãos"
```

---

## Task 8: Nota 07 — Worktrees + Zellij paralelos

**Files:**
- Create: `03-Dominios/Terminal/Workflow/07 - Worktrees + Zellij paralelos.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: worktree)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://git-scm.com/docs/git-worktree
```

Capturar: comandos worktree (add, list, remove, prune), limitações (apenas um working tree por branch).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Worktrees + Zellij paralelos"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - workflow
  - adepto
  - git
  - worktree
  - playbook
aliases:
  - Worktrees Zellij
  - Multi-task Git
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Playbook: `git worktree add` + sessão Zellij por worktree = multi-task sem stash. Vale pra: review de PR enquanto trabalha em feature; bug fix urgente sem perder estado; testar branch alheia. NÃO vale: `node_modules` compartilhado (cada worktree precisa o seu), lock-files divergem, DB local compartilhada gera conflito. Convenção: `~/repos/<projeto>-<feature>/`."

**O que é / Como funciona** (H3s):

### O que é git worktree
- Git nativamente suporta múltiplos working trees do MESMO repo
- Cada worktree = pasta separada, branch separada, estado independente
- `.git/` compartilhado (commits/refs visíveis em todos os worktrees)
- Adicionado em git 2.5 (2015); estável há quase uma década

### Quando vale
- Bug urgente em main enquanto desenvolve feature em outro worktree
- Code review de PR (`gh pr checkout` em worktree dedicado)
- Comparação A/B de duas abordagens
- Long-running build/test em paralelo com edição

### Quando NÃO vale (atrito > benefício)
- `node_modules` / `target/` / `.venv` por worktree (espaço em disco; tempo de install)
- Lock-files (`package-lock.json`, `Cargo.lock`) divergem; merge depois é dor
- DB local (Postgres, Redis) compartilhada gera conflito de estado
- Containers Docker bindados a paths absolutos

### Modelo mental
- Worktree = mini-clone, sem custo de .git
- Mas com custo de re-instalar deps + reconfig DB
- Trade-off: tempo "alocar/desalocar worktree" vs "stash/pop"

**Na prática** (H3s):

### Comandos essenciais

```bash
# Listar worktrees do repo atual
git worktree list

# Adicionar worktree pra branch existente
git worktree add ~/repos/myproj-bugfix bugfix/login

# Adicionar pra branch nova
git worktree add -b feature/new-thing ~/repos/myproj-feature

# Remover worktree (limpa pasta + ref)
git worktree remove ~/repos/myproj-bugfix

# Prune (remove refs de worktrees deletadas manualmente)
git worktree prune
```

### Convenção de naming

```text
~/repos/myproj/              ← worktree principal (main branch)
~/repos/myproj-bugfix/       ← worktree pra bugfix urgente
~/repos/myproj-review-1234/  ← worktree pra review de PR #1234
~/repos/myproj-feat-X/       ← worktree pra feature paralela
```

### Combo Zellij + worktree

```bash
# Função no ~/.zshrc
wt-new() {
    local proj="$1"
    local branch="$2"
    local path="$HOME/repos/${proj}-${branch//\//-}"
    git worktree add "$path" "$branch"
    cd "$path"
    zellij a -c "${proj}-${branch//\//-}"
}

# Uso
wt-new myproj feature/login
# Cria worktree em ~/repos/myproj-feature-login
# Abre sessão Zellij "myproj-feature-login"
```

### Limpeza weekly

```bash
# Listar worktrees + último access
git worktree list --porcelain | grep "^worktree" | while read -r line; do
    p=$(echo "$line" | cut -d' ' -f2)
    date=$(stat -c %y "$p" 2>/dev/null | cut -d' ' -f1)
    echo "$date $p"
done | sort

# Remover worktrees inativos há +14 dias (revisar manualmente antes!)
```

**Armadilhas (≥4):**

1. **`git worktree remove` sem checar trabalho não-comitado**
   - **Causa:** habit de "limpar".
   - **Sintoma:** mudanças não-comitadas + não-stashed somem.
   - **Como detectar:** `git -C <path> status` antes de remove.
   - **Solução:** `git worktree remove --force` SÓ depois de verificar manualmente. Detault sem `--force` falha em working tree dirty (proteção nativa).

2. **`node_modules` duplicado em N worktrees**
   - **Causa:** cada worktree precisa `npm install`.
   - **Sintoma:** disco enche; instalações lentas em cada worktree.
   - **Como detectar:** `du -sh ~/repos/myproj-*/node_modules`.
   - **Solução:** se monorepo + pnpm/yarn workspaces + content-addressable store, deps compartilhadas. Ou aceita o custo (vale a pena pra trabalho paralelo).

3. **DB local compartilhada gera conflito**
   - **Causa:** Postgres em `localhost:5432` único; worktree A roda migration X, worktree B roda Y.
   - **Sintoma:** schema DB inconsistente; bug "aleatório".
   - **Como detectar:** mismatch entre schema esperado e real.
   - **Solução:** DB-por-worktree (Docker compose com porta diferente). OU disciplina: uma worktree por vez interage com DB local.

4. **Branch checked out em 2 worktrees gera erro**
   - **Causa:** git proíbe ter mesmo branch em 2 worktrees.
   - **Sintoma:** `git worktree add` falha com "branch X is already checked out".
   - **Como detectar:** msg de erro óbvia.
   - **Solução:** cada worktree = branch própria. Pra "compartilhar branch", use detached HEAD: `git worktree add -d ~/repos/myproj-readonly main`.

5. **Esquecer prune após delete manual**
   - **Causa:** apagou pasta de worktree direto (`rm -rf`).
   - **Sintoma:** `git worktree list` mostra worktree "prunable" ou warning.
   - **Como detectar:** `git worktree list`.
   - **Solução:** preferir `git worktree remove <path>`. Se já apagou manualmente: `git worktree prune`.

**Em inglês (8-10 bullets bilíngues):**
Termos: worktree, branch, checkout, stash, lock file, dependencies, dirty working tree, prune, parallel, multi-task. Formato bilíngue.

**Veja também:**
- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[08 - Refactoring multi-arquivo]]
- [[03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes|Sessões persistentes (galho 3)]]
- [[03-Dominios/Terminal/TUIs/01 - Lazygit — overview|Lazygit overview (galho 4)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#worktree|worktree]]
- [[Dicionário do Terminal#named session|named session]]

**Referências:**
- git-worktree: https://git-scm.com/docs/git-worktree

- [ ] **Step 4: Verbete pro Dicionário**

```markdown
### worktree
Funcionalidade nativa do git (`git worktree add <path> <branch>`) que permite múltiplos working trees do mesmo repo em pastas separadas. Cada worktree tem branch e estado independentes; `.git/` é compartilhado. Útil pra multi-task sem stash. Não-trivial com `node_modules` ou DBs locais.

Veja também: [[07 - Worktrees + Zellij paralelos]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/07 - Worktrees + Zellij paralelos.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/07 - Worktrees + Zellij paralelos.md"
grep -E "^### worktree$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥9 wikilinks; verbete visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/07 - Worktrees + Zellij paralelos.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 07 — Worktrees + Zellij paralelos"
```

---

## Task 9: Nota 08 — Refactoring multi-arquivo

**Files:**
- Create: `03-Dominios/Terminal/Workflow/08 - Refactoring multi-arquivo.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: quickfix)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://neovim.io/doc/user/quickfix.html
WebFetch: https://www.lazyvim.org/keymaps (LazyVim default keymaps relevantes pra LSP)
```

Capturar: comandos quickfix (`:cdo`, `:cfdo`, `:cnext`, `:cprev`), LSP rename pelo lspconfig.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Refactoring multi-arquivo"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - workflow
  - magus
  - refactoring
  - playbook
aliases:
  - Refactoring multi-file
  - rg quickfix LSP
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Playbook: refactor que toca 10+ arquivos. Pipeline: `rg <padrão>` pra mapear ocorrências → carregar em nvim quickfix → `:cdo s/X/Y/gc` pra editar em lote OU LSP rename pra refactor type-aware. Validar com `:cnext`/`:cprev`. Cuidado: `:cdo` quando mudanças invalidam matches subsequentes. LSP rename é seguro pra símbolos; rg+quickfix é flexível mas requer atenção."

**O que é / Como funciona** (H3s):

### Por que refactor multi-arquivo merece técnica
- Find/replace global no IDE é caro mente (carregar tudo)
- IDE não tem o controle fino que vim quickfix dá
- LSP rename é seguro mas só pra símbolos (não strings, comentários)
- Combinar rg (descoberta) + nvim quickfix (edição) + LSP (segurança) dá o melhor

### Quickfix — o que é
- Lista global do nvim de "localizações" (file:line:col + texto)
- Carregada por: `:make`, `:grep`, `:vimgrep`, ripgrep plugin (Telescope), LSP diagnostics
- Navegada por: `:cnext`/`:cprev`, `:copen` (lista), `:cclose`
- Editada por: `:cdo <cmd>` (em cada match) ou `:cfdo <cmd>` (em cada arquivo)

### Três fluxos principais
- **rg + quickfix:** flexível, edita strings/regex em qualquer arquivo
- **LSP rename:** seguro, só símbolos (não comments/strings)
- **Telescope live_grep + quickfix:** GUI rica pra escolher matches antes de carregar

### Quando usar cada
- Renomear função/variável → LSP rename (`<leader>rn`)
- Mudar string/comment/log message em N arquivos → rg + quickfix + `:cdo`
- Refactor estrutural (mudar shape) → manual nvim com substituições Telescope-driven

**Na prática** (H3s):

### Fluxo rg + quickfix

```bash
# Fora do nvim — exploratório
rg "OldName" --stats
rg "OldName" --files-with-matches

# Dentro do nvim
:grep "OldName"      # carrega matches no quickfix (usa ripgrep se configurado)
:copen               # abre janela quickfix
:cdo s/OldName/NewName/gc   # substitui com confirmação em CADA match
:cfdo update         # salva todos arquivos modificados (usa :update, só salva se mudou)
```

### Fluxo LSP rename

```text
# Cursor sobre símbolo
<leader>rn  (LazyVim default)
# Digite novo nome → confirma → todos os usos no projeto atualizados
```

### Fluxo Telescope live_grep + quickfix

```text
:Telescope live_grep
# Buscar padrão
# <C-q> envia resultados pro quickfix
# :copen
# :cdo s/.../.../gc
```

### Pipeline avançado: rg → fzf → quickfix

```bash
# Selecionar matches manualmente via fzf antes de carregar quickfix
rg "padrão" --vimgrep | fzf -m | tr '\n' '\0' | xargs -0 nvim -q -
# (Telescope dá UX melhor; esse pipeline é pra contexto fora do nvim)
```

### Validar refactor

```bash
# Após refactor, rodar tests
npm test  # ou pytest, cargo test, etc.

# Verificar que não sobrou nada do nome antigo
rg "OldName" --stats

# Lazygit pra ver diff total antes de commit
lazygit
```

**Armadilhas (≥4):**

1. **`:cdo s/X/Y/g` (sem flag `c`) — substitui tudo sem confirmação**
   - **Causa:** querer "ser produtivo".
   - **Sintoma:** edita arquivos que não devia (matches false positive).
   - **Como detectar:** rodar `:cdo s/X/Y/g` e depois `:diffsplit` ver mudanças.
   - **Solução:** sempre usar flag `c` (confirm) em refactor não-trivial. Modos: `y` (sim), `n` (não), `a` (todos restantes), `q` (parar).

2. **Match em string contendo padrão errado**
   - **Causa:** rg é text-search; pega `OldName` em comentário, log, doc.
   - **Sintoma:** comentários ou strings mudam quando não deviam.
   - **Como detectar:** ver matches em comentários no `:copen`.
   - **Solução:** rg com word boundary `\b`: `rg "\bOldName\b"`. Ou usar LSP rename quando aplicável.

3. **Mudanças invalidam matches subsequentes**
   - **Causa:** `:cdo` carrega lista uma vez; se primeira substituição muda número de linhas, próximos matches podem apontar pra linha errada.
   - **Sintoma:** algumas substituições parecem "pular" ou aplicar em local errado.
   - **Como detectar:** raro; pegar lendo cada confirmação.
   - **Solução:** `:cfdo` (per-file) é mais robusto. Ou recarregar quickfix entre batches: `:grep` de novo.

4. **LSP rename em projeto com múltiplos languages**
   - **Causa:** LSP só conhece a linguagem em foco.
   - **Sintoma:** rename funciona em arquivo TypeScript mas não trocou referências em arquivo JSON/YAML que mencionava o nome.
   - **Como detectar:** após rename, `rg "OldName"` ainda mostra matches.
   - **Solução:** LSP rename pra símbolos; rg + quickfix pra cross-language refs (configs, schemas, docs).

5. **Não commitar antes do refactor**
   - **Causa:** começar mudanças sem baseline.
   - **Sintoma:** `:cdo` em larga escala falha; reverter manualmente é miserável.
   - **Como detectar:** `git status` antes de começar.
   - **Solução:** commit pequeno "WIP: pre-refactor X" antes. `git reset --hard HEAD` se algo der errado.

**Em inglês (8-10 bullets bilíngues):**
Termos: refactoring, quickfix, location list, find and replace, language server, LSP rename, regex, word boundary, batch edit, dry run. Formato bilíngue.

**Veja também:**
- [[03 - Onboarding em projeto novo]]
- [[05 - Code review no terminal]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Editor/09 - LSP no Neovim — Mason, nvim-lspconfig, nvim-cmp|LSP no Neovim (galho 1)]]
- [[03-Dominios/Terminal/Editor/11 - Workflow avançado — quickfix, sessions, refactoring pesado|Quickfix avançado (galho 1)]]
- [[03-Dominios/Terminal/CLI Utils/02 - ripgrep e fd — buscar conteúdo e nomes|ripgrep (galho 6)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#quickfix|quickfix]]
- [[Dicionário do Terminal#LSP|LSP]]

**Referências:**
- nvim quickfix: https://neovim.io/doc/user/quickfix.html
- LazyVim keymaps: https://www.lazyvim.org/keymaps

- [ ] **Step 4: Verbete pro Dicionário**

```markdown
### quickfix
Lista global do Neovim de "localizações" (file:line:col + texto). Populada por `:grep`, `:make`, LSP diagnostics, Telescope. Navegada por `:cnext`/`:cprev`/`:copen`. Editada em lote por `:cdo <cmd>` (cada match) ou `:cfdo <cmd>` (cada arquivo). Essencial pra refactor multi-arquivo.

Veja também: [[08 - Refactoring multi-arquivo]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/08 - Refactoring multi-arquivo.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/08 - Refactoring multi-arquivo.md"
grep -E "^### quickfix$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥10 wikilinks; verbete visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/08 - Refactoring multi-arquivo.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 08 — Refactoring multi-arquivo"
```

---

## Task 10: Nota 09 — Transições de contexto

**Files:**
- Create: `03-Dominios/Terminal/Workflow/09 - Transições de contexto.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: deep work, switching cost, shallow task, context switching cost)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://en.wikipedia.org/wiki/Context_switch
WebFetch: https://en.wikipedia.org/wiki/Deep_work
```

Capturar: terminologia (deep work, context switching, switching cost), origem.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Transições de contexto"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - workflow
  - magus
  - contexto
  - meta
aliases:
  - Transições contexto
  - Context switching
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Trabalho profundo (deep work) vs tasks rasas (shallow tasks) exigem contextos diferentes. Cada switch entre eles tem custo cognitivo (10-30min pra "voltar"). Estratégia: políticas explícitas — uma tab = um contexto, sessões persistentes pra deep work + efêmeras pra shallow, focus mode quando precisar isolamento. Como fechar contextos sem perder estado: detach + bookmarks de cursor + notas TODO no scratch."

**O que é / Como funciona** (H3s):

### Deep work vs shallow tasks
- **Deep work:** atividade focada e cognitivamente exigente; 1-4h sustentadas; produz valor único (Cal Newport, "Deep Work")
- **Shallow tasks:** atividade logística/repetitiva; minutos cada; reativa (emails, tickets pequenos, sync)
- Maioria dos devs faz 80% shallow / 20% deep — invertendo isso é a tese do livro

### Switching cost cognitivo
- Voltar ao estado mental de uma task pesada custa 10-30min de "reaquecimento"
- 5 switches por dia = 1h+ desperdiçada
- Não é mito — neurociência (working memory, attention residue)
- Implicação: blocos longos > muitos blocos curtos

### Sessions efêmeras vs persistentes — política por contexto
- **Efêmera:** shallow tasks. Abre, faz, fecha. Sem custo de cleanup.
- **Persistente:** deep work. Preserva estado. Tab = capítulo do contexto.
- Misturar é a confusão clássica: deep work em sessão efêmera = perder contexto.

### Uma tab = um contexto
- Tab "code" = onde você lê/edita
- Tab "server" = onde o app roda
- Tab "test" = onde rodam suites
- Tab "git" = lazygit
- Cada uma tem 1 papel — não misturar (não rodar testes na tab "code")

### Focus mode em deep work
- Zellij `Alt-f` (default) — esconde UI auxiliar
- Maximiza pane de código
- Sinaliza ao cérebro "trabalho profundo"

**Na prática** (H3s):

### Política diária (template)

```text
08h-10h:   Deep work bloco 1 (sessão persistente, focus mode)
10h-11h:   Shallow / shallow (sessões efêmeras pra tickets, sync)
11h-13h:   Deep work bloco 2
13h-14h:   Almoço (away from keyboard)
14h-15h:   Code review (cf. nota 05)
15h-17h:   Deep work bloco 3 OU continuation
17h-18h:   Tear-down + planning amanhã (cf. nota 04)
```

Hábito: pôr no calendário; honrar.

### Como fechar contexto sem perder estado
- `:mksession` no nvim (salva tabs, buffers, cursor) — restore com `nvim -S`
- Detach Zellij (preserva tudo)
- Anotar TODO/próximo passo em scratch file no contexto

```bash
# scratch por projeto
nvim ~/scratch/<projeto>-todo.md
# Linha curta:
# 2026-05-24 EOD: continuar de src/auth.ts:142, falta caso edge X
```

### Quando aceitar shallow vs adiar
- Mensagem em DM com urgência real (cliente, prod down) → atender
- Email "quando puder" → batch (2x/dia, não responder no momento)
- Sync às 14h (recorrente) → bloco fixo, não interrompe deep work
- Notificação aleatória → silenciar (Slack DND, focus mode do OS)

### Memória muscular — construir
- Atalhos repetidos viram automáticos em 2-4 semanas
- Drilling deliberado: 1 atalho/dia, usar 20+ vezes
- Não tente memorizar 50 atalhos numa semana

**Armadilhas (≥4):**

1. **Confundir "estar ocupado" com "deep work"**
   - **Causa:** muitas coisas pequenas dão sensação de produtividade.
   - **Sintoma:** ao fim do dia, 8h trabalhadas e nada importante avançou.
   - **Como detectar:** ao final do dia, escrever "o que avancei substancialmente?". Se a lista é só tasks pequenas, foi shallow.
   - **Solução:** bloquear 2-4h/dia EXPLICITAMENTE pra deep work. Calendário; sinalizar pro time; desligar notificações.

2. **Deep work sem mudança visível de contexto (mesma tab/mesma sessão)**
   - **Causa:** "vou começar deep" sem ritual.
   - **Sintoma:** mente fica saltando pra emails, Slack.
   - **Como detectar:** notar urgência de checar Slack em <10min.
   - **Solução:** abrir nova sessão Zellij OU novo focus mode. Sinal claro pro cérebro.

3. **Confundir descanso com mais shallow tasks**
   - **Causa:** "vou descansar respondendo emails".
   - **Sintoma:** cansaço cumulativo; deep work do bloco 2 sofre.
   - **Como detectar:** energia ao fim do dia: cair de produtiva por shallow tasks excessivo.
   - **Solução:** pausa real = away from keyboard. Caminhar, alongar, água. NÃO "checagem rápida".

4. **Não fechar contextos — abrir cada vez do zero**
   - **Causa:** sem ritual de tear-down (cf. nota 04).
   - **Sintoma:** segunda-feira reconstruindo o que sexta deixou.
   - **Como detectar:** ao começar o dia, sentir que está "achando o lugar".
   - **Solução:** scratch file por projeto + `:mksession` nvim + detach Zellij. Próximo dia: abrir tudo, contexto reconstrói em minutos.

5. **Atender DM toda durante deep work**
   - **Causa:** "vai ser rápido".
   - **Sintoma:** bloco de deep work fragmentado em 5 minutos efetivos.
   - **Como detectar:** ver Slack/DM count durante bloco.
   - **Solução:** DND (do not disturb) explícito durante bloco. Comunicar ao time: "estou em deep work até X horas". Emergências reais vão por canal de emergência (não DM).

**Em inglês (8-10 bullets bilíngues):**
Termos: deep work, shallow task, context switching, switching cost, attention residue, focus mode, do not disturb (DND), do-not-disturb, scratch file, working memory. Formato bilíngue.

**Veja também:**
- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[04 - Setup matinal e tear-down]]
- [[06 - Ergonomia das mãos]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#deep work|deep work]]
- [[Dicionário do Terminal#shallow task|shallow task]]
- [[Dicionário do Terminal#switching cost|switching cost]]
- [[Dicionário do Terminal#context switching cost|context switching cost]]

**Referências:**
- Context switching (Wikipedia): https://en.wikipedia.org/wiki/Context_switch
- Deep Work (Cal Newport): https://en.wikipedia.org/wiki/Deep_work

- [ ] **Step 4: Verbetes pro Dicionário**

```markdown
### context switching cost
Custo cognitivo de alternar entre tarefas/contextos. Estimado em 10-30min de "reaquecimento" pra retomar tarefa cognitivamente exigente. Mitigação: blocos longos, políticas explícitas, fechamento limpo de contextos.

Veja também: [[09 - Transições de contexto]].

### deep work
Atividade focada e cognitivamente exigente sustentada por 1-4h, produzindo valor único. Termo cunhado por Cal Newport. Oposto: [[Dicionário do Terminal#shallow task|shallow task]].

Veja também: [[09 - Transições de contexto]].

### shallow task
Atividade logística/repetitiva (emails, tickets pequenos, sync) tipicamente reativa. Cumulativa em horas; baixa profundidade cognitiva por unidade. Oposto: [[Dicionário do Terminal#deep work|deep work]].

Veja também: [[09 - Transições de contexto]].

### switching cost
Sinônimo curto pra [[Dicionário do Terminal#context switching cost|context switching cost]].

Veja também: [[09 - Transições de contexto]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/09 - Transições de contexto.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/09 - Transições de contexto.md"
grep -E "^### deep work$" "03-Dominios/Terminal/Dicionário do Terminal.md"
grep -E "^### switching cost$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥10 wikilinks; 4 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/09 - Transições de contexto.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 09 — Transições de contexto"
```

---

## Task 11: Nota 10 — Capstone: Sessão ideal — anatomia de um dia keyboard-first

**Files:**
- Create: `03-Dominios/Terminal/Workflow/10 - Sessão ideal — anatomia de um dia keyboard-first.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: capstone)

- [ ] **Step 1: Pesquisa-âncora**

Capstone NÃO faz pesquisa nova. Compõe as 9 notas anteriores. Skip Step 1.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Sessão ideal — anatomia de um dia keyboard-first"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - workflow
  - magus
  - capstone
  - sintese
aliases:
  - Capstone Workflow
  - Sessão ideal
  - Dia keyboard-first
---
```

- [ ] **Step 3: Escrever capstone**

**ATENÇÃO:** capstone NÃO segue padrão das outras notas. NÃO re-explica ferramentas. Compõe. Tese-em-ato.

**TL;DR (callout `[!abstract]`):**
"Capstone do galho 7 e fechamento da trilha Terminal. Reconta um dia típico do dev keyboard-first do boot ao tear-down, integrando galhos 1-7. Cenário hipotético neutro (alice, dev backend, feature nova). Cada momento aciona uma ou mais notas anteriores via wikilink. Decisões em pontos de bifurcação. NÃO re-explica nada — assume galhos 1-7 dominados."

**Estrutura:**

```markdown
## Cenário

Alice é dev backend num monorepo Python/TypeScript. Hoje começa uma feature de autenticação OAuth que vai durar ~3 dias. Trabalha em laptop Ubuntu 24.04 + segundo monitor; usa Zellij + Neovim/LazyVim + Lazygit + dotfiles versionados com chezmoi.

## Fluxo (cronológico)

### Boot (08h00–08h15)

Alice abre o emulator de terminal e roda:

```bash
work codex-oauth
```

A função `work` (do `~/.zshrc`) faz: `zoxide query codex-oauth` → `cd` → `zellij a -c codex-oauth` com layout default. Vê 3 tabs (code/git/server). Lazygit já roda na tab "git".

→ Referência: [[04 - Setup matinal e tear-down]], [[02 - Anatomia da sessão de trabalho]].

### Onboard de contexto (08h15–08h45)

Não trabalha nessa feature há 3 dias. Lê scratch file pra restaurar contexto:

```bash
nvim ~/scratch/codex-oauth-todo.md
# 2026-05-21 EOD: parei em src/auth/oauth.ts:142, falta caso edge: refresh token sem expiração explícita
```

Faz onboard rápido do estado atual:

```bash
eza --tree -L 2 --git-ignore src/auth/
rg "TODO\|FIXME" src/auth/
lazygit  # ver últimos commits
```

→ Referência: [[03 - Onboarding em projeto novo]].

### Deep work bloco 1 (08h45–11h00)

Alice ativa focus mode (Alt-f no Zellij), maximiza a tab "code". Abre `:Telescope find_files`, escolhe `src/auth/oauth.ts`. Vai até linha 142. Comunica ao time no Slack: "deep work até 11h, DM só pra emergência real". DND ativado.

Trabalha. Usa atalhos de leader key (`<leader>ff`, `<leader>fg`, `gd` LSP definition). Periodicamente, salva session: `:mksession!`.

→ Referência: [[09 - Transições de contexto]], [[06 - Ergonomia das mãos]].

### Pausa intencional (11h00–11h15)

Alice fecha o laptop. Caminha 5min, alonga pulso, bebe água. NÃO checa Slack/email.

→ Referência: [[06 - Ergonomia das mãos]], [[09 - Transições de contexto]].

### Code review urgente (11h15–11h45)

DM do tech lead: "tem 10min pra olhar PR #1234? bloqueia release". Alice abre uma worktree pra não perder estado da feature:

```bash
wt-new codex-myproj review-1234
git worktree add ~/repos/codex-myproj-review-1234 main
cd ~/repos/codex-myproj-review-1234
gh pr checkout 1234
```

Nova sessão Zellij é criada. Alice abre lazygit, lê diff por arquivo, anota observações em `review-notes.md` em pane paralelo:

```bash
gh pr review 1234 --request-changes --body "$(cat review-notes.md)"
```

Detach da sessão de review, volta pra sessão de feature:

```bash
zellij a codex-oauth
```

Worktree fica pra futura limpeza.

→ Referência: [[07 - Worktrees + Zellij paralelos]], [[05 - Code review no terminal]].

### Almoço (12h00–13h00)

Sessão Zellij detached — estado preservado.

### Refactoring multi-arquivo (14h00–15h30)

Alice percebe que o nome `validateToken` deveria ser `verifyToken` (alinhar com vocabulário do RFC). Refactor toca ~20 ocorrências em 12 arquivos.

```bash
# Mapear
rg "\bvalidateToken\b" --stats

# Editor: LSP rename pelo símbolo
# Cursor em `validateToken` → <leader>rn → verifyToken → Enter

# Verificar resíduos (comments, strings, docs)
rg "validateToken"
# Resta uma referência em docs/oauth.md
```

Pra resíduos não-código, usa quickfix:

```text
:grep "validateToken"
:copen
:cdo s/validateToken/verifyToken/gc
```

Roda testes; tudo passa.

→ Referência: [[08 - Refactoring multi-arquivo]].

### Sync com time (15h30–16h00)

Tab "sync" efêmera. Alice abre browser pra meet — único momento do dia que sai do terminal.

→ Referência: [[01 - Filosofia keyboard-first — quando vale e quando não]] (quando NÃO).

### Deep work bloco 2 (16h00–17h30)

Continua feature. Implementa caso edge do refresh token.

### Tear-down (17h30–17h45)

Alice atualiza scratch file:

```bash
nvim ~/scratch/codex-oauth-todo.md
# 2026-05-24 EOD: refactor validateToken→verifyToken feito; falta caso edge refresh sem expiração;
# amanhã: começar tests pro caso edge
```

Salva nvim session, detach Zellij (`zellij d` ou Ctrl-Q). Lazygit commit último WIP. Não usa `zellij k` (preserva pra amanhã).

→ Referência: [[04 - Setup matinal e tear-down]].

## Decisões em pontos de bifurcação

### Quando voltar pro browser?

- Threads de discussão longas em PR (>3 níveis aninhados)
- Discussions GitHub (não-código)
- Meetings, video calls
- Browsing exploratório (busca por docs externas)

→ [[01 - Filosofia keyboard-first — quando vale e quando não]] cobre limites.

### Quando worktree NÃO compensa?

- Mudança de <30min ("vai e volta rápido"); stash é mais barato
- Branch tem `node_modules` pesado que precisa re-install (a menos que monorepo + pnpm)
- DB local exige migração que vai entrar em conflito

→ [[07 - Worktrees + Zellij paralelos]].

### Quando sair do deep work?

- Mensagem real de emergência (não DM "tem 5min?")
- Pausa programada (Pomodoro)
- Notou que perdeu o flow há +15min (não vai voltar)

→ [[09 - Transições de contexto]].

### Quando reescrever a config vs aceitar default?

- Defaults inutilizáveis (lentos, conflitam) → reescrever
- Defaults funcionam mas estranhos → aceitar e adaptar-se
- Customização que beneficia <10x/semana → não vale

→ [[06 - Ergonomia das mãos]].

### Quando aceitar GUI?

- Diff visual side-by-side (alguns devs preferem)
- Code coverage report visual
- Profiling/flamegraphs (interativo)
- Quando o time inteiro está em uma ferramenta GUI

→ [[01 - Filosofia keyboard-first — quando vale e quando não]].

## Em inglês (10 bullets bilíngues)

Termos vindos da composição:
- **fluxo cronológico** — *chronological flow*
- **dia keyboard-first** — *keyboard-first day*
- **bifurcação de decisão** — *decision branch point*
- **sessão de trabalho** — *work session*
- **deep work bloco** — *deep work block*
- **onboard de contexto** — *context onboarding*
- **pausa intencional** — *intentional break*
- **fechamento limpo** — *clean shutdown*
- **estado preservado** — *preserved state*
- **synthese-em-ato** — *thesis-in-act*

## Veja também

- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[03 - Onboarding em projeto novo]]
- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[06 - Ergonomia das mãos]]
- [[07 - Worktrees + Zellij paralelos]]
- [[08 - Refactoring multi-arquivo]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/Editor/index|Editor (galho 1)]]
- [[03-Dominios/Terminal/Shell/index|Shell (galho 2)]]
- [[03-Dominios/Terminal/Multiplexer/index|Multiplexer (galho 3)]]
- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev (galho 4)]]
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Terminal/CLI Utils/index|CLI Utils (galho 6)]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#capstone|capstone]]

## Referências

(sem refs externas; capstone é síntese)
```

- [ ] **Step 4: Verbete pro Dicionário**

```markdown
### capstone
Nota-síntese ao final de um galho/trilha que NÃO re-explica conceitos; compõe-os. Tese-em-ato. Padrão: cenário → fluxo → decisões em bifurcações. Assume galhos anteriores dominados.

Veja também: [[10 - Sessão ideal — anatomia de um dia keyboard-first]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/10 - Sessão ideal — anatomia de um dia keyboard-first.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/10 - Sessão ideal — anatomia de um dia keyboard-first.md"
grep -E "^### capstone$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe; ≥18 wikilinks (capstone referencia todas anteriores + 6 galhos); verbete visível.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/10 - Sessão ideal — anatomia de um dia keyboard-first.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-workflow): add nota 10 — Capstone: Sessão ideal"
```

---

## Task 12: MOC do galho

**Files:**
- Create: `03-Dominios/Terminal/Workflow/index.md`

- [ ] **Step 1: Frontmatter**

```yaml
---
title: "Workflow"
type: moc
publish: true
created: 2026-05-24
updated: 2026-05-24
status: growing
tags:
  - terminal
  - workflow
  - moc
aliases:
  - MOC Workflow
  - Galho 7
---
```

- [ ] **Step 2: Escrever MOC**

Estrutura completa (cf. spec seção 3.2):

```markdown
# Workflow

> [!abstract] TL;DR
> Galho 7 e último da trilha Terminal. 5 playbooks que recombinam ferramentas dos galhos 1-6 + 4 meta-práticas (filosofia keyboard-first, anatomia da sessão, ergonomia, transições de contexto) + 1 capstone sintetizando a trilha inteira em forma de "anatomia de um dia keyboard-first". 10 notas (3 Iniciado + 4 Adepto + 3 Magus).

Este galho NÃO é mais uma ferramenta — é a tese sobre como compor as ferramentas dos galhos 1-6 em fluxos reais de trabalho. As 4 meta-práticas dão o porquê (filosofia, anatomia da sessão, ergonomia, transições de contexto). Os 5 playbooks dão o quê (onboarding, setup matinal, code review, worktrees, refactoring). O capstone dá o como integrado, em forma de cenário cronológico — anatomia de um dia keyboard-first de ponta a ponta.

## Conteúdo

### Iniciado
- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[03 - Onboarding em projeto novo]]

### Adepto
- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[06 - Ergonomia das mãos]]
- [[07 - Worktrees + Zellij paralelos]]

### Magus
- [[08 - Refactoring multi-arquivo]]
- [[09 - Transições de contexto]]
- [[10 - Sessão ideal — anatomia de um dia keyboard-first]]

## Tools usadas por cada nota

| Nota | Editor (G1) | Shell (G2) | Multiplexer (G3) | TUIs (G4) | Dotfiles (G5) | CLI Utils (G6) |
|------|---|---|---|---|---|---|
| 01 — Filosofia | — | — | — | — | — | — |
| 02 — Anatomia sessão | — | — | Zellij conceitos | — | — | — |
| 03 — Onboarding | nvim+telescope | — | — | lazygit | — | zoxide, eza, rg, bat |
| 04 — Setup matinal | nvim | — | Zellij sessions+layouts | lazygit | configs versionadas | atuin |
| 05 — Code review | nvim | — | Zellij panes | lazygit | — | delta, bat, gh CLI |
| 06 — Ergonomia | nvim keymaps | Zsh keybindings | Zellij keybindings | — | — | — |
| 07 — Worktrees | nvim | — | Zellij named sessions | lazygit | — | — |
| 08 — Refactoring | nvim+quickfix+LSP | — | — | — | — | rg |
| 09 — Transições | — | — | Zellij sessions+focus | — | — | atuin |
| 10 — Capstone | tudo | tudo | tudo | tudo | tudo | tudo |

## Rotas alternativas

- **Mínimo viável (Iniciado primeiro):** `01` → `02` → `03` — entende filosofia, vocabulário, primeiro fluxo concreto.
- **Quer ser produtivo já:** `03` → `04` → `05` — onboarding, setup matinal, code review. Pula meta-prática.
- **Quer entender modelo mental:** `01` → `02` → `06` → `09` — pula playbooks, foca nas 4 meta-práticas.
- **Refactor pesado:** `08` direto (assume Editor + CLI Utils dominados).
- **Capstone:** `10` — só depois de ter lido as 9 anteriores.

## Pré-requisitos

Este galho assume galhos 1-6 dominados. Notas referenciam mas NÃO re-explicam ferramentas:

- Editor (galho 1): nvim, LazyVim, telescope, quickfix, LSP
- Shell (galho 2): zsh, p10k, keybindings, completion
- Multiplexer (galho 3): Zellij sessions, layouts, panes
- TUIs (galho 4): lazygit (operações intermediárias)
- Dotfiles (galho 5): chezmoi/stow (configs versionadas)
- CLI Utils (galho 6): fzf, rg, bat, eza, zoxide, atuin, delta

## Veja também

- [[Dicionário do Terminal]] (bloco ## Workflow)
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Terminal/Editor/index|Editor (galho 1)]]
- [[03-Dominios/Terminal/Shell/index|Shell (galho 2)]]
- [[03-Dominios/Terminal/Multiplexer/index|Multiplexer (galho 3)]]
- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev (galho 4)]]
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Terminal/CLI Utils/index|CLI Utils (galho 6)]]
```

- [ ] **Step 3: Validar**

```bash
test -f "03-Dominios/Terminal/Workflow/index.md"
grep -c '\[\[' "03-Dominios/Terminal/Workflow/index.md"
grep -E "^### Iniciado$|^### Adepto$|^### Magus$" "03-Dominios/Terminal/Workflow/index.md"
```

Esperado: arquivo existe; ≥18 wikilinks; 3 H3s de fases visíveis.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Workflow/index.md"
git commit -m "feat(terminal-workflow): add MOC do galho 7"
```

---

## Task 13: Tronco — ativar wikilink e fechar trilha

**Files:**
- Modify: `03-Dominios/Terminal/index.md`

- [ ] **Step 1: Ler tronco atual**

```bash
head -50 "03-Dominios/Terminal/index.md"
```

Localizar linha 33: `- Workflow — galho 7 (planejado): playbooks cross-tool`.

- [ ] **Step 2: Atualizar bullet do galho 7**

Substituir linha 33 por:

```markdown
- [[03-Dominios/Terminal/Workflow/index|Workflow]] — galho 7: playbooks cross-tool (onboarding, review, worktrees, refactoring) + meta-práticas (filosofia keyboard-first, ergonomia, transições de contexto) + capstone (anatomia de um dia)
```

- [ ] **Step 3: Atualizar frontmatter**

Mudar:
- `updated: 2026-05-21` → `updated: 2026-05-24`
- `progresso: andamento` → `progresso: completo`

- [ ] **Step 4: Atualizar TL;DR**

Substituir o callout TL;DR atual por:

```markdown
> [!abstract] TL;DR
> Trilha do ambiente de trabalho no terminal: editor (Neovim/LazyVim), shell (Zsh/p10k), multiplexer (Zellij), TUIs (Lazygit/Lazydocker), dotfiles, CLI utils e playbooks de workflow. 7 galhos completos, ~67 notas distribuídas em 3 fases (Iniciado → Adepto → Magus) por galho + capstones. Trilha fechada — cada galho é referência consultável.
```

- [ ] **Step 5: Validar**

```bash
grep -E "^- \[\[03-Dominios/Terminal/Workflow/index\|Workflow\]\]" "03-Dominios/Terminal/index.md"
grep "^updated:" "03-Dominios/Terminal/index.md"
grep "^progresso:" "03-Dominios/Terminal/index.md"
```

Esperado: wikilink ativo; `updated: 2026-05-24`; `progresso: completo`.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/index.md"
git commit -m "feat(terminal): tronco com wikilink ativo pro galho 7 e trilha completa"
```

---

## Task 14: Validação final do galho

**Files:** (nenhum — só validação)

- [ ] **Step 1: Estrutura de arquivos**

```bash
ls -la "03-Dominios/Terminal/Workflow/" | head -20
ls "03-Dominios/Terminal/Workflow/" | wc -l
```

Esperado: 11 arquivos (10 notas + 1 MOC).

- [ ] **Step 2: Frontmatter consistente**

```bash
for f in "03-Dominios/Terminal/Workflow"/*.md; do
    echo "=== $f ==="
    head -20 "$f" | grep -E "^(title|publish|fase|tags|created|updated):"
done
```

Esperado: cada nota tem `title`, `publish: true`, `fase: iniciado|adepto|magus`, `tags`, `created: 2026-05-24`, `updated: 2026-05-24`.

- [ ] **Step 3: Estrutura H2 das notas regulares (01-09)**

```bash
for f in "03-Dominios/Terminal/Workflow"/0[1-9]\ -*.md; do
    echo "=== $f ==="
    grep "^## " "$f"
done
```

Esperado em cada uma das 9 notas regulares: `## O que é / Como funciona`, `## Na prática`, `## Armadilhas`, `## Em inglês`, `## Veja também`, `## Referências`.

- [ ] **Step 4: Estrutura do capstone (10)**

```bash
grep "^## " "03-Dominios/Terminal/Workflow/10 - Sessão ideal — anatomia de um dia keyboard-first.md"
```

Esperado: `## Cenário`, `## Fluxo (cronológico)`, `## Decisões em pontos de bifurcação`, `## Em inglês`, `## Veja também`, `## Referências`.

- [ ] **Step 5: Armadilhas count (≥4 em cada nota regular)**

```bash
for f in "03-Dominios/Terminal/Workflow"/0[1-9]\ -*.md; do
    count=$(grep -E "^[0-9]+\. \*\*" "$f" | wc -l)
    echo "$f: $count armadilhas"
done
```

Esperado: cada nota com ≥4 armadilhas.

- [ ] **Step 6: Bullets "Em inglês" (8-10 em cada nota)**

```bash
for f in "03-Dominios/Terminal/Workflow"/*.md; do
    section=$(awk '/^## Em inglês/,/^## Veja também/' "$f")
    count=$(echo "$section" | grep -E "^- \*\*" | wc -l)
    echo "$f: $count bullets"
done
```

Esperado: 8-10 bullets em cada nota.

- [ ] **Step 7: verificar-wikilinks no galho**

Usar a skill:

```text
verificar-wikilinks 03-Dominios/Terminal/Workflow
```

Esperado: 0 broken links.

- [ ] **Step 8: Dicionário consistente**

```bash
# Bloco Workflow existe
grep -E "^## Workflow$" "03-Dominios/Terminal/Dicionário do Terminal.md"

# Verbetes em ordem alfabética (case-insensitive)
awk '/^## Workflow$/,/^## /' "03-Dominios/Terminal/Dicionário do Terminal.md" | grep -E "^### " | sort -fc 2>&1
# (saída vazia = ordem alfabética correta; senão mostra primeiro fora de ordem)

# Updated bump
grep "^updated:" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: bloco existe; verbetes ordenados; `updated: 2026-05-24`.

- [ ] **Step 9: Tronco com galho 7 ativo**

```bash
grep -E "\[\[03-Dominios/Terminal/Workflow/index\|Workflow\]\]" "03-Dominios/Terminal/index.md"
grep "^progresso:" "03-Dominios/Terminal/index.md"
```

Esperado: wikilink presente; `progresso: completo`.

- [ ] **Step 10: Sem `Co-Authored-By: Claude` nos commits desta sessão**

```bash
git log --since="2 hours ago" --grep="Co-Authored-By: Claude" | head
# (saída vazia esperada)
git log --since="2 hours ago" --oneline | head -20
```

Esperado: nenhum match no grep; commits visíveis.

---

## Task 15: Cross-task review subagent

**Files:** (sem mudança — só review)

- [ ] **Step 1: Dispatch subagent (Sonnet, contexto curto)**

Usar tool Agent com:
- subagent_type: `general-purpose`
- model: `sonnet` (NÃO usar 1M context — dá erro de créditos)
- isolation: omitido (não precisa worktree pra review read-only)

Prompt do subagent:

```text
Você é um cross-task reviewer pra um galho de trilha de notas Obsidian. 11 arquivos foram escritos em `03-Dominios/Terminal/Workflow/` (10 notas + 1 MOC) + Dicionário expandido + tronco atualizado.

Sua tarefa: revisar **consistência cross-arquivo** das 11 notas + MOC + bloco "Workflow" do Dicionário.

Reporte achados em 3 categorias:

- **Critical:** quebra funcional (wikilink errado, frontmatter inválido, conteúdo contraditório entre notas)
- **Important:** desvio de padrão (callout TL;DR errado, armadilha sem 4 labels, "Em inglês" mal-formatado, ordem alfabética de verbetes errada)
- **Nice-to-have:** sugestões cosméticas (vocabulário, fluência)

Hard constraints (qualquer violação = Critical):
1. NUNCA `josenaldo` ou `/home/josenaldo/` em qualquer arquivo.
2. NUNCA `Co-Authored-By: Claude`.
3. TL;DR deve usar callout `[!abstract]`.
4. Armadilhas em notas 01-09: padrão `N. **Título**` + 4 labels (`**Causa:**`, `**Sintoma:**`, `**Como detectar:**`, `**Solução:**`).
5. Capstone (10): estrutura diferente (Cenário/Fluxo/Decisões).
6. "Em inglês": 8-10 bullets no formato `- **PT** — *EN*. "frase em PT."`. NUNCA tabela.
7. Verbetes do Dicionário em ordem alfabética case-insensitive.
8. Wikilinks SEM backticks em "Veja também".

Liste TODOS os arquivos do galho:
```bash
ls "03-Dominios/Terminal/Workflow/"
```

Use grep/Read pra inspecionar. Reporte breve (≤500 palavras), priorizando Critical/Important. Nice-to-have só se relevante.
```

- [ ] **Step 2: Aplicar fixes (se houver Critical/Important)**

Se o reviewer reportou findings:

- Critical: fix imediato.
- Important: fix imediato.
- Nice-to-have: skip (decisão do usuário).

Dispatchar SEGUNDO subagent (Sonnet, contexto curto) com prompt de fix listando ESPECIFICAMENTE cada item a corrigir. NÃO deixar o subagent decidir; passar lista verificada.

Após fixes, commitar com mensagem:

```bash
git add <arquivos-corrigidos-explicitos>
git commit -m "fix(terminal-workflow): cross-task — <resumo dos fixes>"
```

- [ ] **Step 3: Re-validar após fixes**

Re-rodar steps relevantes da Task 14.

---

## Task 16: Critério de pronto final

- [ ] 11 arquivos em `03-Dominios/Terminal/Workflow/` (10 notas + MOC)
- [ ] Notas 01-09 com TL;DR `[!abstract]`, ≥4 armadilhas no padrão completo, 8-10 bullets "Em inglês"
- [ ] Capstone (10) com estrutura própria (Cenário/Fluxo/Decisões), compondo as 9 anteriores
- [ ] `## Workflow` no Dicionário com 10-15 verbetes em ordem alfabética; `updated: 2026-05-24`
- [ ] Tronco (`Terminal/index.md`) com wikilink ativo pro galho 7; `progresso: completo`; `updated: 2026-05-24`
- [ ] `verificar-wikilinks 03-Dominios/Terminal/Workflow/` → 0 broken
- [ ] Cross-task review subagent sem Critical/Important pendentes
- [ ] Nenhum commit com `Co-Authored-By: Claude`
- [ ] Nenhum `git add -A`; apenas stages explícitos
- [ ] Reportar ao usuário: galho 7 entregue, trilha Terminal completa.

---

## Self-review (a executar antes de salvar este plano)

**1. Spec coverage:**
- ✓ 10 notas (Iniciado 3, Adepto 4, Magus 3): Tasks 2-11
- ✓ MOC do galho: Task 12
- ✓ Tronco atualizado + trilha fechada: Task 13
- ✓ Bloco Workflow no Dicionário: Task 1 (esqueleto) + verbetes nas Tasks 2-11
- ✓ Cross-task review (Sonnet): Task 15
- ✓ Validation com verificar-wikilinks: Task 14

**2. Placeholder scan:** Sem TBD/TODO/"implement later". Listas de verbetes específicas, comandos explícitos, conteúdo concreto em cada Step 3.

**3. Type consistency:**
- Convenção `git add <path>` explícita em todos os commits ✓
- Verbetes referenciados consistentes (e.g. `keyboard-first` em nota 01 + verbete + nota 09) ✓
- Padrão de armadilhas idêntico nas 9 notas regulares ✓
- MOC menciona apenas notas 01-10 (nada além) ✓
