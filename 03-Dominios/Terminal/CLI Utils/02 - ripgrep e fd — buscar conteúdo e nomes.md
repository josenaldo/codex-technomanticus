---
title: "ripgrep e fd — buscar conteúdo e nomes"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - ripgrep
  - fd
  - rust
aliases:
  - ripgrep
  - rg
  - fd
---

# ripgrep e fd — buscar conteúdo e nomes

> [!abstract] TL;DR
> ripgrep (`rg`) e fd são ferramentas irmãs em Rust (filosofia burntsushi-style): rg busca **conteúdo** recursivamente; fd busca **nomes de arquivo**. Ambas respeitam `.gitignore` por padrão, usam regex Rust (não PCRE), suportam smart-case e são massivamente paralelas. Substituem `grep -r` e `find` em fluxos modernos. Em Debian/Ubuntu o binário do fd se chama `fdfind` (colisão com daemon antigo).

## O que é / Como funciona

### Filosofia compartilhada

rg e fd compartilham a mesma escola de design: defaults pragmáticos pensados pra dev, não pra sysadmin genérico.

- **Respeita `.gitignore` por padrão** — pula `node_modules/`, `vendor/`, `dist/`, `.git/` e qualquer pasta listada no gitignore. Output focado em código relevante, sem ruído.
- **Ignora hidden por padrão** — arquivos e pastas com `.` no início ficam fora, a menos que solicitados.
- **Output colorido e human-readable** — tipos de arquivo, nomes de arquivo, números de linha, matches destacados. rg oferece também `--json` pra integração com pipelines estruturados.
- **Paralelismo nativo** — ambas usam iteradores paralelos de diretório; fd é ~23× mais rápido que `find -iregex` em benchmarks típicos.
- **Regex Rust por padrão** — engine baseada em autômatos finitos e otimizações SIMD, sem look-around. Não é PCRE; sintaxe difere de `grep -P`.
- **Substituições diretas** — `rg padrão` substitui `grep -r padrão .`; `fd nome` substitui `find . -name '*nome*'`.

### ripgrep (rg) — buscar conteúdo

rg é uma ferramenta de busca de conteúdo em arquivos. O argumento principal é um padrão regex (ou literal com `-F`).

- **`-t <tipo>`** — filtra por tipo de arquivo. `rg -t py` busca só em `.py`; `rg -t md` em `.md`. Ver tipos disponíveis com `rg --type-list`.
- **`-F`** — desativa regex e trata o padrão como string literal. Útil quando o padrão contém `(`, `)`, `[`, `.` e outros metacaracteres.
- **`-P`** — ativa engine PCRE2, que suporta look-ahead e look-behind. Requer que rg tenha sido compilado com suporte a PCRE2; verificar com `rg --version` (mostra `+pcre2`).
- **`-A N`** / **`-B N`** / **`-C N`** — exibe N linhas de contexto após, antes, ou ao redor de cada match (after/before/context).
- **`--json`** — saída estruturada em JSON por linha (JSON Lines). Cada evento (begin, match, end, summary) é um objeto separado. Integra com `jq`.
- **`-l` / `--files-with-matches`** — lista apenas os nomes dos arquivos que contêm matches; não exibe as linhas.
- **`--no-ignore`** — desabilita todo o processamento de `.gitignore`. Útil pra buscar em `node_modules/`, `vendor/`, `build/`.
- **Smart-case** — padrão todo-lowercase = busca case-insensitive; qualquer letra maiúscula = case-sensitive. Override: `-i` (force insensitive), `-s` (force sensitive).

### fd — buscar nomes de arquivo

fd busca arquivos e diretórios pelo **nome**. O argumento principal é uma substring ou regex aplicada ao nome do arquivo (não ao conteúdo).

- **`-t f|d|l`** — filtra por tipo: `f` (file), `d` (directory), `l` (symlink). Também `x` (executable), `e` (empty).
- **`-e <ext>`** — filtra pela extensão. `fd -e ts` encontra todos os `.ts`; pode combinar com `-t f`.
- **`-H` / `--hidden`** — inclui arquivos e pastas ocultos (`.env`, `.git/`, `.config/`). Por padrão, fd ignora tudo que começa com `.`.
- **`-I`** — ignora `.gitignore`. Por padrão, fd respeita gitignore e pula pastas ignoradas.
- **`-x <cmd>`** — executa `<cmd>` para cada resultado individualmente (paralelo). Placeholder `{}` é substituído pelo path.
- **`-X <cmd>`** — executa `<cmd>` uma vez passando todos os resultados como argumentos (batch). Mais eficiente que `-x` quando o comando aceita múltiplos inputs.
- **Smart-case** — mesma regra do rg: query lowercase = case-insensitive; maiúscula = case-sensitive.

