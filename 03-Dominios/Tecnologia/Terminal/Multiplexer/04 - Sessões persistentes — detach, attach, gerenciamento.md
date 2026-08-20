---
title: "Sessões persistentes — detach, attach, gerenciamento"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
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

# Sessões persistentes — detach, attach, gerenciamento

> [!abstract] TL;DR
> Sessions são o motor de persistência. `zellij` cria/anexa default; `-s <nome>` nomeia; `zellij ls` lista; `attach <nome>` reconecta; `delete-session <nome>` remove. Detach via `Ctrl-o d` — server segue rodando, comandos seguem executando, layouts preservados. Workflow recomendado: 1 session por projeto, auto-attach no shell start.

---

## O que é / Como funciona

### O que persiste

Ao fazer detach de uma session, o server do Zellij continua rodando em background. Tudo que estava ativo permanece intacto até o próximo attach:

- Layout de tabs/panes ✓
- Comandos rodando em cada pane ✓
- Scrollback de cada pane ✓ (até limite configurável)
- Working directory de cada pane ✓
- Variáveis de ambiente das shells ✓
- Conexões SSH abertas dentro de panes ✓

### O que NÃO persiste

A persistência do Zellij depende do server estar vivo. Três situações destroem tudo:

- Reboot da máquina (server morre junto)
- `zellij kill-all-sessions` (encerra o server quando não há mais sessions)
- SIGKILL direto no processo do server

Não há mecanismo nativo equivalente ao `tmux-resurrect` — o Zellij não grava estado em disco para restaurar após reboot.

### Comandos canônicos

```bash
# Criar session nomeada (ou entrar na default sem nome)
zellij -s myproj

# Listar sessions
zellij ls
# Saída típica:
# myproj        [Created 2h ago] (current)
# brave-otter   [Created 5d ago] (EXITED - attach to resurrect)

# Anexar a session existente
zellij attach myproj

# Criar se não existir (idempotente)
zellij attach --create myproj

# Detach de dentro da session (keybinding — não é comando shell):
# Ctrl-o → d    (entrar no modo Session, pressionar d)

# Kill session — mata o processo; entry fica EXITED (pode ressuscitar via attach)
zellij kill-session myproj

# Kill todas as sessions (pede confirmação)
zellij kill-all-sessions
zellij kill-all-sessions --yes    # pula confirmação

# Delete session — remove de vez do registro
zellij delete-session myproj
zellij delete-session myproj --force   # mata antes se ainda anexada

# Delete todas as sessions
zellij delete-all-sessions
zellij delete-all-sessions --yes       # pula confirmação
zellij delete-all-sessions --force     # mata sessions ativas antes de deletar
```

### Kill vs Delete

São dois verbos distintos com semântica diferente — não são sinônimos:

| Comando | O que faz | Entry permanece? | Ressuscitável? |
|---|---|---|---|
| `kill-session <nome>` | Encerra o processo da session | Sim — fica EXITED | Sim — `attach` ressuscita |
| `delete-session <nome>` | Remove a session do registro | Não — apagada | Não |
| `delete-session <nome> --force` | Mata se ativa, depois remove | Não | Não |

`kill` é mais conservador: o processo morre, mas a entry persiste como EXITED — você pode ressuscitar o layout via `zellij attach`. `delete` é destrutivo: remove completamente.

### Resume vs new

Ao fazer `zellij attach` numa session EXITED, o Zellij a "ressuscita":

- **O que retorna:** layout de tabs e panes, estrutura visual.
- **O que se perde:** output dos comandos que rodavam (os processos morreram quando a session foi killed); o scrollback do período EXITED.

Distinguir: layout retorna, histórico de output não. É diferente de simplesmente ter feito detach — um detach preserva tudo intacto.

---

## Na prática

### 1 session por projeto

O padrão mais produtivo: uma session nomeada por projeto ou contexto de trabalho.

```bash
# Alias útil no .zshrc/.bashrc
alias z='zellij attach --create'

# Uso diário
z myproj
z backend
z notes
z infra
```

O alias `z` é idempotente: cria a session se não existir, anexa se já estiver rodando. Sem surpresa de nome aleatório.

### Auto-attach default (shell init)

Para entrar automaticamente numa session ao abrir o terminal:

```bash
# ~/.zshrc — só se for TTY interativa e já não estiver dentro do Zellij
if [[ -z "$ZELLIJ" ]] && [[ -t 0 ]] && [[ -t 1 ]]; then
  zellij attach --create default
fi
```

A variável `$ZELLIJ` está setada quando você já está dentro de uma session — o `if` previne sessões aninhadas.

Config complementar para que fechar a janela faça detach em vez de matar:

```kdl
// ~/.config/zellij/config.kdl
on_force_close "detach"
```

### Cleanup periódico

Sessions EXITED acumulam sem auto-cleanup. Routine de manutenção:

```bash
# Ver o estado atual
zellij ls

# Saída:
# myproj        [Created 2h ago]
# brave-otter   [Created 5d ago] (EXITED - attach to resurrect)
# old-task      [Created 3w ago] (EXITED - attach to resurrect)

# Deletar sessions EXITED antigas individualmente
zellij delete-session brave-otter
zellij delete-session old-task

# Ou deletar tudo de uma vez (cuidado: sessions ativas também)
zellij delete-all-sessions --yes
```

