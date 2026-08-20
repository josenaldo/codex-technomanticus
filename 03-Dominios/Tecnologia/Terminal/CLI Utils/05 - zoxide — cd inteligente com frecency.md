---
title: "zoxide — cd inteligente com frecency"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - zoxide
  - frecency
aliases:
  - zoxide
  - z (zoxide)
---

> [!abstract] TL;DR
> zoxide é cd inteligente baseado em **frecency** (frequency + recency). Mantém DB local de pastas visitadas; `z foo` pula direto pra match com maior pontuação; `zi foo` abre fzf interativo. Init script no shell (substitui ou suplementa `cd`). Sucessor de `autojump` e `z.sh` — mais rápido (Rust), DB mais robusta (sqlite-like).

## O que é / Como funciona

### Filosofia: aprender com seu uso

Pastas visitadas com frequência e visitadas recentemente sobem no ranking; substring matching com pontuação; `z proj` pula pra pasta mais "frecente" cujo path contém `proj`. Basta digitar um pedaço do nome — zoxide resolve o caminho completo com base no histórico real de navegação.

DB local em `~/.local/share/zoxide/db.zo` (padrão XDG). Não é um alias de `cd` por padrão — é um comando separado `z`, mais fzf interativo `zi`.

### Algoritmo frecency

Cada acesso a uma pasta incrementa o contador de visitas e atualiza o timestamp. A pontuação é calculada combinando visitas acumuladas com um multiplicador de recência:

| Última visita        | Multiplicador |
|----------------------|---------------|
| Menos de 1 hora      | score × 4     |
| Menos de 1 dia       | score × 2     |
| Menos de 1 semana    | score / 2     |
| Mais de 1 semana     | score / 4     |

Pastas antigas e pouco visitadas decaem e são removidas quando o total de scores ultrapassa `_ZO_MAXAGE` (padrão: 10 000). Query curta basta pra navegar bem — o algoritmo privilegia o que você usa de verdade.

### Comandos

| Comando                        | O que faz                                              |
|--------------------------------|--------------------------------------------------------|
| `z <substring>`                | Pula pra pasta com maior score contendo a substring    |
| `z <a> <b>`                    | E lógico — path deve conter ambas as substrings        |
| `zi <substring>`               | Interativo com fzf — escolhe entre candidatos rankeados|
| `z -`                          | Volta pra pasta anterior (como `cd -`)                 |
| `zoxide query --list`          | Lista todo o banco com pontuações (debug/limpeza)      |
| `zoxide query --list --score`  | Lista com score numérico visível                       |
| `zoxide add <path>`            | Adiciona path manualmente ao banco                     |
| `zoxide remove <path>`         | Remove path do banco                                   |
| `zoxide import --from <fmt> <file>` | Importa banco de autojump, z.sh ou fasd          |

### Init script no shell

`zoxide init <shell>` produz o script que define as funções `z`, `zi` e os hooks de navegação. Adicionar ao arquivo de config do shell:

```bash
# Zsh — em ~/.zshrc (DEPOIS do plugin manager)
eval "$(zoxide init zsh)"

# Bash — em ~/.bashrc
eval "$(zoxide init bash)"

# Fish — em ~/.config/fish/config.fish
zoxide init fish | source
```

Por padrão define `z` e `zi`. Para sobrescrever `cd` completamente:

```bash
eval "$(zoxide init zsh --cmd cd)"
```

Com `--cmd cd`, `cd /path/absoluto` continua funcionando normalmente — o wrapper é transparente pra paths absolutos e relativos válidos; só aplica lógica frecency quando o argumento não resolve diretamente.

### DB location e portabilidade

| Variável         | Default                        | Efeito                             |
|------------------|--------------------------------|------------------------------------|
| `_ZO_DATA_DIR`   | `~/.local/share/zoxide/`       | Diretório do arquivo `db.zo`       |
| `_ZO_MAXAGE`     | `10000`                        | Limite total de scores antes do GC |
| `_ZO_FZF_OPTS`   | (vazio)                        | Flags extras passadas ao fzf em zi |
| `_ZO_ECHO`       | `0`                            | `1` imprime path antes de cd       |

O DB **não sincroniza** entre máquinas automaticamente — cada máquina aprende com seus próprios padrões de uso.

## Na prática

### Setup

Instalar via package manager e adicionar o init script ao final do `.zshrc`, **depois** do plugin manager:

```bash
# Ubuntu/Debian
sudo apt install zoxide

# Arch
sudo pacman -S zoxide

# macOS
brew install zoxide

# Cargo (última versão)
cargo install zoxide --locked
```

Confirmar versão:

```bash
zoxide --version
```

Adicionar ao `.zshrc` (no **fim**, depois de oh-my-zsh/zinit/prezto):

```bash
eval "$(zoxide init zsh)"
```

Opcional — substituir `cd`:

```bash
eval "$(zoxide init zsh --cmd cd)"
```

> [!tip] Versão hedged
> Exemplos testados com zoxide 0.9+. Verifique `zoxide --version` localmente — flags e defaults podem variar em versões mais antigas.

### Receitas

```bash
# Navegar pra pasta de um projeto (path contém "myproj")
z myproj

# Match duplo — path contém "src" E "cli"
z src cli

# Interativo — lista candidatos rankeados via fzf
zi myproj

# Ver o banco inteiro (debug / limpar entradas velhas)
zoxide query --list --score

# Remover entrada errada do banco
zoxide remove /caminho/que/não/uso/mais
```

