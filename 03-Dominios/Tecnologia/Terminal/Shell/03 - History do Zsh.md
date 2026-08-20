---
title: "History do Zsh"
created: 2026-05-20
updated: 2026-05-20
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - history
aliases:
  - History do Zsh
  - History
---

# History do Zsh

> [!abstract] TL;DR
> Zsh registra cada comando em `HISTFILE` (default `~/.zsh_history`). Configure opts de history (`SHARE_HISTORY`, `EXTENDED_HISTORY`, `HIST_IGNORE_ALL_DUPS`, `HIST_VERIFY`) e ganhe `Ctrl-R` (search incremental) + history expansion (`!!`, `!$`) + `fc` (editar comando como texto). É a ferramenta mais subutilizada do shell.

## O que é / Como funciona

O history do Zsh é o registro persistente de todos os comandos digitados em sessões interativas. Cada entrada é gravada em um arquivo de texto (`HISTFILE`), com tamanho controlado por duas variáveis distintas, e o comportamento é configurado por um conjunto de opts via `setopt`.

### Variáveis de controle

| Variável | Papel | Valor recomendado |
|---|---|---|
| `HISTFILE` | Caminho do arquivo de history no disco | `~/.zsh_history` (default) |
| `HISTSIZE` | Máximo de entradas mantidas na memória da sessão | `50000` |
| `SAVEHIST` | Máximo de entradas gravadas no `HISTFILE` | `50000` |

Regra invariável: `HISTSIZE` deve ser maior ou igual a `SAVEHIST`. Se `HISTSIZE < SAVEHIST`, o shell trunca a memória antes de salvar e você perde entradas.

### Opts essenciais

Todas as opts abaixo são ativadas com `setopt` no `~/.zshrc`. Ver [[02 - Zsh essencial]] para a semântica de `setopt`.

#### `SHARE_HISTORY`
Importa os novos comandos do `HISTFILE` antes de cada pesquisa no line editor, e anexa cada novo comando imediatamente ao arquivo. O efeito prático: abrir uma nova aba do terminal já enxerga os comandos digitados em outras abas abertas simultaneamente. É a opt mais impactante do bloco.

> [!note]
> `SHARE_HISTORY` implica `INC_APPEND_HISTORY`. Não use os dois simultaneamente — `SHARE_HISTORY` é o superset.

#### `EXTENDED_HISTORY`
Salva, além do comando, o timestamp de início (epoch) e a duração em segundos. O formato no arquivo fica `: 1716220000:5;git push` (dois-pontos, epoch, dois-pontos, duração, ponto-e-vírgula, comando). Necessário para `history -i` mostrar timestamps.

#### `HIST_IGNORE_ALL_DUPS`
Quando um novo comando é idêntico a qualquer entrada já presente no history (não só a imediata anterior), remove a entrada mais antiga e insere o novo no topo. Mantém o history limpo sem sacrificar o mais recente. Compare com `HIST_IGNORE_DUPS` (só ignora duplicata imediata) — `ALL_DUPS` é mais agressivo e geralmente preferível.

#### `HIST_IGNORE_SPACE`
Remove do history qualquer linha cujo primeiro caractere seja um espaço. Permite executar comandos "privados" sem registrar: `<space>echo $MY_SECRET`. Requer disciplina de prefixar com espaço.

#### `HIST_REDUCE_BLANKS`
Normaliza espaços extras em cada linha antes de gravar: `git   commit  -m  "msg"` vira `git commit -m "msg"`. Evita duplicatas por whitespace acidental.

#### `HIST_VERIFY`
Expansões de history (`!!`, `!$`, `!git`) não executam direto; o Zsh carrega a linha expandida no prompt para revisão. Pressionar `Enter` uma segunda vez executa. Essencial para evitar acidentes com `sudo !!`.

