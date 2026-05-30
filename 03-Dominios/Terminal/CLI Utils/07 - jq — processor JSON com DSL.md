---
title: "jq — processor JSON com DSL"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - jq
  - json
aliases:
  - jq
---

# jq — processor JSON com DSL

> [!abstract] TL;DR
> jq é processor JSON com DSL própria — pipeline de filtros (`|`), seleção (`select`), transformação (`map`), agregação (`reduce`). Lê JSON do stdin, escreve JSON do stdout. Flag `-r` emite strings sem aspas (essencial pra pipar pra `cd`/`ssh`); `-s` agrupa inputs num array; `-e` retorna exit não-zero quando filtro vazio. Essencial pra qualquer fluxo com API REST ou kubectl.

## O que é / Como funciona

### Filosofia: filtros componíveis em pipeline

jq modela processamento JSON como um pipeline de filtros. Cada filtro recebe um valor e emite 0, 1 ou N valores. O operador `|` encadeia filtros da esquerda pra direita — output de um vira input do próximo. Processamento é streaming: jq processa input-por-input sem carregar tudo na memória (exceto com `-s`).

### Filtros essenciais

| Filtro | Descrição |
|--------|-----------|
| `.` | Identity — repassa input sem modificar |
| `.foo` | Acessa campo `foo` do objeto; retorna `null` se ausente |
| `.foo.bar` | Acesso encadeado; ERROR se `.foo` for null |
| `.[0]` | Primeiro elemento do array; `.[-1]` último |
| `.[]` | Itera todos elementos do array ou valores do objeto |
| `.foo?` | Como `.foo`, mas suprime erro em tipo errado |
| `.[]?` | Como `.[]`, mas suprime erros |
| `.[2:4]` | Slice — subarray/substring (início inclusivo, fim exclusivo) |

### Operadores

| Operador | Descrição |
|----------|-----------|
| `\|` | Pipe — encadeia filtros |
| `,` | Combina outputs — emite resultado de A *e* de B pra mesmo input |
| `+` | Soma, concatenação de strings/arrays/objetos |
| `-` | Subtração; remove elementos de array |
| `*` | Multiplicação; merge recursivo de objetos |
| `/` | Divisão; split de string |
| `//` | Alternativa — retorna esquerda a menos que seja `false`/`null` |

### Funções built-in importantes

| Função | Descrição |
|--------|-----------|
| `select(cond)` | Passa o valor adiante se `cond` for true; descarta se false |
| `map(f)` | Aplica filtro `f` a cada elemento do array; retorna array |
| `reduce STREAM as $v (INIT; UPDATE)` | Fold — acumula valores num único resultado |
| `keys` | Array de chaves do objeto (sorted) ou índices do array |
| `values` | Array de valores do objeto |
| `length` | Tamanho de string, array, objeto, ou `0` pra null |
| `type` | Tipo do valor como string (`"object"`, `"array"`, `"string"`, `"number"`, `"boolean"`, `"null"`) |
| `to_entries` | Converte objeto em array de `{key, value}` |
| `from_entries` | Inverso de `to_entries` |
| `add` | Soma/concatena todos elementos do array |
| `sort_by(f)` | Ordena array por expressão |
| `group_by(f)` | Agrupa por expressão; retorna array de arrays |
| `unique` | Remove duplicatas (requer array sorted) |
| `flatten` | Achata arrays aninhados |

### Flags principais

| Flag | Descrição |
|------|-----------|
| `-r`, `--raw-output` | Strings sem aspas externas — essencial pra pipar pra cd/ssh/xargs |
| `-c`, `--compact-output` | Uma linha por valor (sem pretty-print) |
| `-s`, `--slurp` | Agrupa todos inputs num único array antes de processar |
| `-e`, `--exit-status` | Exit 0 se output ≠ false/null; exit 1 se false/null; exit 4 se vazio |
| `-n`, `--null-input` | Usa `null` como input (útil com `--arg`/`--argjson`) |
| `--arg name value` | Define variável `$name` como string |
| `--argjson name json` | Define variável `$name` como valor JSON |
| `-f file` | Lê programa do arquivo |

