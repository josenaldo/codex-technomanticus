---
title: "Completion system (compsys)"
created: 2026-05-19
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - compsys
  - completion
aliases:
  - Compsys
  - Completion system
---

# Completion system (compsys)

## TL;DR

Compsys é o sistema de completion programável do Zsh. `compinit` inicializa, lê `fpath` pra encontrar funções `_<comando>`, e gera `~/.zcompdump` (cache). `compdef` registra função pra comando. `zstyle` customiza apresentação. Quando completion "não funciona": geralmente é `.zcompdump` velho ou fpath errado.

---

## O que é / Como funciona

### Modelo

Completion = "Tab autocompleta comando, argumento, path, …"

O compsys é um sistema **programável**: cada comando pode ter uma função `_<comando>` que diz "como completar" — argumentos esperados, sub-comandos, flags válidas. Isso é bem diferente de um simples listador de arquivos.

- Funções de completion vivem em arquivos no `fpath` (search path de funções), nomes começando com `_`
- Ao primeiro Tab num comando, Zsh faz autoload da função e a executa
- O resultado é um menu, uma inserção direta, ou uma lista de opções — dependendo de quantos matches existem e de como o `zstyle` está configurado

### `compinit`

Builtin que inicializa o compsys:

- Lê `fpath`, indexa funções `_<*>`
- Gera/atualiza `~/.zcompdump` (cache binário compilado)
- Roda em modo "security check" por default (verifica permissões dos dirs em fpath)

Setup canônico (já feito por OMZ; documentado aqui pra contexto):

```zsh
autoload -Uz compinit
compinit
```

Variações úteis:

- `compinit -i` — ignora arquivos inseguros (não falha, continua)
- `compinit -C` — pula security check (mais rápido, menos seguro; aceitar tradeoff conscientemente)
- `compinit -d <path>` — usa caminho alternativo ao `~/.zcompdump` default

### `compdef`

Registra função de completion pra um comando:

```zsh
compdef _git mygit              # mygit completa como git
compdef '_files -g "*.log"' tail # tail completa só arquivos .log
```

Útil pra binários novos que não trazem completion, ou aliases que precisam de completion específica. O primeiro argumento é a função (ou spec inline); o segundo é o comando a registrar.

### `fpath`

Array com diretórios onde Zsh procura funções autoload (incluindo `_<comando>`). OMZ adiciona `$ZSH/plugins/*/` e `$ZSH/completions/` ao fpath automaticamente ao ser sourced.

```zsh
# Ver fpath (um por linha)
print -l $fpath

# Adicionar diretório de completion custom
fpath=(~/.zsh-custom-completions $fpath)
autoload -Uz compinit && compinit
```

O diretório deve ser adicionado **antes** de `compinit` — depois de inicializado, o cache já foi gerado sem a nova entrada.

### Como Zsh decide o que completar

1. Você digita `git ch<Tab>`
2. ZLE dispatcha o widget `expand-or-complete`
3. O widget chama o compsys, que parseia o command-line: comando = `git`, argumento atual = `ch`
4. Compsys busca `_git` no fpath; se não carregada ainda, faz autoload
5. `_git` define: "primeiro arg de `git` é sub-comando; lista X opções"
6. Compsys filtra opções que começam com `ch` (case-insensitive se configurado via `zstyle`)
7. Exibe menu navegável ou insere diretamente se há só um match

Esse fluxo mostra por que `_git` precisa estar no fpath e por que `compinit` precisa ter rodado: sem o índice, o compsys não sabe onde procurar a função.

### `zstyle` — customização

`zstyle '<context>' '<style>' '<value>'` controla aspectos do compsys (e de outros sistemas Zsh). O contexto `:completion:*` se aplica a toda completion; contextos mais específicos sobrescrevem os gerais.

Configs essenciais:

```zsh
# Case-insensitive: minúscula casa com Minúscula/Maiúscula
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

# Menu navegável com setas (sem isso, Tab só lista)
zstyle ':completion:*' menu select

# Cabeçalho indicando o que está completando
zstyle ':completion:*' format 'Completing %d'

# Agrupar matches por tipo (commands, options, files)
zstyle ':completion:*' group-name ''

# Cores no menu (precisa LS_COLORS exportado)
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

# Não dar match a funções internas (começam com _)
zstyle ':completion:*:functions' ignored-patterns '_*'
```

Ver todos os zstyles configurados: `zstyle -L`

---

## Na prática

### Setup mínimo manual (sem OMZ)

Para quem usa Zsh sem framework, o setup mínimo funcional é:

```zsh
autoload -Uz compinit
compinit
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' menu select
```

Colocar no `.zshrc`, antes de qualquer adição ao fpath. Se quiser completions de ferramentas específicas (ex: `kubectl`, `gh`), gerar via comando da ferramenta e adicionar o diretório ao fpath antes do `compinit`.

