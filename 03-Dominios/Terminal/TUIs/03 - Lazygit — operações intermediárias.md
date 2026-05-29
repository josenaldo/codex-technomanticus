---
title: "Lazygit — operações intermediárias"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - tuis
  - lazygit
  - adepto
  - git
aliases:
  - Lazygit rebase
  - Lazygit cherry-pick
---

# Lazygit — operações intermediárias

> [!abstract] TL;DR
> Lazygit transforma operações git delicadas em fluxos visuais: rebase interativo (painel Commits, `i` para todos os commits da branch ou `e` a partir de commit específico), cherry-pick (`C` copy uppercase na branch origem + `V` paste uppercase na branch destino), staging por hunks (`enter` em arquivo no painel Files → `space` em hunk; `a` alterna modo hunk ↔ linha; `tab` troca staged/unstaged), reflog acessível pela aba Reflog no painel Branches (`]`/`[`), merge conflicts detectados automaticamente com `enter` no arquivo `UU` abrindo conflict view. Keybindings verificados contra `Keybindings_en.md` oficial (Lazygit main branch, 2026-05).

## O que é / Como funciona

### Rebase interativo

O rebase interativo permite reorganizar, editar, combinar ou remover commits antes de um push ou PR.

Dois pontos de entrada no painel Commits:

- **`i`** — "Start interactive rebase": inicia rebase pra todos os commits da branch a partir do primeiro merge commit ou commit de branch principal. Mostra lista editável.
- **`e`** — "Edit (start interactive rebase)": inicia a partir do commit selecionado. Se já estiver em rebase, marca o commit para edição (rebase pausa nesse commit).

Durante o rebase, cada commit recebe ações aplicadas pelas teclas abaixo (painel Commits):

| Tecla | Ação | Detalhe |
|---|---|---|
| `s` | Squash | Combina com o commit abaixo; mensagem do commit atual é anexada |
| `f` | Fixup | Combina com o commit abaixo; mensagem do commit atual é descartada |
| `d` | Drop | Remove o commit |
| `r` | Reword | Edita apenas a mensagem do commit |
| `e` | Edit | Pausa o rebase nesse commit pra permitir alterações manuais |
| `p` | Pick | Mantém o commit como está (usado pra desfazer squash/drop mid-rebase) |
| `<c-k>` | Mover commit acima | Reordena o commit uma posição para cima |
| `<c-j>` | Mover commit abaixo | Reordena o commit uma posição para baixo |

Após marcar as ações:

- **`m`** (global) — "View merge/rebase options" → Continue pra aplicar o rebase
- **`<esc>`** — Abort (cancela e reverte)

> Obs: `<c-k>` e `<c-j>` usam Ctrl — confira no `?` contextual caso seu terminal intercepte Ctrl+J/K.

### Cherry-pick cross-branch

Cherry-pick copia 1 ou mais commits de uma branch pra outra sem fazer merge completo.

Fluxo no Lazygit:

1. Painel Branches → checkout da branch **origem** (`space`)
2. Painel Commits → `C` (uppercase) no commit desejado → commit marcado como "copied" (cor diferente)
3. Repetir `C` em outros commits se necessário (seleção acumulativa)
4. Painel Branches → checkout da branch **destino** (`space`)
5. Painel Commits → `V` (uppercase) — "Paste (cherry-pick)" — aplica os commits copiados

Para cancelar a seleção de cherry-pick antes de colar: `<c-r>` no painel Commits.

Se houver conflito após o paste, o fluxo é o mesmo de merge conflict (ver seção abaixo).

### Staging por hunks

Permite commitar apenas parte das mudanças de um arquivo — útil para commits atômicos.

1. Painel Files → `enter` em arquivo modificado → entra na **staging view** (main panel)
2. `<left>`/`<right>` navega entre hunks
3. `space` — stage/unstage o hunk ou linha selecionada
4. `a` — alterna modo: **hunk** (bloco inteiro) ↔ **linha** (granularidade individual)
5. `v` — "Toggle range select": seleciona intervalo de linhas pra stage em lote
6. `tab` — alterna entre lado unstaged e staged
7. `<esc>` — retorna ao painel Files

O arquivo no painel Files pode aparecer como parcialmente staged (split entre staged e unstaged).

### Discard

- `d` no painel Files → menu com opções de discard (arquivo selecionado ou tudo)
- Confirma antes de executar, mas **mudanças uncommitted não aparecem no reflog** — se descartadas, não há recuperação fácil via git
- Hábito recomendado: `s` (stash) antes de discardar, pra ter ponto de retorno

### Reflog

O reflog registra todos os movimentos de HEAD: commits, checkouts, resets, rebases, merges.

Acesso no Lazygit:

