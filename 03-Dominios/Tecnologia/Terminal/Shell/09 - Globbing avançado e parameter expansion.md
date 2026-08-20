---
title: "Globbing avançado e parameter expansion"
created: 2026-05-19
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - terminal
  - shell
  - zsh
  - magus
  - globbing
  - expansion
aliases:
  - Globbing
  - Parameter expansion
---

# Globbing avançado e parameter expansion

## TL;DR

Globbing avançado do Zsh substitui dezenas de `find -X` por one-liners. `EXTENDED_GLOB` liga negação (`^`), exclusão (`~`), `#`/`##` e alternation `(p1|p2)`. Glob qualifiers `(.)/(/)/(N)/(L+N)/(om[N])` funcionam sem `EXTENDED_GLOB` — são feature nativa do globbing. Parameter expansion vai além de `${var:-default}` com flags `(L)/(U)/(s:.:)/(@)` que evitam pipe pra `sed`/`awk`. Use diariamente.

---

## O que é / Como funciona

### Globbing essencial (compatível com Bash + sh)

Padrões de glob que funcionam em qualquer shell POSIX:

- `*` — zero ou mais chars (exceto `/`)
- `?` — exatamente 1 char
- `[abc]` — char em set
- `[a-z]` — char em range
- `[^abc]` — char NÃO em set
- `**/` — recursivo (subdirs); Zsh tem nativo, Bash precisa `shopt -s globstar`

### Extended glob (Zsh)

Requer `setopt EXTENDED_GLOB`. Não é ativado por default em Zsh vanilla (nem pelo OMZ).

- `^pattern` — negação: `*^.bak` = tudo que não termina em `.bak`
- `~pattern` — exclusão: `*.txt~README*` = arquivos `.txt` exceto os que começam com `README`
- `(p1|p2)` — alternation: `*.(txt|md)` = arquivos `.txt` ou `.md`
- `pattern#` — zero ou mais repetições do padrão
- `pattern##` — um ou mais repetições do padrão

### Glob qualifiers `(...)`

Pós-fixados ao padrão; filtram por atributo do arquivo. **Não** requerem `EXTENDED_GLOB` — são feature nativa do globbing do Zsh.

| Qualifier | Match |
|---|---|
| `(.)` | arquivos regulares |
| `(/)` | diretórios |
| `(@)` | symlinks |
| `(*)` | executáveis |
| `(N)` | null glob (sem match = vazio, não erro) |
| `(L+N)` | tamanho > N bytes (`Lk`/`Lm`/`Lg` pra kB/MB/GB) |
| `(L-N)` | tamanho < N bytes |
| `(mh-N)` | modificado nas últimas N horas |
| `(mm-N)` | modificado nos últimos N minutos |
| `(md-N)` | modificado nos últimos N dias |
| `(om)` | ordenar por mtime (mais recente primeiro) |
| `(Om)` | ordenar por mtime (mais antigo primeiro) |
| `(om[N,M])` | ordenar por mtime, pegar índices N a M |
| `(U)` | owned by you (effective UID) |
| `(G)` | owned by your group (effective GID) |
| `(F)` | diretórios não-vazios |

Qualifiers se combinam: `*(.NL+1k.om[1,5])` = arquivos regulares, sem erro se vazio, maiores que 1kB, 5 mais recentes.

### Parameter expansion essencial

**Defaults e checks** (compatíveis com Bash):

- `${var:-default}` — valor de `var` se setado e não-vazio, senão `default`
- `${var:+alt}` — `alt` se `var` setado e não-vazio, senão vazio
- `${var:=default}` — atribui `default` a `var` se não setado; expande pra `default`
- `${var:?error}` — exit + mensagem de erro se `var` não setado ou vazio

**Substring e length:**

- `${var:offset:length}` — slice Bash-compat (0-based)
- `${var[start,end]}` — slice Zsh: indexação 1-based, end inclusivo
- `${#var}` — comprimento da string ou número de elementos do array

**Match e replace:**

- `${var#prefix}` — remove prefix mais curto (greedy mínimo)
- `${var##prefix}` — remove prefix mais longo (greedy máximo)
- `${var%suffix}` — remove suffix mais curto
- `${var%%suffix}` — remove suffix mais longo
- `${var/pat/repl}` — substitui primeira ocorrência de `pat` por `repl`
- `${var//pat/repl}` — substitui todas as ocorrências
- `${var/#pat/repl}` — substitui só se `pat` casa no início
- `${var/%pat/repl}` — substitui só se `pat` casa no fim

