---
title: "Modos básicos e keybindings essenciais"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
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

# Modos básicos e keybindings essenciais

> [!abstract] TL;DR
> Zellij é modal: você sempre está num modo (normal, pane, tab, etc.). Cada modo tem keybindings próprios — a status bar mostra todos. `Ctrl-<letra>` entra num modo; depois letras isoladas executam ações. Memorize 4 modos pra começar (normal, pane, tab, session) e ~20 keybindings.

---

## O que é / Como funciona

### Por que modal

Tmux usa prefixo: `Ctrl-b` + tecla. Toda ação é um chord de 2 passos a partir do mesmo ponto de entrada.

Zellij usa modos: `Ctrl-<letra>` entra num modo; dentro do modo, teclas isoladas executam ações. Os modos são estados persistentes — você continua no modo até sair explicitamente (ESC ou repetindo o `Ctrl-<letra>`).

**Vantagem do modal:** a status bar do Zellij exibe os atalhos disponíveis no modo ativo. Você não precisa decorar tudo — basta olhar a tela. A descoberta é embutida na interface.

**Desvantagem:** cada ação exige 2 passos (entrar no modo + executar) em vez de 1 chord direto. Fluxo tem uma fricção inicial até os modos virarem muscle memory.

### Os 9 modos

Os modos canônicos do Zellij default:

| Modo | Entrada | Para que serve |
|------|---------|----------------|
| **Normal** | estado inicial | Input vai direto pro shell/app. Ações Alt disponíveis. |
| **Locked** | `Ctrl-g` | Desliga todos os keybindings do Zellij. Tudo passa pro pane. Útil para Emacs, Helix, qualquer app com `Ctrl-<letra>`. |
| **Pane** | `Ctrl-p` | Split, fechar, focar, fullscreen, floating. |
| **Tab** | `Ctrl-t` | Nova tab, fechar, renomear, navegar, ir por número. |
| **Resize** | `Ctrl-n` | Redimensiona pane focado. |
| **Scroll** | `Ctrl-s` | Scrollback: subir, descer, page up/down. |
| **Search** | via Scroll + `s` | Busca regex no scrollback do pane atual. |
| **Session** | `Ctrl-o` | Detach, trocar de session, plugins de gerenciamento. |
| **Move** | `Ctrl-h` | Move o pane focado dentro do grid. |

> [!note] Modos derivados
> `EnterSearch`, `RenameTab` e `RenamePane` são estados transitórios de entrada de texto — não são modos canônicos configuráveis. Eles aparecem temporariamente enquanto você digita um nome ou termo de busca e somem ao confirmar ou cancelar.

### Como descobrir keybindings

A status bar (barra inferior do Zellij) mostra os atalhos disponíveis no modo ativo. Quando você entra em modo Pane, ela lista todas as ações de pane. Quando está em Normal, mostra os `Ctrl-<letra>` de entrada para cada modo.

Se a status bar não aparecer, verifique se `pane_frames true` está na config (valor default). O plugin `status-bar` precisa estar carregado — ele está ativo no layout default do Zellij.

### Mnemônica

Associe a letra de cada modo à sua função:

- `Ctrl-p` — **p**ane
- `Ctrl-t` — **t**ab
- `Ctrl-s` — **s**croll / **s**earch
- `Ctrl-o` — sessi**o**n
- `Ctrl-n` — re**n**size
- `Ctrl-g` — **g**rab keys (locked / passthrough)
- `Ctrl-h` — move (m**ove** usa `h` por ser a letra do movimento vim pra esquerda; `m` já era usado em outro contexto)

---

## Na prática

### Cheatsheet das 20 primeiras keybindings

Keybindings verificadas no `default.kdl` do Zellij:

