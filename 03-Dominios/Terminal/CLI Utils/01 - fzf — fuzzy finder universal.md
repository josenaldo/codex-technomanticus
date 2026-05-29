---
title: "fzf — fuzzy finder universal"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - fzf
  - fuzzy
aliases:
  - fzf
  - Fuzzy finder
---

> [!abstract] TL;DR
> fzf é um fuzzy finder universal que lê stdin e devolve a seleção no stdout. Vira motor de seleção pra qualquer pipeline: history (Ctrl-R), files (Ctrl-T), cd (Alt-C), branches git, processos. Extended search syntax (`^prefix`, `suffix$`, `'exato`, `!negar`) afina matching. Configurável via `FZF_DEFAULT_OPTS` e `FZF_DEFAULT_COMMAND`. Ao adotar, o ganho é trocar `find ... | grep ...` por seleção interativa com preview.

## O que é / Como funciona

### Filosofia: filtro genérico stdin→stdout

fzf não é busca de arquivos — é filtro interativo de listas. Lê linhas do stdin, abre uma TUI com fuzzy matching em tempo real, e emite a seleção no stdout. Isso significa que ele compõe com qualquer comando que produza uma lista:

```bash
git branch | fzf
kubectl get pods | fzf
ps aux | fzf
cat /etc/hosts | fzf
```

Saída vai pro stdout como qualquer outro comando, podendo ser encadeada em novos pipes ou usada em command substitution (`$(fzf)`). Nenhuma integração especial com o sistema de arquivos — é um filtro genérico.

### Algoritmo fuzzy

O algoritmo de matching é aproximado por caracteres ordenados: `fmgo` casa `from_go`, `formula_path`, `format_message`. A pontuação combina:

- **consecutivos:** caracteres contíguos valem mais
- **início de palavra:** casar em boundary de palavra (após `-`, `_`, `/`, maiúscula) tem bônus
- **case match:** letra exata pesa mais que case-insensitive

O resultado: digitar alguns caracteres chave — geralmente as iniciais — é suficiente pra filtrar listas grandes para poucos candidatos, sem precisar lembrar a posição exata da substring.

### Extended search syntax

Quando `--extended` está ativo (default), fzf aceita modificadores que alteram o tipo de match por token:

| Token | Comportamento |
|---|---|
| `sbtrkt` | fuzzy match (padrão) |
| `'exato` | substring exata, sem fuzzy |
| `^prefixo` | prefixo — item começa com |
| `sufixo$` | sufixo — item termina com |
| `!negar` | exclusão — item NÃO contém |
| `!^inicio` | NÃO começa com |
| `!fim$` | NÃO termina com |
| `a b` | E lógico (ambos, ordem livre) |
| `a \| b` | OU lógico (qualquer um) |

Exemplos práticos:

```bash
# só arquivos .ts que não são .spec.ts
fzf --filter "'.ts$ !'.spec.ts$"

# começa com "feat" ou começa com "fix"
git log --oneline | fzf --filter "^feat | ^fix"
```

### Preview window

`--preview '<cmd>'` exibe um painel lateral com saída de um comando aplicado ao item em destaque. Substituições:

- `{}` — item inteiro
- `{1}`, `{2}` — campos (separados por espaço por default)
- `{n}` — campo N; `{-1}` — último campo

Layout via `--preview-window`:

```bash
fzf --preview 'bat --color=always {}' \
    --preview-window 'right:60%:wrap'

# posição: right, left, up, down
# tamanho: percentual ou número fixo de linhas/colunas
# :wrap — wrapping de linhas longas
# :hidden — começa oculto (toggle com ?/Ctrl-/ etc.)
```

### Integração com shell

A instalação adiciona bindings automáticos ao shell (Zsh/Bash/Fish). A partir de fzf 0.4x+, o método moderno é:

```bash
# Zsh
source <(fzf --zsh)

# Bash
eval "$(fzf --bash)"
```

Bindings default:

| Atalho | Ação |
|---|---|
| `Ctrl-R` | Busca interativa no history (cola no prompt) |
| `Ctrl-T` | Seleciona arquivo/dir e cola no prompt |
| `Alt-C` | `cd` no diretório selecionado |
| `<cmd>**<TAB>` | Completion expansion fuzzy pra `<cmd>` |

Comportamento de cada binding é customizável com env vars específicas (ver seção "Na prática").

## Na prática

### Setup básico

Instalar via package manager e ativar integração com shell:

