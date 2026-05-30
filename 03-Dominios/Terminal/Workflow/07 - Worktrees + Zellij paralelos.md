---
title: "Worktrees + Zellij paralelos"
created: 2026-05-24
updated: 2026-05-24
type: concept
progress: backlog
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

# Worktrees + Zellij paralelos

> [!abstract] TL;DR
> Playbook: `git worktree add` + sessão Zellij por worktree = multi-task sem stash. Vale pra: review de PR enquanto trabalha em feature; bug fix urgente sem perder estado; testar branch alheia. NÃO vale: `node_modules` compartilhado (cada worktree precisa o seu), lock-files divergem, DB local compartilhada gera conflito. Convenção: `~/repos/<projeto>-<feature>/`.

---

## O que é / Como funciona

### O que é git worktree

Funcionalidade nativa do git desde a versão 2.5 (2015). Permite múltiplos working trees do **mesmo** repositório, cada um em uma pasta separada com branch e estado independentes. O diretório `.git/` é **compartilhado** entre todos os worktrees — commits e refs são visíveis em qualquer um deles. Nenhum dado duplicado, nenhum clone extra.

### Quando vale

- Bug urgente em `main` enquanto desenvolve feature em outro worktree — sem stash, sem interrupção
- Code review de PR: `gh pr checkout` em worktree dedicado, branch de feature intacta
- Comparação A/B de duas abordagens rodando em paralelo
- Long-running build/test em paralelo com edição ativa em outra pasta

### Quando NÃO vale

- Projetos com `node_modules`/`target`/`.venv` pesados: cada worktree exige instalação própria (espaço em disco + tempo)
- Lock-files divergem entre worktrees: o merge depois é dor desnecessária
- DB local compartilhada (ex.: Postgres em `localhost:5432`): dois worktrees rodando migrations diferentes corrompem o schema
- Containers Docker com bind mounts em paths absolutos: conflito de paths em worktrees diferentes

### Modelo mental

Worktree = mini-clone sem custo de `.git/`. Mas há custo real: re-instalar deps e reconfigurar DB por worktree. O trade-off é "alocar/desalocar worktree" versus "stash/pop". Para trabalho de horas ou dias em paralelo, worktree vence. Para mudança rápida de contexto (minutos), stash ainda é mais prático.

---

## Na prática

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

A função abaixo cria o worktree e abre uma sessão Zellij com nome correspondente. Adicionar ao `~/.zshrc`:

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

Para limpar ao fim do trabalho: fechar a sessão Zellij com `zellij k myproj-feature-login`, depois remover o worktree com `git worktree remove ~/repos/myproj-feature-login`.

### Limpeza weekly

Script para identificar worktrees antigas pelo último acesso:

```bash
# Listar worktrees + último access
git worktree list --porcelain | grep "^worktree" | while read -r line; do
    p=$(echo "$line" | cut -d' ' -f2)
    date=$(stat -c %y "$p" 2>/dev/null | cut -d' ' -f1)
    echo "$date $p"
done | sort
```

Worktrees com data antiga e sem sessão Zellij ativa são candidatas a remoção.

---

## Armadilhas

1. **`git worktree remove` sem checar trabalho não-comitado**
   - **Causa:** hábito de "limpar" sem verificar.
   - **Sintoma:** mudanças não-comitadas e não-stashed desaparecem sem aviso.
   - **Como detectar:** `git -C <path> status` antes do remove.
   - **Solução:** o git por padrão recusa `remove` em working tree dirty — isso é proteção nativa. Usar `--force` SÓ após verificação manual explícita.

2. **`node_modules` duplicado em N worktrees**
   - **Causa:** cada worktree precisa de `npm install` próprio.
   - **Sintoma:** disco enche rapidamente; instalações lentas a cada novo worktree.
   - **Como detectar:** `du -sh ~/repos/myproj-*/node_modules`.
   - **Solução:** monorepos com pnpm ou Yarn workspaces + content-addressable store compartilham dependências. Caso contrário, aceite o custo ou prefira stash.

3. **DB local compartilhada gera conflito de estado**
   - **Causa:** Postgres em `localhost:5432` único; worktree A roda migration X, worktree B roda migration Y.
   - **Sintoma:** schema inconsistente, bugs "aleatórios" difíceis de reproduzir.
   - **Como detectar:** mismatch entre schema esperado pela app e schema real.
   - **Solução:** Docker Compose com portas diferentes por worktree, ou disciplina de uma worktree por vez interagindo com a DB local.

4. **Branch checked out em dois worktrees ao mesmo tempo**
   - **Causa:** git proíbe ter a mesma branch em dois worktrees simultâneos.
   - **Sintoma:** `git worktree add` falha com "branch X is already checked out at...".
   - **Como detectar:** mensagem de erro explícita.
   - **Solução:** cada worktree recebe sua própria branch. Para acesso read-only a uma branch em outro worktree, use detached HEAD: `git worktree add -d ~/repos/myproj-readonly main`.

5. **Esquecer `prune` após deletar pasta manualmente**
   - **Causa:** apagou a pasta do worktree diretamente com `rm -rf` em vez de usar o comando git.
   - **Sintoma:** `git worktree list` mostra entradas "prunable" ou exibe warnings em operações git.
   - **Como detectar:** `git worktree list` — entradas com caminho inexistente aparecem com aviso.
   - **Solução:** preferir sempre `git worktree remove <path>`. Se já apagou manualmente: `git worktree prune` limpa as referências órfãs.

---

## Em inglês

- **worktree** — *worktree*. "Cada worktree tem sua própria branch e estado de trabalho."
- **branch** — *branch*. "Crie uma branch nova pra cada contexto de trabalho paralelo."
- **checkout** — *checkout*. "Fazer checkout de uma branch já em uso em outro worktree gera erro."
- **stash** — *stash*. "Para contextos de minutos, stash ainda é mais rápido que criar um worktree."
- **lock file** — *lock file*. "Lock files divergindo entre worktrees tornam o merge trabalhoso."
- **dependencies** — *dependencies*. "Cada worktree precisa instalar suas próprias dependências."
- **dirty working tree** — *dirty working tree*. "Git recusa remover um worktree com dirty working tree por padrão."
- **prune** — *prune*. "Rode git worktree prune depois de apagar pastas de worktree manualmente."
- **parallel** — *parallel*. "O objetivo do combo worktree + Zellij é habilitar trabalho parallel sem perda de contexto."
- **multi-task** — *multi-task*. "Git worktrees transformam um repositório único em plataforma de multi-task."

---

## Veja também

- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[08 - Refactoring multi-arquivo]]
- [[03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes — detach, attach, gerenciamento|Sessões persistentes (galho 3)]]
- [[03-Dominios/Terminal/TUIs/01 - Lazygit — overview e operações essenciais|Lazygit overview (galho 4)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#worktree|worktree]]
- [[Dicionário do Terminal#named session|named session]]

---

## Referências

- [git-worktree — documentação oficial](https://git-scm.com/docs/git-worktree)