| Modo | Sequência | Ação | Quando usar |
|------|-----------|------|-------------|
| (qualquer) | `Ctrl-p` | Entra modo Pane | Vai mexer em panes |
| Pane | `n` | Novo pane vertical (split direita) | Comparar dois outputs lado a lado |
| Pane | `d` | Novo pane horizontal (split abaixo) | Log ou output abaixo do editor |
| Pane | `x` | Fecha pane focado | Limpar pane que não precisa mais |
| Pane | `f` | Toggle fullscreen do pane | Foco temporário sem mudar layout |
| Pane | `w` | Toggle floating pane | Terminal extra sem destruir layout |
| Pane | `h` / `j` / `k` / `l` | Foca pane na direção (esq/baixo/cima/dir) | Navegar entre panes no modo Pane |
| Pane | `z` | Toggle pane frames | Esconder/mostrar bordas dos panes |
| (qualquer) | `Ctrl-t` | Entra modo Tab | Vai mexer em tabs |
| Tab | `n` | Nova tab | Separar contextos de trabalho |
| Tab | `x` | Fecha tab atual | Limpar contexto encerrado |
| Tab | `r` | Renomeia tab atual | Organizar tabs por projeto/tarefa |
| Tab | `h` / `l` | Tab anterior / próxima | Navegar sequencialmente |
| Tab | `[1-9]` | Vai para tab N | Atalho direto por número |
| (qualquer) | `Ctrl-o` | Entra modo Session | Operações de session |
| Session | `d` | Detach (session continua rodando) | Sair preservando o trabalho |
| Session | `w` | Abre session manager (floating) | Trocar ou listar sessions |
| (qualquer) | `Ctrl-s` | Entra modo Scroll | Ver histórico do pane |
| Scroll | `d` / `u` | Metade da página pra baixo/cima | Navegar scrollback rapidamente |
| Scroll | `s` | Entra Search mode (regex) | Buscar texto no histórico |
| (qualquer) | `Ctrl-g` | Entra/sai do modo Locked | Usar app com atalhos conflitantes |

> [!tip] Alt shortcuts em Normal mode
> Em Normal mode, algumas ações estão disponíveis sem entrar em modo:
> - `Alt-n` — novo pane (split)
> - `Alt-h` / `Alt-l` — move foco ou troca de tab (dependendo se há panes na direção)
> - `Alt-j` / `Alt-k` — move foco pane abaixo/acima
> - `Alt-f` — toggle floating pane
>
> Esses atalhos existem pra ações frequentes que não exigem entrar num modo dedicado.

### Workflow exemplo (primeiros 5 min em Zellij)

```text
1. Abrir terminal, digitar: zellij -s trabalho
   → Está em Normal mode. Digite comandos normalmente.

2. Quer um terminal à direita?
   Ctrl-p → n
   → Novo pane aparece à direita.

3. Quer navegar pro pane original?
   Ctrl-p → h   (ou Alt-h em Normal mode)
   → Foco volta pro pane esquerdo.

4. Quer ver o output completo em fullscreen?
   Ctrl-p → f
   → Pane expande. Repita Ctrl-p → f pra sair.

5. Quer separar contexto (novo projeto)?
   Ctrl-t → n
   → Nova tab. Ctrl-t → r para renomear.

6. Precisa sair mas quer preservar tudo?
   Ctrl-o → d   (detach)
   → Volta pro prompt do OS. Session continua rodando.
   → Retornar: zellij attach trabalho
```

---

## Armadilhas

### (1) Ficar no modo errado e executar ações sem querer

**Causa:** entrar em modo Pane para fazer um split, executar a ação, e esquecer que ainda está no modo Pane. Digitar `x` querendo escrever `x` no shell → o pane fecha.

**Sintoma:** pane fechou sem intenção; shell sumiu; layout mudou sem explicação.

**Como detectar:** olhar a status bar — ela mostra o modo ativo em destaque. Se não estiver em Normal, há um label colorido indicando o modo.

**Solução:** após qualquer ação num modo, checar se voltou pra Normal (ESC ou repetir `Ctrl-<modo>`). Prática: ao terminar uma ação em modo Pane, pressionar ESC conscientemente até criar o hábito.

---

### (2) Usar Locked achando que "trava o cursor" ou "pausa o pane"

**Causa:** o nome "locked" sugere imobilidade. Na realidade, Locked significa que os keybindings do Zellij estão desativados — o input continua chegando ao pane normalmente.

**Sintoma:** entrar em Locked esperando que o pane pare de receber input, ficar confuso que ele continua funcionando.

**Como detectar:** a status bar mostra "LOCKED" e lista apenas o atalho de saída (`Ctrl-g`).

**Solução:** usar Locked exclusivamente quando um app roda dentro do Zellij e precisa de atalhos que conflitam com o Zellij (Emacs `Ctrl-p`, Helix, etc.). Para simplesmente parar de interagir com um pane, apenas pare de digitar.

---

### (3) Status bar desligada — não saber em qual modo está

**Causa:** config customizada sem o plugin `status-bar`, ou `pane_frames false` sem substituição visual.

**Sintoma:** Zellij abre sem barra inferior; usuário entra num modo sem perceber; ações estranhas acontecem.

**Como detectar:** se não há barra na parte inferior mostrando modo e atalhos, o plugin status-bar não está ativo.