Exemplo com kubectl:

```zsh
# Gera completion em arquivo
mkdir -p ~/.zsh-completions
kubectl completion zsh > ~/.zsh-completions/_kubectl

# Adicionar antes do compinit no .zshrc
fpath=(~/.zsh-completions $fpath)
autoload -Uz compinit
compinit
```

### Troubleshooting

**Completion para um comando "sumiu" após instalar plugin:**

```zsh
# Verifica se a função existe
which _<comando>

# Mostra origem da função
whence -v _<comando>

# Listas dirs com permissões suspeitas em fpath
compaudit
```

**.zcompdump corrompido (após mudança de plugins, atualização do OMZ, adição de fpath):**

```bash
rm ~/.zcompdump*
compinit
```

Esse é o troubleshooting mais comum. Sempre que algo mudar no fpath ou nos plugins, o cache precisa ser regenerado.

**`compinit` lento na startup:**

```bash
# Mede tempo total de startup do shell
time zsh -i -c exit
```

Opções para acelerar:

- `compinit -C` — pula security check, ganha ~100-200ms dependendo do setup; aceitar o tradeoff conscientemente
- Plugin `zsh-defer` (romkatv/zsh-defer) — adia `compinit` para depois do primeiro prompt aparecer; melhora tempo de startup percebido sem sacrificar funcionalidade

**`compaudit` reclamando de permissões:**

```bash
compaudit | xargs chmod g-w,o-w
```

Esse fix corrige group-writable e other-writable nos diretórios listados. Após corrigir, `compinit` deixa de reclamar sem precisar de `-i`.

### Plugins que mexem em completion

**fzf-tab** (`Aloxaf/fzf-tab`): substitui o menu builtin de completion por uma interface `fzf` — UX moderna com preview interativo. Deve ser sourced **antes** de `zsh-syntax-highlighting`. Compatível com o compsys default — não sobrescreve `zstyle` nem redefinição de widgets de forma destrutiva.

**zsh-autocomplete** (`marlonrichert/zsh-autocomplete`): exibe sugestões de completion em tempo real enquanto você digita, sem pressionar Tab. Modifica o fluxo de Tab e vários zstyles agressivamente. **Incompatível** com `fzf-tab` se usados simultaneamente — os dois competem pelo controle das completions. Requer Zsh 5.8+.

Decisão antes de adotar um dos dois: escolha uma estratégia (default OMZ, `fzf-tab`, ou `zsh-autocomplete`) e não misture.

---

## Armadilhas

### 1. `.zcompdump` órfão após instalar plugin

**Causa:** `compinit` gera um cache binário (`~/.zcompdump`) que indexa funções de completion disponíveis no fpath no momento em que rodou. Quando um novo plugin é instalado e adiciona novas funções `_<comando>` ao fpath, o cache antigo ainda não conhece essas funções.

**Sintoma:** `_<comando>` existe no fpath mas Tab não produz completion para esse comando. Funciona como se a função não existisse.

**Como detectar:** `ls -la ~/.zcompdump*` mostra um mtime anterior à instalação do plugin; `which _<comando>` mostra a função existindo no fpath. Essa contradição confirma o cache órfão.

**Solução:** `rm ~/.zcompdump* && compinit` — regenera o cache incluindo as funções novas.

---

### 2. Ordem do fpath importa: dois plugins com `_<comando>` competem

**Causa:** Se dois plugins (ou um plugin e um diretório custom) fornecem funções `_<comando>` com o mesmo nome, o compsys usa aquela que aparece **primeiro** no fpath — a ordem em que os diretórios foram adicionados determina o vencedor.

**Sintoma:** Completion funciona, mas usa lógica errada ou desatualizada — por exemplo, a versão bundled do OMZ em vez da versão mais nova que você instalou em `~/.zsh-completions/`.

**Como detectar:** `print -l $fpath` mostra a ordem dos diretórios. `whence -v _<comando>` mostra exatamente qual arquivo foi carregado e de qual diretório.

**Solução:** Colocar o diretório preferido **antes** no fpath: `fpath=(~/.zsh-completions $fpath)`. Depois `rm ~/.zcompdump* && compinit`.

---

### 3. `compaudit` dispara no install novo do OMZ (dirs com permissões group-writable)

**Causa:** OMZ clona seu repositório com permissões que às vezes deixam diretórios group-writable (modo 775 em vez de 755), dependendo do `umask` do sistema. O `compinit` rejeita esses diretórios em seu security check por padrão.

**Sintoma:** `compinit` imprime mensagem "There are insecure directories and files in your…" e `[1] ignore insecure directories and files, [2] exit?`. Completion pode ficar parcial ou não inicializar completamente.