### Exit code semantics

Por padrão, jq sai com código 0 sempre que parse é OK — independente do output. Com `-e`, a semântica muda: exit 0 se o último output foi algo que não `false` nem `null`; exit 1 se foi `false`/`null`; exit 4 se não houve output algum. Útil em scripts pra usar jq como asserção em condicionais.

## Na prática

### Receitas básicas

```bash
# Pretty-print qualquer JSON
curl -s https://api.github.com/users/jqlang | jq .

# Acessar campo
echo '{"name":"alice","age":30}' | jq '.name'
# → "alice"  (com aspas — JSON)

# Acessar campo como string pura (sem aspas)
echo '{"name":"alice"}' | jq -r '.name'
# → alice  (sem aspas — texto)

# Iterar array
echo '[1,2,3]' | jq '.[]'
# → 1
# → 2
# → 3

# Filtrar com select
echo '{"users":[{"name":"alice","active":true},{"name":"bob","active":false}]}' \
  | jq '.users[] | select(.active)'
# → {"name":"alice","active":true}

# Projetar campos
echo '{"users":[{"id":1,"name":"alice","email":"a@x.com"},{"id":2,"name":"bob","email":"b@x.com"}]}' \
  | jq '.users | map({id, name})'
# → [{"id":1,"name":"alice"},{"id":2,"name":"bob"}]

# Extrair emails como texto puro
curl -s https://api.example.com/users | jq -r '.users[].email'
```

### Receitas avançadas

```bash
# Variável string com --arg
jq --arg user alice '.users[] | select(.name == $user)' users.json

# Variável JSON com --argjson
jq --argjson minAge 18 '.users[] | select(.age >= $minAge)' users.json

# Slurp — agregar múltiplos arquivos JSON
jq -s 'add' file1.json file2.json
# Junta dois arrays JSON em um

# -e como asserção em script
if curl -s https://api/health | jq -e '.ok == true' > /dev/null; then
  echo "API saudável"
else
  echo "API com problema"
fi

# CSV de campos selecionados
jq -r '.users[] | [.name, .email, .age | tostring] | @csv' users.json

# reduce — somar preços
echo '{"items":[{"price":10},{"price":25},{"price":5}]}' \
  | jq '[.items[].price] | reduce .[] as $p (0; . + $p)'
# → 40

# to_entries pra renomear chaves
echo '{"oldKey":"value"}' \
  | jq '.to_entries | map(.key = "newKey") | from_entries'

# Interpolação de string
echo '{"name":"alice","age":30}' \
  | jq -r '"Usuário: \(.name), idade: \(.age)"'
# → Usuário: alice, idade: 30

# rg --json | jq pra análise estruturada
rg --json 'TODO' | jq 'select(.type=="match") | .data.path.text' | sort -u
```

> [!note] Versão
> Exemplos testados com jq 1.7+; verifique `jq --version` localmente. A flag `-e` retorna exit 4 pra output vazio a partir da 1.6.

## Armadilhas

### (1) `-r` faltando — strings com aspas quebram pipe

**Causa:** sem `-r`, jq emite strings JSON com aspas (`"alice"` em vez de `alice`).

**Sintoma:** `cd "$(jq '.path' file)"` recebe `"/home/alice"` com aspas literais e falha com "No such file".

**Como detectar:** output visível tem aspas ao redor do valor.

**Solução:** quando consumer é texto (`cd`, `ssh`, `xargs`, variável shell), SEMPRE use `-r`. Omita `-r` apenas quando o consumer espera JSON válido (outro jq, yq, parser).

### (2) `select` vs `map` confundidos

**Causa:** `select(cond)` filtra — mantém o item se `cond` for true, descarta se false. `map(f)` transforma — aplica `f` a cada item e retorna array do mesmo tamanho.

**Sintoma:** "queria filtrar mas transformou" ou vice-versa.

**Como detectar:** `select` retorna o item original ou nada; `map` retorna SEMPRE array com resultado de `f`.

**Solução:** mnemonic — `select` = `WHERE`; `map` = `SELECT` (SQL). Combinado: `.users | map(select(.active))` — filter dentro de transform.