**Solução:** no Zellij stock (sem config customizada), o plugin está ativo por default. Para reativar: incluir o plugin `status-bar` no layout KDL, ou usar `zellij --layout default` para garantir o layout padrão.

---

### (4) Muscle memory de tmux — esperar `Ctrl-b` como prefixo

**Causa:** quem vem do tmux está habituado a `Ctrl-b <key>` como chord único. No Zellij, `Ctrl-b` não é o prefixo padrão — os modos são entrados com `Ctrl-p`, `Ctrl-t`, etc.

**Sintoma:** digitar `Ctrl-b n` esperando nova janela, e nada acontece (ou o `n` vai pro shell).

**Como detectar:** o Zellij tem um modo `Tmux` opcional (ativável via config) que emula o prefixo `Ctrl-b`. Se esse modo não estiver ativo, os atalhos do tmux não funcionam.

**Solução:** treinar os modos do Zellij separadamente. Alternativamente, ativar o modo `Tmux` no config para período de transição. A longo prazo, os modos do Zellij são mais descobríveis pelo auxílio da status bar.

---

### (5) Esperar que `h/j/k/l` funcionem em Normal mode para navegar panes

**Causa:** em editores modais (Neovim, Helix), `hjkl` movem o cursor em Normal mode. No Zellij, Normal mode passa todo input pro shell — `h`, `j`, `k`, `l` escrevem as letras no shell.

**Sintoma:** digitar `h` em Normal mode esperando mover o foco, e a letra aparecer no shell.

**Como detectar:** olhar o shell — se a letra aparece no prompt, você está em Normal mode.

**Solução:** para navegar entre panes: entrar em modo Pane (`Ctrl-p`) e usar `hjkl`, ou usar `Alt-h`/`Alt-l`/`Alt-j`/`Alt-k` em qualquer modo (esses atalhos funcionam em Normal sem entrar em Pane).

---

### (6) Confundir `Ctrl-p f` (fullscreen) com `Ctrl-p z` (toggle pane frames)

**Causa:** em tmux, `Ctrl-b z` é o zoom/fullscreen. A associação letra-ação diverge no Zellij.

**Sintoma:** pressionar `Ctrl-p z` esperando fullscreen e as bordas dos panes somem/aparecem.

**Como detectar:** `z` em modo Pane executa `TogglePaneFrames` (esconde/mostra as bordas visuais dos panes); `f` executa `ToggleFocusFullscreen` (expande 1 pane pra ocupar toda a área).

**Solução:** memorizar: `f` = **f**ullscreen em modo Pane. O status bar mostra o mapeamento correto.

---

## Em inglês

- **modal** — *modal*. "modo de software que opera em estados distintos onde as teclas têm significado diferente."
- **mode** — *mode*. "estado que define como o input é interpretado; no Zellij, ativado via `Ctrl-<letra>`."
- **keybinding** — *keybinding*. "associação de uma combinação de teclas com uma ação."
- **shortcut** — *shortcut*. "atalho de teclado pra uma ação; uso coloquial de keybinding."
- **chord** — *chord*. "sequência de teclas pressionadas em ordem pra ativar um comando (ex.: `Ctrl-b n` no tmux)."
- **discoverability** — *discoverability*. "qualidade de uma UI de mostrar suas opções disponíveis sem precisar decorar; o status bar do Zellij é projetado pra isso."
- **status bar** — *status bar*. "barra inferior do Zellij que exibe o modo atual e os keybindings disponíveis."
- **passthrough** — *passthrough*. "modo onde o input passa direto pro app dentro do pane sem ser interceptado pelo multiplexer; ativado no modo Locked."
- **muscle memory** — *muscle memory*. "memória motora dos atalhos adquirida pela repetição, sem esforço consciente."
- **cheatsheet** — *cheatsheet*. "tabela de referência rápida listando sequências de teclas e suas ações."

---

## Veja também

- [[02 - Modelo mental — sessions, tabs, panes]] — o que os modos manipulam (sessions, tabs, panes)
- [[04 - Sessões persistentes — detach, attach, gerenciamento]] — modo Session em profundidade
- [[06 - Modos avançados, plugins e copy-mode]] — Locked, Scroll, Search avançados e plugins de status bar
- [[03-Dominios/Tecnologia/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Mode (Zellij)|mode]], [[Dicionário do Terminal#Status bar|status bar]]

---

## Referências

- [Zellij — Keybindings](https://zellij.dev/documentation/keybindings)
- [Zellij default.kdl](https://github.com/zellij-org/zellij/blob/main/zellij-utils/assets/config/default.kdl)
