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

# Modelo mental — sessions, tabs, panes

> [!abstract] TL;DR
> Zellij organiza tudo em 3 níveis: 1 server roda em background → N sessions nomeadas sobrevivem a detach → cada session tem N tabs → cada tab tem N panes (split, stacked, floating). Você sempre interage com 1 pane ativo; troca de pane/tab/session via keybindings.

## O que é / Como funciona

### Hierarquia

A estrutura completa do Zellij em árvore:

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

Cada nível tem responsabilidade distinta:

- **Server** — processo de fundo; persiste enquanto há sessions ativas.
- **Session** — container nomeado; sobrevive a detach.
- **Tab** — agrupamento de panes dentro de uma session; cada tab tem seu próprio layout.
- **Pane** — divisão terminal dentro de uma tab; recebe e exibe output de 1 processo.

### Server

O server do Zellij é iniciado automaticamente na primeira invocação de `zellij`. Ele roda como processo separado e cada cliente (emulador, SSH) comunica com ele via Unix socket. Há 1 server por usuário por default.

```bash
# Verificar se o server está rodando
ps aux | grep zellij

# Matar todas as sessions com SIGKILL (e o server junto, se não houver mais clients)
zellij kill-all-sessions

# Remover graciosamente todas as sessions (coberto em nota 04)
zellij delete-all-sessions
```

Não é necessário iniciar o server manualmente. Ele sobe junto com `zellij` ou `zellij -s <nome>`.

### Session

Uma session é um container nomeado que agrupa tabs e panes. Ela **sobrevive** a fechar o emulador de terminal, a uma queda de conexão SSH, ou a um `detach` explícito — os processos rodando dentro continuam ativos.

```bash
# Listar sessions ativas
zellij ls
# Saída típica:
# myproj [Created 12m ago]
# default [Created 3h ago] (EXITED - attach to resurrect)

# Criar session com nome específico
zellij -s myproj

# Anexar a uma session existente
zellij attach myproj

# Deletar session específica
zellij delete-session myproj

# Deletar todas as sessions
zellij delete-all-sessions
```

Sem `-s`, o Zellij gera um nome aleatório (ex.: `quirky-llama`). Nomear sessions explicitamente com `-s` facilita reattach posterior.

Uma session com status `EXITED` significa que todos os panes foram fechados, mas o container ainda existe no server. `zellij attach <nome>` a "ressuscita".

### Tab

Tabs são agrupamentos horizontais de panes dentro de uma session. Cada tab mantém seu próprio layout, independente das outras. O nome aparece na barra superior do Zellij e pode ser renomeado.

Operações básicas de tab:

- `Ctrl-t` — entra no modo Tab
- `Ctrl-t n` — nova tab
- `Ctrl-t r` — renomear tab atual
- `Ctrl-t x` — fechar tab atual (fecha todos os panes nela)
- `Ctrl-t [1-9]` — ir para tab por número

Tabs do Zellij são diferentes de tabs do emulador de terminal (kitty, WezTerm, etc.): as tabs do Zellij vivem dentro da session e persistem com ela; as tabs do emulador são janelas do OS que não sobrevivem a fechar o emulador.

### Pane — 3 tipos

Um pane é a unidade básica de trabalho: um retângulo de terminal rodando um shell ou comando. O pane ativo recebe input do teclado; os outros continuam executando em background.

#### Split pane

Divisão padrão. Ocupa um retângulo fixo no grid da tab. Pode ser criado na vertical (lado a lado) ou na horizontal (acima/abaixo).

```bash
# Dentro do Zellij — modo Pane (Ctrl-p):
# Ctrl-p n  — novo pane split vertical (direita)
# Ctrl-p d  — novo pane split horizontal (abaixo)
```

#### Floating pane

Pane sobreposto ao grid, sem ocupar espaço dos outros panes. Pode ser movido e redimensionado livremente com mouse ou keybindings. Útil para consultar `man`, rodar um comando rápido ou abrir um segundo shell sem alterar o layout.

```bash
# Ctrl-p w  — toggle floating pane (abre ou fecha o painel flutuante)
# Mouse: arrastar a borda para redimensionar, arrastar o título para mover
```

Floating pane não tem comportamento de "suspend" nativo — fechar é permanente (o processo termina).

#### Stacked pane

Modo de agrupamento onde múltiplos panes ficam empilhados na mesma área: 1 pane expandido ocupa o espaço inteiro e os outros aparecem apenas como barra de título (minimizados). Útil para monitorar vários logs ou jobs sem perder referência de quais estão rodando.