---

## Armadilhas

### (1) Typo em `attach` cria session nova com nome errado

**Causa:** `zellij attach --create myporj` (typo) não encontra `myproj` e cria uma session nova com o nome digitado errado.

**Sintoma:** você acha que voltou pro projeto, mas está numa session vazia com nome diferente. A session original segue rodando em paralelo.

**Como detectar:** `zellij ls` mostra duas sessions — a correta e a recém-criada.

**Solução:** usar `zellij attach myproj` sem `--create` para confirmar que a session existe antes; ou aceitar que typos viram sessions e fazer cleanup com `zellij delete-session`.

---

### (2) Detach confundido com encerrar a session

**Causa:** `Ctrl-o d` desconecta o cliente mas a session segue rodando no server — para quem não conhece multiplexers, parece que a session morreu.

**Sintoma:** reabrir o terminal, digitar `zellij`, e encontrar uma segunda session criada em vez de reanexar a anterior.

**Como detectar:** `zellij ls` mostra a session anterior ainda ativa, enquanto a nova é a recém-criada.

**Solução:** ao abrir o terminal depois de um detach, usar `zellij attach <nome>` ou `zellij ls` antes de criar algo novo.

---

### (3) Server crash leva todas as sessions

**Causa:** as sessions vivem no processo server do Zellij. Se o server morrer (reboot, SIGKILL, crash), todas as sessions morrem junto — não há checkpoint em disco.

**Sintoma:** após reboot ou crash, `zellij ls` retorna vazio; todo o trabalho (comandos, scrollback) se foi.

**Como detectar:** `zellij ls` vazio após reinício inesperado.

**Solução:** aceitar que Zellij não tem resurreição pós-reboot nativa. Usar layouts KDL ([[05 - Layouts declarativos em KDL]]) para recriar o ambiente em segundos. Trabalho crítico deve ser salvo no editor, não só no scrollback.

---

### (4) Sessions EXITED acumulando silenciosamente

**Causa:** quando todos os panes de uma session fecham (e.g. shell exited), a session não é removida automaticamente — fica como EXITED. Sem limpeza periódica, acumula indefinidamente.

**Sintoma:** `zellij ls` lista dezenas de sessions antigas, todas EXITED, com nomes aleatórios ou de projetos encerrados.

**Como detectar:** `zellij ls | grep EXITED | wc -l` — se o número crescer, há acúmulo.

**Solução:** rotina de cleanup: `zellij delete-session <nome>` individualmente, ou `zellij delete-all-sessions` quando não há trabalho ativo em nenhuma session.

---

### (5) Múltiplos clients na mesma session replicam input

**Causa:** Zellij permite múltiplos clientes conectados à mesma session simultaneamente — input de qualquer cliente é enviado ao pane ativo, e output é replicado para todos os clientes.

**Sintoma:** você abre o terminal, reanexe a session, e percebe que outra janela (ou outro SSH) também está controlando os mesmos panes — teclado de ambas as janelas escrevem na mesma shell.

**Como detectar:** olhar se `zellij ls` mostra `(current)` em dois terminais ao mesmo tempo para a mesma session.

**Solução:** comportamento intencional e útil para pair programming ou mostrar output pra alguém. Se não quiser múltiplos clientes: fazer detach no cliente antigo antes de anexar no novo, ou usar `zellij delete-session <nome> --force` para forçar saída de todos os clientes antes de reentrar.

---

## Em inglês

- **session** — *session*. "container nomeado que sobrevive a detach."
- **anexar** — *attach*. "reconectar a uma session em background."
- **desanexar** — *detach*. "sair da session sem matar o server."
- **persistente** — *persistent*. "que sobrevive a fechar o emulador ou a uma queda de conexão."
- **ressuscitar** — *resurrect*. "reativar uma session EXITED via attach, recuperando o layout."
- **idempotente** — *idempotent*. "operação que produz o mesmo resultado independente de quantas vezes é executada; `attach --create` é idempotente."
- **limpeza** — *cleanup*. "remover sessions obsoletas acumuladas; feito com `delete-session`."
- **matar** — *kill*. "encerrar o processo da session; entry permanece EXITED, ressuscitável."
- **deletar** — *delete*. "remover a session completamente do registro; não ressuscitável."
- **retomar** — *resume*. "continuar uma session interrompida; attach numa session EXITED ressuscita o layout."

---

## Veja também

- [[02 - Modelo mental — sessions, tabs, panes]] — hierarquia de server → session → tab → pane
- [[03 - Modos básicos e keybindings essenciais]] — modo session (Ctrl-o) e keybinding de detach
- [[05 - Layouts declarativos em KDL]] — usar layouts em vez de depender de resurrect
- [[03-Dominios/Tecnologia/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Session (Zellij)|session]], [[Dicionário do Terminal#Attach|attach]], [[Dicionário do Terminal#Detach|detach]]

---

## Referências

- [Zellij — Sessions](https://zellij.dev/documentation/sessions)
- [Zellij — Commands](https://zellij.dev/documentation/commands)