### Sinergia rg + fd

fd seleciona quais arquivos abrir; rg busca conteúdo dentro. O pipeline é natural:

- fd filtra por tipo/extensão/nome e rg recebe apenas os arquivos relevantes.
- Via `xargs`: `fd -t f -e py | xargs rg 'def test_'`
- Via flag `-x` do fd: `fd -t f -e py -x rg 'def test_'` (rg é chamado por arquivo)
- Para batch: `fd -t f -e py -X rg 'def test_'` (rg recebe todos de uma vez — mais eficiente)

## Na prática

### Receitas ripgrep

```bash
# Buscar "TODO" em todos os arquivos do projeto
rg "TODO"

# Buscar "import requests" apenas em arquivos Python
rg -t py "import requests"

# Busca literal — desativa regex (útil com parênteses, pontos, etc.)
rg -F "function(x, y)"

# Mostrar 3 linhas de contexto ao redor de cada match
rg -A 3 -B 3 "panic!"

# Saída JSON filtrada com jq (só linhas de match)
rg --json "error" | jq -c 'select(.type == "match")'

# Buscar incluindo node_modules e vendor (ignora o .gitignore)
rg --no-ignore "TODO"

# Listar apenas os nomes dos arquivos que têm FIXME
rg -l "FIXME"
```

Versões hedged: ripgrep 14+ (verificar com `rg --version`); ripgrep 15.1 era o latest em mai/2026.

### Receitas fd

```bash
# Buscar arquivos cujo nome contém "config"
fd config

# Buscar só arquivos TypeScript
fd -e ts -t f

# Buscar .env (hidden — requer -H)
fd -H '.env'

# Rodar black em todos os arquivos Python do projeto
fd -t f -e py -x black

# Contar linhas de todos os Python em batch (mais eficiente)
fd -t f -e py -X wc -l

# Encontrar diretórios chamados "tests"
fd -t d 'tests'
```

Versões hedged: fd 9+ (verificar com `fd --version` ou `fdfind --version`); fd 10.4.2 era o latest em mai/2026.

### Composição rg + fd

```bash
# Encontrar arquivos Python que têm pdb.set_trace (debugger esquecido)
fd -t f -e py -x rg 'pdb.set_trace'

# Renomear .jpeg → .jpg em batch (fd encontra, sh renomeia)
fd -e jpeg -x sh -c 'mv "$1" "${1%.jpeg}.jpg"' _ {}

# Listar arquivos com TODO e cruzar com fd pra confirmar extensão
rg --files-with-matches 'TODO' | fd -e py
```

## Armadilhas

### (1) .gitignore comendo arquivos esperados

**Causa:** rg e fd respeitam `.gitignore` por padrão — qualquer pasta ou arquivo listado ali fica invisível: `node_modules/`, `vendor/`, `dist/`, `build/`, arquivos gerados.

**Sintoma:** "Sei que esse arquivo existe mas rg/fd não acha."

**Como detectar:** `ls node_modules/` mostra a pasta; `rg "lodash" node_modules/` não retorna nada.

**Solução:** `--no-ignore` em rg; `-I` em fd. Se a pasta também for hidden (começa com `.`), combinar com `-H`. Exemplo: `rg --no-ignore --hidden "TODO"`.

### (2) Regex Rust ≠ PCRE (sem look-around por default)

**Causa:** A engine de regex do Rust usa autômatos finitos que garantem tempo linear — mas não suportam look-behind `(?<=...)` nem look-ahead complexo. É uma limitação por design, não bug.

**Sintoma:** Pattern que funciona em `grep -P` ou em Python/Perl falha em rg com mensagem: `"look-around, including look-ahead and look-behind, is not supported"`.

**Como detectar:** Mensagem de erro explícita do rg.

**Solução:** Usar `-P` (PCRE2) — mas requer que rg tenha sido compilado com suporte. Verificar: `rg --version` deve mostrar `+pcre2` nos features. Se não mostrar, reformular o regex em sintaxe Rust (sem look-around) ou instalar versão com PCRE2.

### (3) Smart-case surpreendendo com maiúscula