### Flags Zsh `${(<flags>)var}`

Sintaxe `${(flags)var}` aplica transformações inline — sem pipes externos.

- `(L)` — lowercase: `${(L)var}`
- `(U)` — uppercase: `${(U)var}`
- `(C)` — capitalize (primeira letra de cada palavra)
- `(s:sep:)` — split por separador; resultado é array
- `(j:sep:)` — join array com separador; resultado é string
- `(@)` — preservar elementos como array (evita join automático quando entre aspas duplas)
- `(P)` — indireção: `${(P)name}` = valor da variável cujo NOME está em `$name`
- `(k)` — keys de hash associativo
- `(v)` — values de hash associativo

Flags se combinam: `${(j:,:)array}` junta array com vírgula; `${(s:.:)hostname}` split por ponto.

---

## Na prática

### Globbing — one-liners reais

```zsh
# Os 5 logs mais recentes (om = ordem desc por mtime; [1,5] = primeiros 5)
print -l **/*.log(.om[1,5])

# Arquivos .ts não-vazios (tamanho > 1 byte)
print -l **/*.ts(.L+1)

# Diretórios modificados nas últimas 24h
print -l **/*(/mh-24)

# Arquivos maiores que 10MB
print -l **/*(.Lm+10)

# Tudo em ~/Downloads exceto arquivos .iso
ls ~/Downloads/*~*.iso

# Sem erro se não houver match (útil em scripts)
print -l **/*.tmp(N)

# Arquivos executáveis no diretório atual
print -l *(*)

# Os 3 arquivos mais antigos em src/
print -l src/*(.Om[1,3])
```

### Parameter expansion — one-liners reais

```zsh
# Extension de um arquivo (remove prefix mais longo até o último ponto)
file="report.tar.gz"
echo ${file##*.}            # gz

# Basename sem a última extension
echo ${file%.*}             # report.tar

# Replace separador de path
path="a/b/c/d"
echo ${path//\//-}          # a-b-c-d

# Uppercase
name="ana"
echo ${(U)name}             # ANA

# Split hostname em array (cada parte numa linha)
print -l ${(s:.:)HOST}

# Default com env var
echo ${EDITOR:-vim}         # vim se EDITOR não setado

# Indireção — dispatch dinâmico
greeting="Hello"
varname="greeting"
echo ${(P)varname}          # Hello

# Join array com vírgula
items=(alpha beta gamma)
echo ${(j:,:)items}         # alpha,beta,gamma
```

---

## Armadilhas

### 1. `EXTENDED_GLOB` esquecido

**Causa:** `EXTENDED_GLOB` não é ativado por default em Zsh vanilla. OMZ não o liga automaticamente. Qualquer padrão com `^`, `~`, `#`, `##` ou alternation `(p1|p2)` requer a opção ativa. Glob qualifiers `(...)` NÃO precisam — funcionam vanilla.

**Sintoma:** `zsh: bad pattern: ^*.bak` ou erro similar ao tentar usar negação ou qualifiers.

**Como detectar:** `setopt | grep -i extended` — se não aparecer `extendedglob`, a opção está desligada. Tentar `echo ^foo` também confirma: sem EXTENDED_GLOB, `^` é literal.

**Solução:** Adicionar `setopt EXTENDED_GLOB` no `~/.zshrc` (acima do `source "$ZSH/oh-my-zsh.sh"` se usar OMZ).

---

### 2. `(N)` faltando em script — padrão sem match aborta

**Causa:** O default do Zsh é `NOMATCH` — quando um glob não encontra nenhum arquivo, o shell dispara erro em vez de retornar vazio. Em scripts não-interativos isso aborta a execução.

**Sintoma:** Script para com `zsh: no matches found: **/*.tmp` mesmo quando a ausência de arquivos é um caso válido.

**Como detectar:** Rodar o padrão num diretório vazio: `cd /tmp/vazio; print **/*.tmp`. Se sair com erro (exit code ≠ 0), confirma o comportamento.

**Solução:** Usar o qualifier `(N)` no padrão (`**/*.tmp(N)`) pra silenciar o erro e retornar lista vazia. Alternativa global: `setopt NULL_GLOB` no script (ou `unsetopt NOMATCH`).

