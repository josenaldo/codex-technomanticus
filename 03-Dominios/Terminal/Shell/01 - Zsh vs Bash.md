---
title: "Zsh vs Bash"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - bash
aliases:
  - Zsh vs Bash
  - Por que Zsh
---

# Zsh vs Bash

> [!abstract] TL;DR
> Zsh é um shell interativo da família Bourne, parente próximo de Bash mas com escolhas diferentes — não é superset. Pra dev individual, o ganho está em completion programável superior, prompt rico, globbing avançado e extensibilidade via OMZ. Scripts Bash continuam rodando se você usar shebang `#!/usr/bin/env bash`.

## O que é / Como funciona

### O que é um shell

Um shell é um interpretador de comandos de um sistema Unix-like. Recebe comandos do usuário (ou de um script), expande variáveis, gerencia redirecionamento de I/O, executa processos externos e builtins, e devolve resultados.

Há dois modos de operação fundamentais:

- **Interativo**: o shell lê de um TTY, exibe prompt, carrega `~/.zshrc` (Zsh) ou `~/.bashrc` (Bash). É o que você usa no dia a dia.
- **Não-interativo**: o shell executa um script; `~/.zshrc` não é carregado. O shebang define qual shell roda o script.

Essa distinção é importante: configurações no `~/.zshrc` não se aplicam a scripts — o que funciona no terminal pode falhar silenciosamente num script se depender de opts ou funções definidas interativamente.

### Família Bourne: linha do tempo curta

```
sh (1979, Stephen Bourne, Bell Labs)
  └─ ksh (1983, David Korn, AT&T)
       ├─ bash (1989, Brian Fox, GNU Project)
       └─ zsh (1990, Paul Falstad, Princeton)
```

Zsh surgiu em 1990, criado por Paul Falstad como estudante em Princeton. A sintaxe base vem da família Bourne (sh/ksh), mas Zsh incorporou ideias de csh para arrays e globbing, e adicionou funcionalidades próprias — completion programável, prompt expansions, ZLE (Zsh Line Editor).

### POSIX como mínimo comum

POSIX (Portable Operating System Interface) é um padrão IEEE que define APIs e comportamento mínimos de shell. Um script escrito apenas com construções POSIX deve rodar em qualquer shell POSIX-compatível (sh, dash, ash, bash em modo strict).

- **Bash** é mais próximo do POSIX por default; muitas extensões Bash são ativadas explicitamente (`shopt -s extglob`).
- **Zsh** não garante POSIX compliance no modo default — e o faz de forma intencional. Mas oferece `emulate sh|bash|ksh` para ativar compat quando necessário.

### O mito "Zsh é superset de Bash"

A documentação oficial do Zsh e o seu FAQ são diretos: **bash e Zsh são linguagens de programação diferentes**. Um programa escrito pra uma não rodará, em geral, sem ajustes na outra.

O que alimenta o mito é que a maioria dos scripts simples (sequência de comandos, pipes, redirecionamentos básicos) funciona nos dois — por compartilharem a sintaxe Bourne de base. Mas basta usar arrays, parameter expansion avançada ou word splitting que as diferenças aparecem.

---

## Na prática

### Identificar o shell em uso

```zsh
# Shell de login configurado no sistema
echo $SHELL

# Shell efetivamente rodando agora (process name)
ps -p $$

# Versão do Zsh
echo $ZSH_VERSION
```

`$SHELL` mostra o shell de login registrado no `/etc/passwd` — não o que está rodando agora. Se você abriu um subshell bash dentro do Zsh, `$SHELL` ainda mostrará `/usr/bin/zsh`.

### Trocar o shell default

```zsh
# Trocar para Zsh (requer re-login)
chsh -s $(which zsh)

# Confirmar após re-login
echo $SHELL   # deve mostrar /usr/bin/zsh ou /bin/zsh
```

Sem o re-login (ou abertura de nova sessão), o shell de login não muda na sessão atual.

### Rodar script Bash em ambiente Zsh

```bash
#!/usr/bin/env bash
# Com este shebang, o script roda sempre em bash,
# independente do shell interativo do usuário.

arr=(zero um dois)
echo "${arr[0]}"   # imprime "zero" — indexação Bash 0-based
```