### Migração de autojump/z.sh

```bash
# De autojump
zoxide import --from autojump ~/.local/share/autojump/autojump.txt

# De z.sh
zoxide import --from z ~/.z

# De fasd
zoxide import --from fasd ~/.fasd
```

Após importar, confirmar com `zoxide query --list` que os paths chegaram.

## Armadilhas

### (1) Init script ordering errado quebra `z`

**Causa:** `eval "$(zoxide init zsh)"` colocado ANTES do plugin manager (oh-my-zsh, zinit, prezto) causa problema: o plugin manager pode sobrescrever o widget ou função definida pelo zoxide.

**Sintoma:** `z` não funciona, conflita com outro alias, ou gera "command not found".

**Como detectar:** `which z` mostra função de outro plugin ou builtin.

**Solução:** colocar o `eval` no **fim** do `.zshrc`, depois de tudo que mexe em widgets, aliases e funções.

### (2) `zi` sem fzf instalado falha silenciosamente

**Causa:** `zi` depende de fzf no PATH; sem ele, o comportamento varia entre versões (erro obscuro ou saída vazia).

**Sintoma:** `zi` não abre o menu interativo.

**Como detectar:** `command -v fzf` retorna vazio.

**Solução:** instalar fzf antes de usar `zi` (dependência soft — `z` puro funciona sem fzf).

### (3) Match surpresa em substring curta

**Causa:** `z d` casa qualquer pasta cujo path contém `d`, podendo incluir centenas de resultados num monorepo.

**Sintoma:** pula pra pasta inesperada.

**Como detectar:** `zoxide query d --list` mostra os candidatos rankeados.

**Solução:** usar substring mais específica (`z docs` em vez de `z d`), ou compor (`z docs api`).

### (4) DB não migra entre máquinas

**Causa:** `~/.local/share/zoxide/db.zo` é local; ao trocar de máquina ou configurar nova, começa do zero.

**Sintoma:** `z` precisa "aprender de novo" e falha em pastas não visitadas.

**Como detectar:** `zoxide query --list` vazio em máquina recém-configurada.

**Solução:** sincronizar `db.zo` via Syncthing/Resilio entre máquinas com estrutura de pastas similar; ou aceitar cold start (uma semana de uso normal reconstrói o útil).

### (5) Conflito com aliases `cd` em containers e CI

**Causa:** em ambientes minimalistas sem zoxide, scripts que invocam `cd foo` diretamente falham se o alias `cd` → zoxide não existe.

**Sintoma:** script funciona local, quebra em CI/container limpo.

**Como detectar:** rodar o script em container sem zoxide instalado.

**Solução:** scripts portáveis devem usar paths absolutos ou checar `command -v zoxide` antes de assumir `z`/`cd` com zoxide.

### (6) `_ZO_DATA_DIR` customizado quebrando portabilidade do init

**Causa:** mudar `_ZO_DATA_DIR` sem garantir que todas as máquinas exportam a mesma variável faz o zoxide procurar o DB no lugar errado.

**Sintoma:** `zoxide query --list` vazio mesmo após uso intenso, ou banco "duplicado" em dois lugares.

**Como detectar:** `echo $_ZO_DATA_DIR` em cada máquina — divergência = problema.

**Solução:** se customizar, exportar `_ZO_DATA_DIR` **antes** do `eval "$(zoxide init ...)"` no `.zshrc`, e documentar no repo de dotfiles.

## Em inglês

- **frecência** — *frecency*. "frecency é métrica híbrida de frequency + recency; base do algoritmo de ranking do zoxide."
- **frequência** — *frequency*. "frequency mede quantas vezes uma pasta foi visitada; um dos dois fatores do frecency."
- **recência** — *recency*. "recency mede quão recente foi o último acesso à pasta; o outro fator do frecency."
- **script de inicialização** — *init script*. "O init script é injetado pelo `eval \"$(zoxide init <shell>)\"` e define `z`, `zi` e os hooks de navegação."
- **correspondência por substring** — *substring match*. "substring match significa que `z foo` casa qualquer path que contenha \"foo\"."
- **banco de dados (DB)** — *database*. "O database `db.zo` é onde zoxide persiste pastas visitadas e seus scores de frecency."
- **classificação** — *ranking*. "O ranking ordena candidatos por score frecency; maior score = posição mais alta no resultado."
- **widget** — *widget*. "Um widget é uma função registrada no ZLE; init scripts de zoxide/fzf/atuin registram widgets e os bindkeiam."
- **função shell** — *shell function*. "z` e `zi` são definidos como shell functions (não binários) pelo init script do zoxide."
- **fuzzy** — *fuzzy*. "Modo fuzzy de matching aproximado; `zi` usa fzf com fuzzy matching sobre os candidatos do banco."

## Veja também

- [[01 - fzf — fuzzy finder universal]] — `zi` usa fzf
- [[06 - atuin — history shell com SQLite e sync]] — também usa frecency em outra dimensão
- [[12 - Stack interativo — fzf zoxide atuin]] — composição capstone
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#zoxide|zoxide]]
- [[Dicionário do Terminal#frecency|frecency]]
- [[Dicionário do Terminal#init script (shell)|init script (shell)]]

## Referências

- zoxide repo: https://github.com/ajeetdsouza/zoxide
- zoxide wiki: https://github.com/ajeetdsouza/zoxide/wiki