```bash
# Ctrl-p s  — toggle stacked mode na tab atual
```

No stacked mode, navegar entre panes com `Alt ↑` / `Alt ↓` alterna qual pane está expandido.

### Lifecycle: detach vs close

Entender a diferença entre "desanexar" e "fechar" é crucial para não perder trabalho.

| Ação | O que acontece | Keybinding |
|---|---|---|
| **Detach** | Session continua no server; processos seguem rodando; você volta ao prompt do OS | `Ctrl-o` → `d` |
| **Close pane** | Processo do pane recebe SIGTERM e termina; pane desaparece | `Ctrl-p` → `x` |
| **Close tab** | Todos os panes da tab fecham (SIGTERM em cada processo) | `Ctrl-t` → `x` |
| **Quit session** | Session inteira é encerrada; todos os processos terminam | `Ctrl-q` |

> [!warning] Detach preserva; close destrói
> `Ctrl-q` mata a session. `Ctrl-o d` apenas desanexa — a session segue rodando. Confundir os dois é a armadilha mais comum ao começar com Zellij.

Floating pane "minimizado" não é um estado nativo do Zellij: não há suspend de floating pane. Para "esconder" um floating pane, use `Ctrl-p w` (toggle) — isso fecha o painel (e o processo termina). Se precisar preservar o estado, use um split pane ou stacked pane.

---

## Na prática

### Criar a hierarquia

```bash
# Iniciar session nomeada
zellij -s myproj

# Dentro do Zellij:
# Nova tab
Ctrl-t n

# Split pane à direita (vertical)
Ctrl-p n

# Split pane abaixo (horizontal)
Ctrl-p d

# Abrir floating pane
Ctrl-p w

# Toggle stacked mode
Ctrl-p s
```

Para navegar entre panes sem entrar em modo Pane:

```bash
# Navegar com Alt + seta (modo Normal)
Alt ←  # pane à esquerda
Alt →  # pane à direita
Alt ↑  # pane acima
Alt ↓  # pane abaixo
```

### Inspecionar sessions sem entrar

```bash
zellij ls
# Saída:
# myproj   [Created 12m ago]
# default  [Created 3h ago] (EXITED - attach to resurrect)
```

A flag `(EXITED)` indica que todos os panes fecharam, mas a session ainda existe no server e pode ser reativada com `attach`.

Para ver mais detalhes sobre uma session específica:

```bash
zellij attach --create myproj
# Cria a session se não existir, ou anexa se já existir
```

### Mental model rápido

Use este guia para decidir qual nível usar:

- **Quer separar projetos completamente?** → 1 session por projeto (`zellij -s <projeto>`).
- **Quer separar "fases de trabalho" dentro do mesmo projeto?** → tabs (`Ctrl-t n`).
- **Quer ver várias coisas ao mesmo tempo no mesmo contexto?** → splits (`Ctrl-p n` / `Ctrl-p d`).
- **Quer um terminal extra sem mexer no layout atual?** → floating (`Ctrl-p w`).
- **Quer 5 logs visíveis mas só interagir com 1 de vez?** → stacked (`Ctrl-p s`).

---

## Armadilhas

### (1) Confundir "fechar o emulador" com "matar a session"

**Causa:** quem vem de trabalhar sem multiplexer associa "fechar o terminal" com "encerrar tudo". No Zellij, fechar o emulador (kitty, WezTerm, etc.) apenas desanexa o cliente — a session continua rodando no server.

**Sintoma:** abrir um novo emulador, digitar `zellij`, e encontrar uma segunda session criada enquanto a anterior ainda existe. Acúmulo silencioso de sessions.

**Como detectar:** `zellij ls` mostra sessions ativas além da atual.

**Solução:** ao terminar o trabalho, use `Ctrl-q` para encerrar a session explicitamente. Ou `zellij delete-session <nome>` de fora. Para checar e limpar: `zellij delete-all-sessions` (cuidado: destrói tudo).

---

### (2) Acumular sessions abandonadas

**Causa:** cada `zellij` sem `-s` cria uma nova session com nome aleatório. Após algumas semanas de uso, podem existir dezenas de sessions com nomes como `fervent-robin` ou `calm-lobster`.

**Sintoma:** `zellij ls` lista muitas sessions desconhecidas, algumas marcadas como `EXITED`.