**Como detectar:** `compaudit` lista os diretórios problemáticos com suas permissões.

**Solução:** Corrigir as permissões diretamente:

```bash
compaudit | xargs chmod g-w,o-w
```

Alternativa temporária (não recomendada como fix permanente): `compinit -i` para ignorar arquivos inseguros na inicialização.

---

### 4. `compinit` rodando duas vezes degrada startup

**Causa:** OMZ roda `compinit` internamente no seu script de carregamento (`lib/completion.zsh`). Se o usuário adiciona uma segunda chamada a `compinit` no `.zshrc` depois do `source "$ZSH/oh-my-zsh.sh"`, o compsys é inicializado duas vezes, reindexando o fpath e regravando o cache sem necessidade.

**Sintoma:** Startup do shell mais lento que o esperado; cada nova janela de terminal demora visivelmente mais que o normal.

**Como detectar:**

```bash
zsh -i -c exit -x 2>&1 | grep compinit | wc -l
```

Se o resultado for maior que 1, há chamadas duplicadas.

**Solução:** Não chamar `compinit` manualmente no `.zshrc` quando já usa OMZ. Deixar o framework gerenciar a inicialização do compsys. Se quiser adicionar diretórios ao fpath, adicione **antes** do `source "$ZSH/oh-my-zsh.sh"`.

---

### 5. `zsh-autocomplete` + sistema de completion default: comportamentos conflitantes

**Causa:** `zsh-autocomplete` redefine vários zstyles e widgets de completion do compsys para implementar seu fluxo de sugestões em tempo real. Esse redesign é intencional — o plugin quer substituir, não complementar, o sistema default. Ao mesmo tempo, `fzf-tab` também substitui o widget de menu do compsys. Ambos ativos ao mesmo tempo: os dois competem pelo mesmo ponto de intercepção.

**Sintoma:** Tab se comporta de forma imprevisível — às vezes abre o menu do fzf, às vezes o menu do zsh-autocomplete, às vezes não faz nada. `zstyle -L` mostra dezenas de overrides conflitantes.

**Como detectar:** `zstyle -L | wc -l` — um número muito alto de zstyles (acima de ~50) em setup básico indica que algum plugin está sobrescrevendo agressivamente. `zle -l | grep complete` mostra múltiplos widgets de completion registrados por fontes diferentes.

**Solução:** Escolher **uma** estratégia de completion e remover as concorrentes:
- Default OMZ (sem plugins extras de completion): funcional, estável
- `fzf-tab`: UX moderna, compatível com compsys default
- `zsh-autocomplete`: mudança de paradigma, incompatível com os outros dois

Ao migrar de `zsh-autocomplete` para outra estratégia: remover o plugin do array `plugins=(...)`, deletar `~/.zcompdump*`, e recarregar o shell.

---

## Em inglês

- **completar** — *complete*. "Press Tab to complete the current argument."
- **sistema de completion** — *completion system*. "The Zsh completion system is programmable via functions in fpath."
- **inicializar** — *initialize*. "Run `compinit` to initialize the completion system on startup."
- **função de completion** — *completion function*. "Each command can have a completion function named `_<command>` in fpath."
- **arquivo de cache** — *cache file*. "The `~/.zcompdump` file is the cache generated by compinit."
- **reconstruir** — *rebuild*. "Delete `~/.zcompdump` and rerun `compinit` to rebuild the completion cache."
- **permissão insegura** — *insecure permission*. "Run `compaudit` to list directories with insecure permissions in fpath."
- **match** — *match*. "The matcher-list style controls which completions match the typed prefix."
- **agrupar** — *group*. "Set `group-name ''` to group completion matches by type."
- **sub-comando** — *sub-command*. "The `_git` function defines completions for each git sub-command."

---

## Veja também

- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]] — OMZ já chama `compinit`
- [[06 - Keybindings práticos]] — Tab é um binding ZLE
- [[07 - ZLE]] — widgets de completion vivem aqui
- [[10 - Plugins, themes e custom no OMZ]] — escrever `_<comando>` próprio
- [[03-Dominios/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Compsys|compsys]], [[Dicionário do Terminal#Compinit|compinit]], [[Dicionário do Terminal#Compdef|compdef]], [[Dicionário do Terminal#Fpath|fpath]], [[Dicionário do Terminal#Zstyle|zstyle]]

---

## Referências

- Zsh manual — Completion System: https://zsh.sourceforge.io/Doc/Release/Completion-System.html
- Zsh manual — Completion Widgets: https://zsh.sourceforge.io/Doc/Release/Completion-Widgets.html
- fzf-tab README: https://github.com/Aloxaf/fzf-tab
- zsh-autocomplete README: https://github.com/marlonrichert/zsh-autocomplete