```bash
# Ubuntu/Debian
sudo apt install fzf

# macOS (Homebrew)
brew install fzf

# Ativar bindings e completion no Zsh (adicionar ao .zshrc)
source <(fzf --zsh)
```

Verificar versão instalada:

```bash
fzf --version
# fzf 0.7x.y (...)
```

O bloco `source <(fzf --zsh)` é idempotente — pode ser chamado múltiplas vezes sem efeito colateral.

### Env vars úteis

Definir no `.zshrc` (ou `.bashrc`):

```bash
# Comando default quando input é tty (Ctrl-T e fzf sem pipe)
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'

# Ctrl-T usa o mesmo comando
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# Layout default pra todas as invocações
export FZF_DEFAULT_OPTS="--height 60% --layout=reverse --border --preview-window=right:50%:wrap"

# Ctrl-R com preview do comando completo
export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window down:3:hidden:wrap --bind '?:toggle-preview'"

# Alt-C mostra preview da árvore de diretório
export FZF_ALT_C_OPTS="--preview 'tree -C {} | head -50'"
```

### Receitas comuns

**Selecionar branch git e fazer checkout:**

```bash
git checkout "$(git branch --format='%(refname:short)' | fzf)"
```

**Kill processo interativo:**

```bash
ps aux | fzf | awk '{print $2}' | xargs -r kill
```

**Abrir arquivo com preview (requer `bat` e `fd`):**

```bash
nvim "$(fd -t f | fzf --preview 'bat --color=always {}')"
```

**Buscar conteúdo com ripgrep e navegar resultado:**

```bash
rg --line-number '' | fzf --delimiter ':' \
  --preview 'bat --color=always --highlight-line {2} {1}' \
  --preview-window 'right:60%:+{2}+3/3:wrap'
```

**Selecionar múltiplos arquivos (`-m`) e abrir no editor:**

```bash
nvim $(fd -t f | fzf -m)
```

### Integração com Neovim

fzf.vim é um plugin que integra o binário fzf externo diretamente no Neovim, abrindo a TUI do fzf dentro de um buffer flutuante. Telescope é plugin Neovim escrito em Lua com fuzzy finder próprio — não depende do binário fzf instalado. Em LazyVim, Telescope é o default (`<leader>ff`, `<leader>fg`). Os dois coexistem; fzf.vim é mais próximo da experiência shell, Telescope tem mais integrações nativas com LSP e Treesitter.

### Versão hedged

fzf 0.7x+; verifique `fzf --version` localmente. O projeto evolui ativamente — consultar o changelog pra recursos recentes como `--popup`, `--header-border`, e integração Zellij.

## Armadilhas

### (1) Extended search syntax confusa

**Causa:** confundir `'exato` (substring exata sem fuzzy) com `^prefixo` (começa com).

**Sintoma:** filtro não casa o esperado — `'foo` mostra resultados com "foo" em qualquer posição, não apenas no começo.

**Como detectar:** testar com input controlado: criar lista com `printf 'foobar\nbarfoo\n'` e comparar `'foo` vs `^foo`.

**Solução:** lembrar que `'` desativa fuzzy mas não ancora — casa substring exata em qualquer posição. Use `^` pra prefixo e `$` pra sufixo. Referência: seção "Search syntax" no README do fzf.

### (2) FZF_DEFAULT_COMMAND ignorando .gitignore

**Causa:** o fallback default do fzf é `find .` sem filtros.

**Sintoma:** `Ctrl-T` mostra milhares de arquivos irrelevantes — node_modules, .git, dist, __pycache__.

**Como detectar:** `echo $FZF_DEFAULT_COMMAND` — se vazio ou com `find` puro, o problema é esse.

**Solução:** setar `FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'` no `.zshrc`. Se `fd`/`fdfind` não estiver instalado, alternativa: `rg --files --hidden --follow --glob '!.git'`.

### (3) Preview lento ou corrompendo terminal

**Causa:** preview com `cat` em binário, ou comando custoso sem proteção.

**Sintoma:** UI lagada com arquivos grandes; terminal corrompido ao previewar binários (PDFs, imagens, executáveis).

**Como detectar:** selecionar um arquivo binário e observar saída garbage no painel de preview.

**Solução:** usar `bat` como previewer — detecta binários automaticamente e exibe aviso. Wrapper defensivo:

```bash
--preview 'file {} | head -1; bat --color=always {} 2>/dev/null || echo "[binary — sem preview]"'
```

