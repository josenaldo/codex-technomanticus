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

# Ergonomia das mãos

> [!abstract] TL;DR
> Ergonomia importa pra evitar RSI e cansaço. Princípios: leader keys cross-tool (`<Space>` no nvim, prefix no Zellij), CapsLock→Ctrl (mão esquerda agradece), atalhos consistentes que valem aprender (10+ uses/dia). Customizar com critério, não por estética. Pausas e postura > customização hardcore.

## O que é / Como funciona

### O problema das contorções

`Ctrl-Shift-X` no teclado padrão exige mão esquerda em garra — polegar no Ctrl, mínimo no Shift, anelar/médio no X. Repetir esse combo dezenas de vezes por hora é receita de RSI em meses.

O princípio central: **atalho frequente DEVE ser barato** — 1 ou 2 dedos, sem estiramento, sem torção do pulso. Se você faz algo 20x/dia e custa 3 dedos contorcidos, é um candidato imediato a remap.

### Leader keys cross-tool

Uma **leader key** é uma tecla "raiz" que abre um namespace de atalhos. Em vez de `Ctrl-Shift-F` pra find file, você aperta `<Space>` (leader) e depois `ff` — dois toques leves na home row.

Defaults comuns:

| Ferramenta | Leader / Prefix | Observação |
|---|---|---|
| nvim (LazyVim) | `<Space>` | Padrão moderno, home row |
| Zellij | `Ctrl-G` | Configurável; responsivo |
| tmux | `Ctrl-B` | Default; muitos rebindam pra `Ctrl-A` |

Vantagem: namespace infinito sem depender de Ctrl/Alt/Shift. `<leader>ff` (find file), `<leader>fg` (live grep), `<prefix>n` (new tab) — expansível sem conflito.

### CapsLock como modificador

CapsLock fica em posição privilegiada: home row, mão esquerda, facilmente alcançável sem desvio. Por default faz apenas toggle de maiúsculas — uso real: quase zero. Remapear pra Ctrl é o ganho ergonômico de maior impacto/esforço disponível.

Depois do remap: `Ctrl-A`, `Ctrl-E`, `Ctrl-R` passam a custar um dedo só (dedo mindinho na posição natural). Comparado com esticar o mindinho até o canto inferior esquerdo do teclado, é transformador.

### Atalhos consistentes — princípios

**Vim grammar como língua franca:** `hjkl` funcionam em nvim, `less`, `bat`, `fzf`, `atuin`. Aprender uma vez, usar em todo lugar.

**Leader+letter pra ações de domínio:** `<leader>ff` find file em nvim, `<prefix>n` new tab em Zellij — padrão que o cérebro reconhece como "letra depois da raiz".

**NÃO override defaults sem motivo:** `dd` deletar linha é universal. O nvim do servidor remoto não terá seu keymap customizado. Se você sobrescreve algo canônico, vai errar no ambiente "nu".

### Pausas e postura

Nenhum keymap elimina o problema de trabalhar 6h sem parar. A ergonomia física é incontornável:

- **Pomodoro 25+5:** 25 min de foco, 5 min de pausa. Timer no Zellij (`zellij run -- timer`) ou app dedicado.
- **Regra 20-20-20:** a cada 20 minutos, 20 segundos olhando pra algo a 20 metros (alivia tensão ocular).
- **Postura:** punhos neutros (sem flexão pra cima/baixo), cotovelos a ~90°, monitor à altura dos olhos.
- **Alongamento básico:** rotação de pulso (10x cada direção), abrir/fechar mãos com força, girar ombros.

---

## Na prática

### Remapear CapsLock pra Ctrl (Linux/X11)

```bash
# Sessão atual (teste rápido)
setxkbmap -option ctrl:nocaps

# Persistente — adicionar em ~/.xprofile ou ~/.xsession
echo 'setxkbmap -option ctrl:nocaps' >> ~/.xprofile
```

Ou via `/etc/default/keyboard` (Debian/Ubuntu): adicionar `ctrl:nocaps` em `XKBOPTIONS`.

### Remapear CapsLock (Linux/Wayland)

```bash
# GNOME
gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"

# KDE: System Settings > Keyboard > Advanced > Caps Lock behavior
# Selecionar: "Caps Lock is Ctrl"
```

### Remapear CapsLock (macOS)

```text
System Preferences > Keyboard > Modifier Keys...
Caps Lock Key: ^ Control
```

### Verificar o remap

```bash
# Pressione CapsLock; deve exibir "Control_L" no output
xev | grep -A2 keysym
```

### Atalhos que VALEM aprender (10+ uses/dia)