Sem shebang, o sistema pode usar `sh` (dash no Ubuntu) ou o shell configurado — comportamento indefinido. Shebang explícito é o único jeito confiável.

A alternativa em Zsh puro: `emulate bash` no topo do script ativa um modo de compatibilidade que ajusta as opts mais comuns, mas não é 100% equivalente a bash — use para scripts simples.

### Diferenças sintáticas que mais aparecem

#### 1. Indexação de arrays

```zsh
# Zsh — 1-indexed (padrão csh)
arr=(um dois tres)
echo $arr[1]    # "um"
echo $arr[0]    # "" (vazio — não existe índice 0 por default)

# Bash — 0-indexed
arr=(um dois tres)
echo ${arr[0]}  # "um"
echo ${arr[1]}  # "dois"
```

Um script Bash que usa `${arr[0]}` retorna **vazio** em Zsh (com a mensagem ignorada). A opção `KSH_ARRAYS` faz Zsh usar 0-indexed, mas ativa outras mudanças também.

#### 2. Ativar opções de shell

```zsh
# Zsh — setopt
setopt EXTENDED_GLOB
setopt NULL_GLOB

# Bash — shopt
shopt -s extglob
shopt -s nullglob
```

Os nomes das opções também diferem; não é apenas a sintaxe.

#### 3. Conversão de case em variáveis

```zsh
# Zsh — parameter flags com ${(flag)var}
nome="Codex Technomanticus"
echo ${(L)nome}   # "codex technomanticus"
echo ${(U)nome}   # "CODEX TECHNOMANTICUS"

# Bash — operadores de expansão
nome="Codex Technomanticus"
echo ${nome,,}    # "codex technomanticus"
echo ${nome^^}    # "CODEX TECHNOMANTICUS"
```

Um alias ou função que usa `${var,,}` copiado do Bash produz `bad substitution` em Zsh. Reescreva com `${(L)var}` ou use `emulate bash -c '...'`.

#### 4. Globbing recursivo

```zsh
# Zsh — globbing recursivo nativo (EXTENDED_GLOB ou ** nativo)
ls **/*.ts         # todos os .ts em subdiretórios, sem opt adicional

# Bash — requer shopt
shopt -s globstar
ls **/*.ts
```

No Zsh, `**` é tratado como glob recursivo por default em versões modernas. No Bash pré-4.0, `**` não existe; em Bash 4.0+, precisa de `shopt -s globstar`.

#### 5. Word splitting: a diferença mais silenciosa

```zsh
# Zsh — NÃO faz word splitting em $var por default
lista="arquivo1.txt arquivo2.txt"
for f in $lista; do
    echo $f
done
# Imprime: "arquivo1.txt arquivo2.txt" (1 iteração, 1 item)

# Bash — faz word splitting por default
lista="arquivo1.txt arquivo2.txt"
for f in $lista; do
    echo $f
done
# Imprime:
# arquivo1.txt
# arquivo2.txt
```

No Zsh, `$lista` não é dividido em palavras por espaço por default. O loop itera **uma vez** com a string inteira. Para obter o comportamento Bash, ative `setopt SH_WORD_SPLIT` ou use `${=lista}` para expansão explícita com splitting.

---

## Armadilhas

### (1) Script Bash que depende de word splitting quebra silenciosamente em Zsh

**Causa:** Bash faz word splitting em `$var` não-quoted; Zsh não faz por default.

```bash
# Bash: funciona como esperado
arquivos="foo.sh bar.sh baz.sh"
for f in $arquivos; do chmod +x $f; done  # itera 3 vezes
```

```zsh
# Zsh: quebra silenciosamente
arquivos="foo.sh bar.sh baz.sh"
for f in $arquivos; do chmod +x $f; done  # itera 1 vez, tenta chmod em "foo.sh bar.sh baz.sh"
```

**Sintoma:** loop executa apenas uma iteração; `chmod` falha com "no such file" (ou aparentemente não faz nada se o arquivo por acaso se chama assim).

**Como detectar:** `set -x` antes do loop mostra as expansões. Ou use `print -l $arquivos` (Zsh) para inspecionar a lista linha a linha antes do loop.