### (4) Bindings conflitando com multiplexer

**Causa:** `Ctrl-T` ou `Alt-C` reservados pelo Zellij ou tmux no layout ativo.

**Sintoma:** o atalho do fzf não aciona — o multiplexer intercepta antes de chegar ao shell.

**Como detectar:** abrir terminal sem multiplexer (terminal emulador direto) e testar — se funcionar lá, o conflito é no multiplexer.

**Solução:** rebindar a ação conflitante no multiplexer para liberar a tecla, ou redefinir o binding do fzf via `bindkey` para uma sequência não usada pelo multiplexer.

### (5) `**<TAB>` completion falhando em comandos específicos

**Causa:** a completion expansion do fzf não é universal — depende de wrappers `_fzf_complete_<cmd>` definidos por comando.

**Sintoma:** `ssh **<TAB>` ou `kill **<TAB>` não popula lista interativa, mesmo com fzf instalado e outros completions funcionando.

**Como detectar:** testar com outros comandos (`cd **<TAB>`, `cat **<TAB>`) — alguns funcionam, outros não.

**Solução:** verificar funções `_fzf_complete_<cmd>` disponíveis (ex: `_fzf_compgen_path`, `_fzf_compgen_dir`). Para comandos não cobertos, definir wrapper custom — ver seção "Custom fuzzy completion" no README.

### (6) Output com espaços quebrando consumidores

**Causa:** fzf emite a string selecionada raw; consumer (cd, ssh, cp) recebe path com espaço sem aspas.

**Sintoma:** `cd $(fzf)` falha com `cd: too many arguments` ao selecionar path como `meu projeto/src`.

**Como detectar:** selecionar deliberadamente um item com espaço no nome e observar o comportamento.

**Solução:** aspas duplas no command substitution sempre:

```bash
cd "$(fzf)"
nvim "$(fd -t f | fzf)"
```

Para múltiplos itens com `--print0`:

```bash
fd -t f | fzf -m --print0 | xargs -0 nvim
```

## Em inglês

- **Fuzzy finder** — *fuzzy finder*. "fzf é o fuzzy finder canônico do shell: filtra listas grandes por match aproximado."
- **Extended search syntax** — *extended search syntax*. "A extended search syntax do fzf estende o fuzzy match com âncoras (`^`, `$`) e exclusões (`!`)."
- **Preview window** — *preview window*. "A preview window exibe o conteúdo do item selecionado em um painel lateral configurável."
- **Key binding** — *key binding* (ou *keybinding*). "Os key bindings default do fzf no shell são Ctrl-R, Ctrl-T e Alt-C."
- **Env var** — *environment variable*. "Env vars como `FZF_DEFAULT_OPTS` e `FZF_DEFAULT_COMMAND` configuram o comportamento global do fzf."
- **Completion** — *completion*. "A integração de completion do fzf permite expandir `comando **<TAB>` em seleção interativa fuzzy."
- **Pipe** — *pipe*. "fzf é projetado pra viver em pipes: qualquer comando que produza lista pode ser filtrado por ele."
- **Stdin/stdout** — *stdin/stdout*. "fzf lê do stdin e emite a seleção no stdout — composição pura de Unix."
- **Command substitution** — *command substitution*. "Use command substitution com aspas duplas (`"$(fzf)"`) ao passar o resultado pra comandos que aceitam paths."
- **Widget (shell)** — *shell widget*. "Os bindings Ctrl-R e Ctrl-T são shell widgets registrados no ZLE do Zsh."

## Veja também

- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — fd como fonte default pra `FZF_DEFAULT_COMMAND`
- [[03 - bat — cat moderno com syntax highlight]] — bat como preview de arquivos
- [[12 - Stack interativo — fzf zoxide atuin]] — composição capstone
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#fuzzy finder|fuzzy finder]]
- [[Dicionário do Terminal#extended search syntax (fzf)|extended search syntax]]
- [[Dicionário do Terminal#preview window (fzf)|preview window]]
- [[Dicionário do Terminal#FZF_DEFAULT_OPTS|FZF_DEFAULT_OPTS]]
- [[Dicionário do Terminal#Telescope|Telescope]] — contraponto no Neovim

## Referências

- GitHub fzf: https://github.com/junegunn/fzf
- fzf wiki examples: https://github.com/junegunn/fzf/wiki/examples
- fzf changelog: https://github.com/junegunn/fzf/blob/master/CHANGELOG.md