```text
# nvim / LazyVim
<leader>ff   — find file (fuzzy)
<leader>fg   — live grep (busca em conteúdo)
gd           — goto definition
<C-o>        — voltar ao ponto anterior (jump list)

# zsh / bash (com CapsLock→Ctrl)
Ctrl-R       — busca no histórico (atuin ou fzf)
Alt-.        — insere último argumento do comando anterior
Ctrl-A       — início da linha
Ctrl-E       — fim da linha
Ctrl-W       — apaga palavra anterior

# Zellij
<prefix>n    — nova tab
<prefix>p    — tab anterior
<prefix>h/l  — tab anterior/próxima (se configurado)
```

### Atalhos que NÃO valem (usa 1-2x/semana)

- Tudo que envolve `Ctrl-Shift-Alt-letra` — custo motor alto, recall baixo
- Macros raros que copiou de um blog — memória vaza em semanas
- Atalhos IDE-specific que você usa só nesse projeto

Critério simples: se não usou 3x nos últimos 7 dias, remova o mapeamento.

---

## Armadilhas

1. **CapsLock→Ctrl quebra em algumas ferramentas** — Causa: software que detecta CapsLock por nome de tecla (raro, mas existe em certos apps de terminal ou jogos). Sintoma: uma app específica não aceita o Ctrl remapeado. Como detectar: quase nunca ocorre — se acontecer, questione "essa app é crítica pro meu trabalho?". Solução: revert seletivo via config por-app, ou aceitar o trade-off (CapsLock real ainda acessível via `Shift-CapsLock` em alguns layouts). `[ergonomia]` `[teclado]`

2. **Custom keybindings pesadas no leader space** — Causa: querer mapear absolutamente tudo. Sintoma: 30+ keymaps em `keymaps.lua`; frequentemente você não lembra o que existe. Como detectar: abrir o arquivo e contar entradas — mais de 20 é sinal de alerta. Solução: princípio "10+ uses/dia ou não entra"; revisão a cada 3 meses pra remover o que não usou. `[config]` `[nvim]`

3. **Atalhos conflitam entre nvim e Zellij** — Causa: `Ctrl-H` em nvim (vim-tmux-navigator) navega pra pane esquerdo, mas Zellij captura o combo antes do nvim receber. Sintoma: atalho funciona em um contexto, falha misteriosamente em outro. Como detectar: qualquer keybinding "que às vezes funciona" é candidata. Solução: estabelecer ordem de precedência (multiplexer geralmente captura antes do editor); o plugin `vim-zellij-navigator` resolve o caso específico nvim+Zellij. `[conflito]` `[zellij]`

4. **Trabalhar em maratona sem pausa** — Causa: estado de flow ("não posso parar agora"). Sintoma: após semanas/meses, dor cotidiana no pulso, antebraço ou cotovelo que aparece no fim do dia e some com repouso — esse padrão é warning precoce de RSI. Como detectar: qualquer dor pós-trabalho recorrente. Solução: Pomodoro é não-negociável; configurar timer visível no status bar do Zellij ou usar app dedicado. `[saúde]` `[RSI]`

---

## Em inglês

- **ergonomia** — *ergonomics*. "Ergonomics is the science of designing tools and workflows to fit the human body."
- **leader key** — *leader key*. "In Vim, the leader key opens a custom namespace so you avoid modifier-heavy chords."
- **tecla prefixo** — *prefix key*. "Tmux uses a prefix key (Ctrl-B by default) before every pane and window command."
- **tecla modificadora** — *modifier key*. "Ctrl, Alt, and Shift are modifier keys — they change the meaning of the next key pressed."
- **mapeamento de tecla** — *keybinding / key mapping*. "Setting a keybinding for 'find file' saves dozens of keystrokes per session."
- **mapa de teclas** — *keymap*. "Your keymap is the full table of custom bindings loaded by the editor on startup."
- **lesão por esforço repetitivo** — *RSI (Repetitive Strain Injury)*. "RSI is one of the most common occupational injuries among software developers."
- **postura** — *posture*. "Neutral wrist posture means your forearm and hand form a straight line while typing."
- **pulso neutro** — *neutral wrist*. "A neutral wrist position reduces tension on the tendons that pass through the carpal tunnel."
- **memória muscular** — *muscle memory*. "After two weeks of daily use, the remapped CapsLock feels completely natural — that's muscle memory."

---

## Veja também

- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Editor/02 - Motions, operadores e text objects|Motions Vim (galho 1)]]
- [[03-Dominios/Terminal/Shell/07 - ZLE|ZLE (galho 2)]]
- [[03-Dominios/Terminal/Multiplexer/03 - Modos básicos e keybindings essenciais|Keybindings Zellij (galho 3)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#leader key|leader key]]
- [[Dicionário do Terminal#RSI|RSI]]

## Referências

- OSHA — Computer Workstations: <https://www.osha.gov/ergonomics/computer-workstations>