#### `INC_APPEND_HISTORY`
Escreve cada comando no `HISTFILE` ao término da execução, sem esperar o shell fechar. Use quando não quiser `SHARE_HISTORY` (que é mais amplo) mas ainda quiser persistência imediata.

#### `INC_APPEND_HISTORY_TIME`
Variante de `INC_APPEND_HISTORY` que só escreve após o comando terminar, permitindo registrar a duração real no formato `EXTENDED_HISTORY`. Incompatível com `SHARE_HISTORY`.

### Comandos de history

**`history`** Lista os últimos comandos da sessão com número sequencial. Por default mostra os últimos 16 eventos (número varia por implementação).

```zsh
history          # últimos eventos
history 1        # desde o evento 1 (todo o history)
history -10      # últimos 10
history -i       # com timestamps (requer EXTENDED_HISTORY)
history -t '%F %T'  # timestamps em formato legível
```

**`fc -l`** `fc` (fix command) com flag `-l` lista entradas do history com intervalo configurável.

```zsh
fc -l            # últimos 16 eventos
fc -l 1          # desde o evento 1
fc -l 1 50       # eventos 1 a 50
fc -l -10 -1     # últimos 10 (índices negativos = contagem regressiva)
fc -l -t '%F %T' # com timestamps formatados
```

**`fc` sem flags (editar)** Abre o último comando no editor definido em `$EDITOR` (ou `$FCEDIT`, ou `vi` como fallback). Ao salvar e fechar o editor, o Zsh executa o conteúdo editado. Poderoso para re-executar comandos longos com ajustes.

```zsh
fc               # edita e executa o último comando
fc -e nvim       # força o editor (sobrepõe $EDITOR)
fc -e nvim 42    # edita o evento de número 42
```

**`fc <string>`** Re-executa o comando mais recente que **começa com** a string (sem abrir editor). Comportamento equivalente ao `!str` do history expansion — prefixo, não substring. Para busca por conteúdo (contém), use `!?str?`.

```zsh
fc git           # re-executa o último comando que começa com "git"
```

> [!note]
> `fc` sem argumento e `fc -e -` têm comportamentos diferentes. `fc` puro abre o editor. `fc -e -` re-executa o último sem editar (equivalente a `!!` sem history expansion).

### Search interativo

**`Ctrl-R`** — busca incremental backward: abre o search mode no ZLE, cada caractere digitado filtra o history em tempo real, `Ctrl-R` adicional cicla para o match anterior, `Enter` executa, `Esc` ou `Ctrl-G` cancela.

**`Ctrl-S`** — busca forward (do mais antigo para o mais recente). Em muitos terminais está bloqueado por controle de fluxo XON/XOFF. Para liberar:

```zsh
stty -ixon   # desativa XON/XOFF; colocar no .zshrc
```

### History expansion

History expansion permite reusar partes de comandos anteriores sem redigitá-los. É ativada pela opt `BANG_HIST` (ligada por default em shells interativos Zsh — modo `<Z>`).

#### Designadores de evento

| Sintaxe | O que referencia |
|---|---|
| `!!` | Comando anterior inteiro |
| `!n` | Evento de número `n` |
| `!-n` | Evento `n` posições atrás (ex: `!-2` = antepenúltimo) |
| `!str` | Evento mais recente que **começa** com `str` |
| `!?str?` | Evento mais recente que **contém** `str` |
| `!#` | Linha atual digitada até agora |

#### Designadores de palavra

Combinados com o evento usando `:` (ex: `!!:$`):

| Sintaxe | Palavra selecionada |
|---|---|
| `!!:0` | Primeiro token (o comando em si) |
| `!!:1` | Primeiro argumento |
| `!!:^` | Primeiro argumento (atalho para `:1`) |
| `!!:$` ou `!$` | Último argumento |
| `!!:*` ou `!*` | Todos os argumentos |
| `!!:N` | Argumento de posição `N` |
| `!!:x-y` | Argumentos de `x` a `y` |

#### Quick substitution