**Como detectar:** `zellij ls | wc -l` — se o número for muito maior que o esperado, há acúmulo.

**Solução:** adotar o hábito de usar `-s <nome>` sempre. Limpar periodicamente com `zellij delete-all-sessions` (quando não há trabalho ativo em nenhuma) ou deletar sessions individualmente: `zellij delete-session <nome>`.

---

### (3) Achar que floating pane sobrevive ao detach de forma diferente

**Causa:** floating é só uma escolha de layout (renderização sobreposta), não um lifecycle separado.

**Sintoma:** você espera que ao reanexar a session, floating pane apareça "minimizado" ou em estado diferente do split.

**Como detectar:** detach (`Ctrl-o d`) com floating aberto; reattach e olhar layout.

**Solução:** floating volta exatamente onde estava — mesma posição, mesmo tamanho. Lifecycle idêntico ao split. Não existe "suspended floating" nativo.

---

### (4) Esperar que zoom/maximize seja o mesmo que stacked

**Causa:** em editores e WMs (window managers), "maximize" é uma ação temporária: expande e depois volta ao tamanho anterior. Stacked parece visualmente similar.

**Sintoma:** entrar em stacked mode esperando que seja um toggle rápido de "ver esse pane em fullscreen e voltar", mas descobrir que é uma organização permanente de agrupamento.

**Como detectar:** `Ctrl-p s` muda o layout estruturalmente. Sair requer outro `Ctrl-p s` (toggle).

**Solução:** para zoom/fullscreen temporário em Zellij, use o modo Pane com `Ctrl-p f` (toggle fullscreen do pane focado) — isso expande 1 pane sem reorganizar o layout. Stacked é para agrupamento permanente de panes relacionados.

---

### (5) Confundir tab Zellij com tab do emulador de terminal

**Causa:** o conceito de "tab" existe tanto no Zellij quanto no emulador de terminal. Como os dois podem estar visíveis na mesma tela, é fácil operar no nível errado.

**Sintoma:** criar uma nova tab com o atalho do emulador (ex.: `Ctrl-Shift-t` no kitty) em vez de `Ctrl-t n` do Zellij, criando uma janela do emulador desconectada da session Zellij.

**Como detectar:** a tab criada pelo emulador mostra o prompt sem a interface do Zellij (sem status bar, sem tab bar do Zellij).

**Solução:** dentro do Zellij, sempre usar `Ctrl-t n` para criar tabs. Tabs do emulador (fora do Zellij) são para ter múltiplos contextos completamente independentes (ex.: uma tab com Zellij e outra com um script de setup).

---

## Em inglês

- **sessão** — *session*. "Attach to a named session to resume exactly where you left off."
- **painel** — *pane*. "Split the current pane horizontally to open a second shell side by side."
- **aba** — *tab*. "Each tab holds an independent pane layout within the same session."
- **desanexar** — *detach*. "Detach from the session before closing your laptop — it keeps running."
- **anexar** — *attach*. "Attach to the session by name: `zellij attach myproj`."
- **dividir** — *split*. "Split a pane vertically with `Ctrl-p n`; the new pane shares the same tab."
- **flutuante** — *floating*. "A floating pane overlays the grid without displacing other panes."
- **empilhado** — *stacked*. "Stacked panes share a single area; only one is expanded at a time."
- **servidor** — *server*. "The Zellij server runs in the background and persists across client connections."
- **primeiro plano** — *foreground*. "Bring a stacked pane to the foreground with `Alt ↑` / `Alt ↓`."

---

## Veja também

- [[01 - Zellij vs tmux vs screen]] — overview do Zellij e comparação com tmux/screen
- [[03 - Modos básicos e keybindings essenciais]] — como criar e navegar entre panes/tabs
- [[04 - Sessões persistentes — detach, attach, gerenciamento]] — lifecycle de sessions em profundidade
- [[05 - Layouts declarativos em KDL]] — definir hierarquia de panes em arquivo KDL
- [[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Session (Zellij)|session]], [[Dicionário do Terminal#Tab (Zellij)|tab]], [[Dicionário do Terminal#Pane|pane]], [[Dicionário do Terminal#Floating pane|floating pane]], [[Dicionário do Terminal#Stacked pane|stacked pane]]

---

## Referências

- [Zellij — Panes](https://zellij.dev/documentation/panes)
- [Zellij — Tabs](https://zellij.dev/documentation/tabs)
- [Zellij — Sessions](https://zellij.dev/documentation/sessions)