---

### 3. `om` é ordem descendente — confunde quem espera ordem alfabética

**Causa:** `(om)` ordena por mtime com **mais recente primeiro** — é ordem descendente por design do Zsh. Quem espera "primeiros 5 por ordem de criação/nome" recebe os 5 mais novos.

**Sintoma:** `**/*.log(.om[1,5])` retorna os logs mais recentes, não os mais antigos. Quem queria "os mais velhos" recebe exatamente o oposto.

**Como detectar:** Comparar `**/*.log(.om[1])` e `**/*.log(.om[-1])` com `stat -c %y` — o índice 1 é o mais recente, o último índice é o mais antigo.

**Solução:** Usar `(Om)` (maiúscula O) para ordem crescente (mais antigo primeiro). Para inverter a janela: `(Om[1,5])` = 5 mais antigos.

---

### 4. Parameter expansion sem aspas duplas — word splitting quebra resultado

**Causa:** O shell realiza field splitting em expansões não protegidas por aspas. Um valor com espaços vira múltiplos argumentos separados, quebrando loops e chamadas de função.

**Sintoma:** `var="hello world"; for x in ${var}; do echo "[$x]"; done` imprime `[hello]` e `[world]` em linhas separadas — em vez de `[hello world]` numa só iteração.

**Como detectar:** Usar `set -x` ou `echo "[$var]"` para ver a expansão real. Qualquer espaço no valor e ausência de aspas confirma o risco.

**Solução:** Usar aspas duplas sempre em expansões: `"${(L)var}"`, `"${var:-default}"`. Em Zsh, arrays com `"${(@)arr}"` preservam elementos individualmente sem split indesejado.

---

### 5. `(s:.:)` em string vazia retorna array vazio silenciosamente

**Causa:** Split de string vazia com `(s:sep:)` produz array com zero elementos. Código que assume "sempre há pelo menos um elemento" após o split quebra sem aviso.

**Sintoma:** `HOST=""` faz `${(s:.:)HOST}[1]` ser vazio; lógica que usa o primeiro componente do hostname produz resultado vazio ou erro silencioso downstream.

**Como detectar:** `var=""; arr=(${(s:.:)var}); echo ${#arr}` — imprime `0`, confirmando o array vazio.

**Solução:** Verificar `[[ -n $var ]]` antes de fazer o split, ou garantir default não-vazio: `${var:-localhost}`. Em scripts críticos, adicionar `(( ${#arr} > 0 )) || return 1` após o split.

---

## Em inglês

- **glob / globbing** — *glob / globbing*. "Shell globbing expands patterns like `*` into matching filenames."
- **expansão** — *expansion*. "Parameter expansion transforms variable values inline without external tools."
- **substituição** — *substitution*. "The `${var/pat/repl}` syntax performs pattern substitution."
- **case-insensitive** — *case-insensitive*. "Glob matching in Zsh can be made case-insensitive with `(i)` qualifier."
- **valor default** — *default value*. "Use `${var:-default}` to supply a default value when the variable is unset."
- **separador** — *separator*. "The `(s:sep:)` flag splits a string on the given separator."
- **split** — *split*. "Split a dotted hostname into an array with `${(s:.:)HOST}`."
- **join** — *join*. "Join array elements into a string with `${(j:,:)arr}`."
- **indireção** — *indirection*. "The `(P)` flag enables indirection: expand the variable whose name is stored in another variable."
- **recursivo** — *recursive*. "The `**/` glob pattern matches files recursively through subdirectories."

---

## Veja também

- [[02 - Zsh essencial]] — `setopt EXTENDED_GLOB` pré-requisito
- [[10 - Plugins, themes e custom no OMZ]] — globbing em scripts de plugin
- [[03-Dominios/Tecnologia/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Globbing|globbing]], [[Dicionário do Terminal#Extended glob|extended glob]], [[Dicionário do Terminal#Glob qualifier|glob qualifier]], [[Dicionário do Terminal#Parameter expansion|parameter expansion]]

---

## Referências

- Zsh manual — Filename Generation: https://zsh.sourceforge.io/Doc/Release/Expansion.html#Filename-Generation
- Zsh manual — Parameter Expansion: https://zsh.sourceforge.io/Doc/Release/Expansion.html#Parameter-Expansion