`^antigo^novo` — substitui a primeira ocorrência de `antigo` por `novo` no comando anterior e re-executa. Equivale a `!!:s^antigo^novo^`.

```zsh
git commit -m "fix ts bug"
^ts^js              # → git commit -m "fix js bug"
```

#### Exemplos práticos

```zsh
# Repetir com sudo
apt install curl
sudo !!             # → sudo apt install curl

# Reusar o último argumento
mkdir -p ~/projects/novo-projeto
cd !$               # → cd ~/projects/novo-projeto

# Reusar todos os argumentos
cp arquivo.txt destino/
ls -la !*           # → ls -la arquivo.txt destino/

# Re-executar último git
!git                # → último comando que começa com "git"

# Substituição rápida
make tset           # typo
^tset^test          # → make test
```

---

## Na prática

### Bloco recomendado para `~/.zshrc`

```zsh
HISTFILE=~/.zsh_history
HISTSIZE=50000
SAVEHIST=50000

setopt SHARE_HISTORY            # compartilha history entre sessões abertas
setopt EXTENDED_HISTORY         # salva timestamp + duração de cada comando
setopt HIST_IGNORE_ALL_DUPS     # remove entradas duplicadas mais antigas
setopt HIST_IGNORE_SPACE        # prefixar com espaço = comando privado
setopt HIST_REDUCE_BLANKS       # normaliza whitespace antes de salvar
setopt HIST_VERIFY              # !! carrega no prompt antes de executar
```

> [!note] Por que não `INC_APPEND_HISTORY` junto com `SHARE_HISTORY`?
> `SHARE_HISTORY` já implica escrita incremental. Usar `INC_APPEND_HISTORY` simultaneamente com `SHARE_HISTORY` é redundante e pode causar comportamento inesperado. Escolha um ou outro.

### Workflows do dia a dia

**Search com `Ctrl-R`**

1. Pressione `Ctrl-R`
2. Comece a digitar parte do comando (ex: `docker run`)
3. `Ctrl-R` adicional cicla para o match anterior no history
4. `Enter` executa o match atual
5. `Esc` ou `Ctrl-G` cancela e volta ao prompt limpo

**Editar um comando longo**

Quando o comando anterior foi complexo e precisa de ajuste pontual:

```zsh
fc          # abre $EDITOR com o último comando
# edite, salve, feche → Zsh executa automaticamente
```

**Re-executar com tweak rápido**

```zsh
npm run test:unit
^unit^integration    # → npm run test:integration
```

**Comando privado (sem history)**

```zsh
 export TOKEN=valor_secreto    # espaço inicial = não grava
```

Requer `HIST_IGNORE_SPACE` ativo.

**Listar e inspecionar**

```zsh
history 1 | grep docker    # todos os comandos docker já executados
fc -l -20 -1              # os últimos 20 comandos numerados
```

---

## Armadilhas

### 1. `HISTSIZE` menor que `SAVEHIST`

**Causa:** configurar `HISTSIZE=1000` e `SAVEHIST=50000`. **Sintoma:** ao fechar o shell, apenas 1000 entradas são gravadas no `HISTFILE`, apagando as mais antigas além desse limite — mesmo que o arquivo tivesse mais. **Detectar:** `echo $HISTSIZE $SAVEHIST` — se `HISTSIZE < SAVEHIST`, há problema. **Solução:** sempre manter `HISTSIZE >= SAVEHIST`. O valor razoável hoje é 50000 para ambos (arquivos de history modernos são minúsculos em disco).

---

### 2. `SHARE_HISTORY` + edição manual do `HISTFILE`

**Causa:** editar `~/.zsh_history` manualmente (ex: para remover um comando com credencial) enquanto outra sessão Zsh está aberta e usando `SHARE_HISTORY`. **Sintoma:** ao fechar a sessão ativa, ela reescreve o `HISTFILE` a partir do seu estado em memória, sobrescrevendo as edições manuais. **Detectar:** comparar o arquivo depois de fechar a sessão com o que você editou. **Solução:** fechar todas as sessões Zsh antes de editar manualmente. Ou usar `fc -R ~/.zsh_history` para recarregar o arquivo na sessão ativa após editar.