**Causa:** qualquer letra maiúscula no padrão ativa mode case-sensitive automaticamente. `rg "TODO"` busca só "TODO"; `rg "todo"` casa "TODO", "Todo", "todo".

**Sintoma:** match conta diferente do esperado; `rg "TODO"` retorna menos resultados que `rg "todo"`.

**Como detectar:** testar com padrão em lowercase e comparar contagem de resultados.

**Solução:** forçar comportamento explícito com `-i` (sempre case-insensitive) ou `-s` (sempre case-sensitive). Ou criar alias `alias rg='rg --smart-case'` pra deixar smart-case sempre ligado explicitamente.

### (4) fd ignorando hidden por padrão

**Causa:** fd pula qualquer arquivo ou diretório cujo nome começa com `.` — sem aviso, sem mensagem de erro.

**Sintoma:** `fd '.env'` não retorna nada num projeto que definitivamente tem `.env`. `fd -e cfg` não encontra `~/.config/` entries.

**Como detectar:** `ls -la` mostra o arquivo; `fd '.env'` não retorna. Confirmar com `fd -H '.env'`.

**Solução:** sempre usar `-H` / `--hidden` quando o alvo pode ser arquivo oculto. Combinar com `-I` se a pasta também está no `.gitignore`.

### (5) fdfind vs fd em Debian/Ubuntu

**Causa:** o pacote `fd-find` no apt instala o binário como `fdfind` por colisão com o daemon `fd` do BIND (servidor DNS), que existia antes.

**Sintoma:** `fd config` → `zsh: command not found: fd`; mas `fdfind config` funciona normalmente.

**Como detectar:** `which fd` falha; `which fdfind` resolve o path correto.

**Solução:** criar alias no `.zshrc`: `alias fd=fdfind`; ou symlink: `ln -s $(which fdfind) ~/.local/bin/fd` (garantir que `~/.local/bin` esteja no `$PATH`). Em scripts portáveis, detectar ambos: `command -v fd || command -v fdfind`.

### (6) rg -F esquecido em string com metacaracteres regex

**Causa:** `rg "function(x, y)"` interpreta `(` como início de grupo de captura e `,` e `)` como parte da regex — pode gerar erro de parsing ou match inesperado.

**Sintoma:** `rg "function(x, y)"` retorna erro de regex ou zero matches quando o texto literal existe no arquivo.

**Como detectar:** `rg "function(x, y)"` falha ou não retorna; `rg -F "function(x, y)"` retorna corretamente.

**Solução:** usar `-F` / `--fixed-strings` sempre que o padrão contiver metacaracteres literais: `(`, `)`, `[`, `]`, `.`, `*`, `?`, `+`, `{`, `}`, `^`, `$`, `|`, `\`.

## Em inglês

- **buscar conteúdo** — *search content*. "rg searches file content recursively."
- **buscar por nome** — *search by filename*. "fd searches filenames, not file content."
- **recursivo** — *recursive*. "Both tools traverse directories recursively by default."
- **respeita gitignore** — *gitignore-aware*. "fd and rg are gitignore-aware out of the box."
- **smart-case** — *smart-case*. "Smart-case means lowercase queries are case-insensitive automatically."
- **paralelo** — *parallel*. "fd is parallel by default, using all CPU cores."
- **paralelismo** — *parallelism*. "Parallelism is what makes rg significantly faster than grep -r."
- **flavor de regex** — *regex flavor*. "rg uses the Rust regex flavor, not PCRE."
- **look-around** — *look-around*. "Look-around (look-ahead and look-behind) requires the -P flag in rg."
- **literal** — *literal string*. "Use -F to search for a literal string without regex interpretation."

## Veja também

- [[01 - fzf — fuzzy finder universal]] — fzf usa `rg --files` ou `fd` como source
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — `rg --json | jq` pra análise estruturada
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#ripgrep|ripgrep]]
- [[Dicionário do Terminal#fd|fd]]
- [[Dicionário do Terminal#fdfind|fdfind]]
- [[Dicionário do Terminal#smart-case|smart-case]]
- [[Dicionário do Terminal#gitignore-aware|gitignore-aware]]
- [[Dicionário do Terminal#Whitelist (.gitignore)|Whitelist (.gitignore)]] — conceito relacionado em dotfiles

## Referências

- ripgrep: https://github.com/BurntSushi/ripgrep
- ripgrep GUIDE: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md
- fd: https://github.com/sharkdp/fd