- Painel Branches (`3`) → aba **Reflog** via `]` (próxima aba) até chegar; ou `[` (anterior)
- O painel Branches tem abas: Local → Remotes → Tags → **Reflog**

Dentro da aba Reflog:

- `j`/`k` navega entre entradas
- `space` — checkout da entrada como detached HEAD
- `g` — "Reset" — reset do HEAD atual pra essa entrada (soft/mixed/hard)
- `n` — cria branch a partir da entrada
- `C` — cherry-pick de entrada do reflog

Útil pra:
- Recuperar branch deletada (encontrar o SHA antes da deleção, criar branch a partir dele)
- Desfazer reset acidental (`g` → hard reset de volta)
- Ver exatamente o que mudou no HEAD ao longo do tempo

> Limitação: reflog cobre apenas movimentos de HEAD. Changes uncommitted (working tree não commitada) não aparecem.

### Merge conflicts

Após `git merge`, `git rebase` ou cherry-pick com conflito, Lazygit detecta automaticamente.

1. Painel Files mostra arquivos com status `UU` (both modified, unresolved)
2. `enter` em arquivo `UU` → **conflict view** no main panel
3. Navegar conflitos: `<left>`/`<right>` (conflito anterior/próximo), `<up>`/`<down>` (hunk anterior/próximo)
4. `space` — "Pick hunk": escolhe o hunk atual (ours ou theirs)
5. `b` — "Pick all hunks": aceita todos de uma vez
6. `z` — "Undo": desfaz última resolução de conflito
7. Após resolver todos, arquivo sai de `UU`
8. Stagear e continuar com `m` → Continue

---

## Na prática

### Workflow "limpar history antes de PR"

Objetivo: transformar vários commits de rascunho em commits limpos e atômicos.

```text
1. Painel Commits → `i` (start interactive rebase pra todos os commits da branch)
2. Commits de rascunho/wip: pressionar `f` (fixup) — sem mensagem — ou `s` (squash) — combina mensagem
3. Reordenar com <c-k>/<c-j> se necessário
4. Commits pra remover totalmente: `d` (drop)
5. `m` → Continue → Lazygit aplica o rebase
6. Push com force-with-lease (via custom command ou git CLI: git push --force-with-lease)
```

> Push com `P` pode falhar após rebase — os SHAs mudaram; remoto rejeita. Ver Armadilha 1.

### Workflow "trazer hotfix de main pra feature"

Objetivo: aplicar um fix já commitado em main na branch de feature, sem rebase completo.

```text
1. Painel Branches → checkout main (ou a branch que tem o fix)
2. Painel Commits → localizar o commit do hotfix
3. `C` (uppercase) no commit → marcado como "copied"
4. Painel Branches → checkout feature
5. Painel Commits → `V` (uppercase) → cola o commit
6. Conflito? Painel Files → `enter` em arquivo UU → resolver hunks com `space` → `m` → Continue
```

### Workflow "stage parcial pra commit atômico"

Objetivo: arquivo tem 2 mudanças não-relacionadas; commitar em commits separados.

```text
1. Painel Files → `enter` no arquivo → staging view
2. Hunk 1 (mudança A): `space` → staged
3. Hunk 2 (mudança B): não pressionar `space` → permanece unstaged
4. `<esc>` → volta ao painel Files
5. `c` → escreve mensagem do commit A → confirma
6. Painel Files ainda mostra arquivo com mudança B unstaged
7. `enter` → staging view → `space` em hunk 2 → `c` → commit B
```

Pra granularidade de linha (mudanças no mesmo hunk):

```text
1. `enter` no arquivo → staging view
2. `a` → alterna pra modo linha (line-by-line)
3. `j`/`k` navega linhas; `space` stage linha individual
4. `<esc>` → commit parcial
```

---

## Armadilhas

**1. Rebase com commit já pushado vira force-push**

- **Causa:** rebase interativo altera SHA de todos os commits rebaseados; remoto já tem os SHAs antigos.
- **Sintoma:** `P` (push) falha com "non-fast-forward" ou "rejected — remote contains work you don't have".
- **Como detectar:** após rebase, tentar push normal; falha indica divergência de SHAs.
- **Solução:** usar `--force-with-lease` (preferível a `--force`) via custom command (nota 06) ou git CLI. Confirmar antes que a branch não é shared com outros devs ou é branch pessoal de feature.

**2. Discard apaga changes uncommitted sem recuperação via reflog**