---

### 3. `HIST_VERIFY` ausente + `!!` em comando destrutivo

**Causa:** não ter `HIST_VERIFY` ativo e executar `sudo !!` após um `rm -rf ~/tmp/pasta`. **Sintoma:** `sudo rm -rf ~/tmp/pasta` executa direto, sem confirmação adicional. **Detectar:** testar `!!` num prompt seguro — se executar imediatamente sem recarregar a linha, `HIST_VERIFY` não está ativo. **Solução:** adicionar `setopt HIST_VERIFY` ao `~/.zshrc`. Com ele, `!!` carrega a linha expandida no prompt; só executa ao pressionar `Enter` uma segunda vez.

---

### 4. Atuin sobrescrevendo `Ctrl-R` sem clareza

**Causa:** instalar atuin (ferramenta de history sincronizado e pesquisável) em um shell que já tem `history-substring-search` ou outro plugin bindando `Ctrl-R`. **Sintoma:** `Ctrl-R` abre a TUI do atuin em vez do search nativo, ou — pior — nenhum dos dois funciona porque os widgets do ZLE se sobrescrevem silenciosamente. **Detectar:** `bindkey | grep '^"\\C-r"'` mostra qual widget está bindado para `Ctrl-R`. **Solução:** escolher apenas uma ferramenta de search de history por vez. Atuin registra seu widget via shell hook de inicialização; desabilitar com `ATUIN_NOBIND=true` no `~/.zshrc` antes do `eval "$(atuin init zsh)"` permite carregar o atuin sem bindar o `Ctrl-R`.

---

## Em inglês

| PT-BR | EN | Frase técnica curta |
|---|---|---|
| Histórico do shell | Shell history | "Zsh persists shell history to a file across sessions." |
| Expansão de histórico | History expansion | "History expansion lets you reuse previous commands with `!!` and `!$`." |
| Pesquisa incremental | Incremental search | "Press `Ctrl-R` to start an incremental backward search through history." |
| Arquivo de histórico | History file | "The history file (`HISTFILE`) stores commands persistently on disk." |
| Duplicata | Duplicate | "`HIST_IGNORE_ALL_DUPS` removes older duplicate entries from history." |
| Timestamp | Timestamp | "`EXTENDED_HISTORY` saves a Unix timestamp alongside each command." |
| Comando privado | Private command / no-history command | "Prefix a command with a space to keep it out of history." |
| Corrigir comando | Fix command | "`fc` stands for 'fix command' — it opens the last command in an editor." |
| Designador de evento | Event designator | "Event designators (`!!`, `!n`, `!str`) identify which history entry to expand." |
| Designador de palavra | Word designator | "Word designators (`:$`, `:^`, `:*`) select specific words from the referenced event." |

---

## Veja também

- [[02 - Zsh essencial]] — `setopt` é pré-requisito para entender as opts de history
- [[06 - Keybindings práticos]] — plugin `history-substring-search` expande o `Ctrl-R`
- [[06 - Keybindings práticos]] — bindar `Ctrl-R` custom e gerenciar conflitos de widget
- [[03-Dominios/Tecnologia/Terminal/Shell/index|MOC do galho Shell]]
- [[Dicionário do Terminal#History|History]], [[Dicionário do Terminal#fc|fc]]

---

## Referências

- Zsh manual — Options (HIST_\*): <https://zsh.sourceforge.io/Doc/Release/Options.html#History>
- Zsh manual — Shell Builtins (`fc`): <https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html>
- Zsh manual — Expansion (History Expansion): <https://zsh.sourceforge.io/Doc/Release/Expansion.html#History-Expansion>
- Atuin — shell history sync: <https://atuin.sh/>