**Solução em Zsh:** use um array real:
```zsh
arquivos=(foo.sh bar.sh baz.sh)
for f in $arquivos; do chmod +x $f; done  # correto em Zsh
```

---

### (2) Alias ou função com `${var,,}` falha com `bad substitution`

**Causa:** a sintaxe de case conversion `${var,,}` / `${var^^}` é exclusiva do Bash 4+. Zsh não a reconhece.

**Sintoma:** ao definir ou executar a função em Zsh, o erro `bad substitution` aparece na linha da expansão. O alias que funcionava no `.bashrc` falha imediatamente ao ser carregado no `.zshrc`.

**Como detectar:** `zsh -n ~/.zshrc` faz syntax check sem executar — reporta o problema na linha correta.

**Solução:** reescrever usando parameter flags do Zsh:
```zsh
# Em vez de ${var,,}
echo ${(L)variavel}

# Em vez de ${var^^}
echo ${(U)variavel}
```

Ou, pra um bloco de compat pontual: `emulate bash -c 'echo ${variavel,,}'`.

---

### (3) Indexação 0 vs 1 retorna vazio sem erro

**Causa:** Zsh é 1-indexed; `arr[0]` retorna string vazia sem mensagem de erro.

**Sintoma:** código que funciona em Bash silenciosamente retorna string vazia em Zsh. Um `if [[ -n "${arr[0]}" ]]` sempre entra no ramo `else` — bug difícil de rastrear porque não há output de erro.

**Como detectar:**
```zsh
arr=(alfa beta gama)
echo "índice 0: '$arr[0]'"   # '' (vazio)
echo "índice 1: '$arr[1]'"   # 'alfa'
echo "tamanho:  $#arr"        # 3
```

**Solução:** ao portar scripts Bash, buscar todos os `[0]` e incrementar para `[1]`, ou ativar `KSH_ARRAYS` no topo do script se a semântica Bash for necessária.

---

## Em inglês

- **shell** — *shell*. "The shell is a command interpreter that acts as an interface between the user and the operating system kernel."
- **shell interativo** — *interactive shell*. "An interactive shell reads commands from user input and displays results; it loads startup files like `.zshrc`."
- **shell de login** — *login shell*. "A login shell is the first shell spawned when a user authenticates; it sources `.zprofile` (Zsh) or `.bash_profile` (Bash)."
- **script** — *script*. "A shell script is a non-interactive shell session that executes a sequence of commands from a file."
- **builtin** — *builtin*. "A builtin is a command implemented directly by the shell, not as an external binary in `$PATH`, so it runs without forking a new process."
- **conformidade POSIX** — *POSIX compliance*. "Bash maintains closer POSIX compliance by default; Zsh offers `emulate sh` for compatibility when needed."
- **indexação** — *indexing*. "Array indexing starts at 1 in Zsh and at 0 in Bash — a frequent source of off-by-one bugs when porting scripts."
- **expansão de parâmetro** — *parameter expansion*. "Parameter expansion like `${(L)var}` in Zsh and `${var,,}` in Bash both lower-case a string, but are not interchangeable syntax."
- **divisão de palavras** — *word splitting*. "Word splitting on unquoted variables is enabled by default in Bash but disabled in Zsh, making `for f in $list` behave differently."
- **emular** — *emulate*. "Running `emulate bash` at the top of a Zsh script activates a compatibility mode that adjusts options to approximate Bash behavior."

---

## Veja também

- [[02 - Zsh essencial]]
- [[03 - History do Zsh]]
- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]]
- [[03-Dominios/Terminal/Shell/index|MOC do galho]]
- [[Dicionário do Terminal#Shell|shell]], [[Dicionário do Terminal#POSIX|POSIX]], [[Dicionário do Terminal#Builtin|builtin]]

## Referências

- Zsh Introduction — <https://zsh.sourceforge.io/Doc/Release/Introduction.html>
- Zsh FAQ — Differences from Other Shells — <https://zsh.sourceforge.io/FAQ/zshfaq02.html>
- A User's Guide to the Z-Shell — <https://zsh.sourceforge.io/Guide/zshguide.html>