- **Causa:** `d` no painel Files com changes uncommitted; working tree não tem reflog no git.
- **Sintoma:** mudanças desaparecem; `git reflog` não mostra nada; `git stash list` vazio.
- **Como detectar:** git só rastreia objetos commitados; changes nunca commitadas não têm SHA.
- **Solução:** hábito de usar `s` (stash) ou `F` (create fixup commit) antes de qualquer operação destrutiva. `git fsck --lost-found` pode recuperar blobs dangling em edge cases, mas não é garantia.

**3. Cherry-pick com conflito deixa operação pendente**

- **Causa:** `V` paste em branch destino com conflito; Lazygit entra em estado "cherry-pick in progress".
- **Sintoma:** painel Files mostra `UU`; painel superior indica operação em andamento.
- **Como detectar:** painel de status no topo do Lazygit exibe a operação ativa; `git status` mostra "You are currently cherry-picking".
- **Solução:** resolver conflitos normalmente (seção Merge conflicts acima) e `m` → Continue; ou `m` → Abort pra cancelar o cherry-pick inteiro.

**4. Reflog não cobre changes uncommitted**

- **Causa:** reflog rastreia movimentos de HEAD (commits, checkouts, resets) — não o working tree.
- **Sintoma:** discardou mudanças uncommitted; reflog não tem entrada; perdido.
- **Como detectar:** `git reflog` não mostra; `git stash list` não tem entrada.
- **Solução:** se a mudança foi commitada ao menos uma vez (mesmo como WIP), está no reflog. Se nunca commitada, `git fsck --lost-found` pode achar objetos dangling. Prevenção: stash antes de operações destrutivas.

**5. Staging por hunks stage mais que o esperado em modo hunk**

- **Causa:** `space` em modo hunk (padrão) stage o bloco contíguo inteiro, não só a linha sob o cursor.
- **Sintoma:** painel Files mostra mais linhas staged que o esperado; `tab` para lado staged confirma.
- **Como detectar:** `tab` alterna pra visão staged e mostra o que vai no próximo commit.
- **Solução:** `a` na staging view alterna para modo linha (line-by-line); `space` passa a agir por linha individual. `a` de novo volta pro modo hunk.

**6. `<c-j>`/`<c-k>` interceptados pelo terminal**

- **Causa:** alguns emuladores (kitty, etc.) ou multiplexers (Zellij, tmux) capturam Ctrl+J/K antes de chegar ao Lazygit.
- **Sintoma:** reordenação de commits não funciona; nada acontece ou ação errada.
- **Como detectar:** `?` no painel Commits mostra os keybindings ativos no contexto; se não aparecer, há conflito.
- **Solução:** configurar o emulador/multiplexer pra não interceptar essas sequências, ou configurar `customKeybindings` no `~/.config/lazygit/config.yml` (nota 04) pra remapear reorder.

---

## Em inglês

- **rebase interativo** — *interactive rebase*. "reescrever histórico de commits: squash, drop, reorder, sem mover pra outro branch."
- **cherry-pick** — *cherry-pick*. "copiar commit(s) específicos de uma branch pra outra sem merge completo."
- **hunk** — *hunk*. "bloco contíguo de linhas alteradas num diff; unidade de staging parcial no Lazygit."
- **stage** — *stage / index*. "marcar mudança pra incluir no próximo commit; staging view permite fazer isso por hunk ou por linha."
- **discard** — *discard*. "descartar mudança uncommitted do working tree; irreversível se não houver stash ou commit prévio."
- **reflog** — *reflog (reference log)*. "registro de todos os movimentos de HEAD; útil pra recuperar branch deletada ou desfazer reset acidental."
- **conflito** — *merge conflict*. "duas branches modificaram o mesmo trecho de código de formas incompatíveis; git não consegue resolver sozinho."
- **squash** — *squash*. "combinar commit com o commit abaixo, unindo as mudanças e as mensagens."
- **fixup** — *fixup*. "variante do squash onde a mensagem do commit corrente é descartada; útil pra WIP commits."
- **force-push** — *force-push*. "push que sobrescreve o histórico remoto; necessário após rebase de commits já publicados; prefira `--force-with-lease`."

---

## Veja também

- [[01 - Lazygit — overview e operações essenciais]] — pré-req: painéis, layout, operações básicas
- [[04 - Lazygit — config e customização]] — `editPreset` pra conflict resolution externa, custom keybindings
- [[06 - Lazygit — operações avançadas]] — bisect, customCommands, worktrees
- [[03-Dominios/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Cherry-pick|cherry-pick]], [[Dicionário do Terminal#Hunk|hunk]], [[Dicionário do Terminal#Interactive rebase|interactive rebase]], [[Dicionário do Terminal#Reflog|reflog]]

---

## Referências

- Lazygit Keybindings (oficial): https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md
- Lazygit Rebasing: https://github.com/jesseduffield/lazygit/blob/master/docs/Rebasing.md