### (3) `null` em chave faltante vs erro

**Causa:** `.foo` em objeto sem a chave `foo` retorna `null` silenciosamente. `.foo.bar` quando `.foo` é `null` retorna ERROR: `Cannot index null with string "bar"`.

**Sintoma:** stack trace no meio de um pipeline.

**Como detectar:** checar se objeto pode não ter a chave em questão.

**Solução:** operador opcional `?` — `.foo?.bar?` retorna `null` em vez de errar. Alternativa: `if .foo then .foo.bar else null end`. Ou `select(.foo) | .foo.bar` filtra antes de acessar.

### (4) Números float vs int — perda de precisão

**Causa:** jq trata todos números como float64 (IEEE 754). Inteiros grandes (Twitter/X IDs, timestamps em nanosegundos) perdem precisão.

**Sintoma:** ID `123456789012345678` vira `123456789012345700` no output.

**Como detectar:** comparar byte-a-byte o input vs output de `.`.

**Solução:** preservar IDs grandes como string no JSON original; ou usar `gojq` (implementação Go) que suporta bigint nativo.

### (5) UTF-8 BOM no input quebra parser

**Causa:** alguns Windows tools (PowerShell Export-Csv, Excel) prefixam BOM (`EF BB BF`) em JSON. jq não tolera BOM — falha imediatamente.

**Sintoma:** `parse error (Invalid numeric literal at EOF at line 1, column 4)` mesmo com JSON válido.

**Como detectar:** `xxd file.json | head -1` mostra `efbb bf7b` no início.

**Solução:** strip BOM antes de pipar — `sed '1s/^\xef\xbb\xbf//' file.json | jq ...` ou `iconv -f UTF-8-BOM -t UTF-8 file.json | jq ...`.

### (6) `-s` slurp em stream gigante engole memória

**Causa:** `-s` agrupa TODO o input num único array antes de iniciar o processamento — em streams de log ou arquivos gigantes, tenta carregar tudo na RAM.

**Sintoma:** OOM killer mata jq, ou processo trava com memória subindo monotonicamente.

**Como detectar:** `ps aux | grep jq` mostra %MEM crescendo.

**Solução:** processar sem `-s` — pipas filtros linha a linha. Quando precisa de agregação sobre stream, use `reduce` que é incremental: `jq -n 'reduce inputs as $x (0; . + $x.value)' big.ndjson`.

## Em inglês

- **pipeline de filtros** — *filter pipeline*. "jq modela processamento JSON como um filter pipeline onde output de um filtro vira input do próximo via `|`."
- **identidade** — *identity*. "O filtro identity (`.`) repassa o input sem modificar — útil para pretty-print."
- **saída bruta** — *raw output*. "raw output (`-r`) emite strings sem aspas JSON externas, essencial para pipar para `cd` ou `ssh`."
- **slurp** — *slurp*. "O modo slurp (`-s`) lê todos os inputs e agrupa num array único antes de processar."
- **select** — *select*. "A função select mantém ou descarta valores baseada em condição booleana."
- **map** — *map*. "A função map transforma cada elemento do array aplicando um filtro e retorna array do mesmo tamanho."
- **reduce** — *reduce*. "reduce é o fold que acumula N valores em 1 resultado via função incremental."
- **código de saída** — *exit code*. "exit code é o status retornado ao shell; com `-e`, jq torna o exit code semanticamente significativo."
- **projeção** — *projection*. "projection constrói objeto com subconjunto de campos, como em `map({id, name})`."
- **interpolação** — *interpolation*. "string interpolation embute expressões dentro de strings via `\"\\(.expr)\"`."

## Veja também

- [[08 - yq — processor YAML e as duas implementações]] — par natural pra YAML
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — composição capstone
- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — `rg --json | jq` pra análise estruturada
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#jq|jq]]
- [[Dicionário do Terminal#raw output (jq -r)|raw output (jq -r)]]
- [[Dicionário do Terminal#slurp (jq -s)|slurp (jq -s)]]

## Referências

- jq manual: https://jqlang.github.io/jq/manual/
- jq tutorial: https://jqlang.github.io/jq/tutorial/
