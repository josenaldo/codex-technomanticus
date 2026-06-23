---
title: "Stack interativo — fzf zoxide atuin"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - fzf
  - zoxide
  - atuin
  - composicao
aliases:
  - Stack interativo
  - fzf zoxide atuin
---

> [!abstract] TL;DR
> Capstone — fzf + zoxide + atuin compondo o fluxo diário. zoxide pula pastas via frecency; atuin substitui Ctrl-R com fuzzy search rico; fzf é motor de seleção compartilhado (`zi` usa fzf; atuin tem TUI própria parecida). Init order importa: atuin DEPOIS de plugins zsh que mexem em Ctrl-R; zoxide pode vir antes. `FZF_DEFAULT_OPTS` aplica-se a todos. Assume leitura das notas [[01 - fzf — fuzzy finder universal]], [[05 - zoxide — cd inteligente com frecency]] e [[06 - atuin — history shell com SQLite e sync]].

## O que é / Como funciona

### As três peças do quebra-cabeça

- **zoxide** — "para onde ir" (pastas)
- **atuin** — "o que eu fiz antes" (history rico)
- **fzf** — "como escolher rapidamente" (motor de seleção)

Sozinhas, cada uma resolve um problema; juntas, viram o loop diário:

1. `z proj` — pula pra pasta do projeto (zoxide)
2. `Ctrl-R "deploy"` — recupera último deploy via atuin (TUI fuzzy)
3. `Ctrl-T` ou `**<TAB>` — completa paths via fzf (Zsh widget)

### Init order no shell (importa)

```bash
# ~/.zshrc — order matters

# 1. Plugin manager (oh-my-zsh, zinit, prezto) — primeiro de tudo
source ~/.config/zinit/zinit.zsh

# 2. Plugins (autosuggestions, syntax-highlighting, completions)
zinit light zsh-users/zsh-autosuggestions
zinit light zdharma-continuum/fast-syntax-highlighting

# 3. zoxide — antes ou depois de fzf, sem conflito direto
eval "$(zoxide init zsh)"

# 4. atuin — DEPOIS de plugins que mexem em Ctrl-R
eval "$(atuin init zsh)"

# 5. fzf bindings — opcionalmente DEPOIS de atuin
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

Plugin manager primeiro. Plugins depois. Init scripts das ferramentas (zoxide → atuin → fzf) por último — o que sobrescreve Ctrl-R por último ganha o binding.

### Compartilhar config visual com FZF_DEFAULT_OPTS

```bash
export FZF_DEFAULT_OPTS="
  --height 60%
  --layout=reverse
  --border=rounded
  --bind 'ctrl-/:toggle-preview'
"
```

atuin não usa `FZF_DEFAULT_OPTS` diretamente (TUI própria), mas tem opções equivalentes em `~/.config/atuin/config.toml` (`inline_height`, `style`).

`FZF_CTRL_T_OPTS` e `FZF_CTRL_R_OPTS` permitem customizar bindings específicos sem afetar todo o fzf.

## Na prática

### Setup do zero em máquina nova

```bash
# Instalar via package manager preferido
# Adicionar ao ~/.zshrc na ordem certa (ver acima)

# Importar histórico zsh pro atuin
atuin import zsh

# Verificar bindings
bindkey '^R'                # deve mostrar atuin widget
bindkey '^T'                # deve mostrar fzf widget

# Treinar zoxide (rodar cd manualmente nos primeiros dias)
cd ~/work/myproj
cd ~/personal/dotfiles
# Em alguns dias, `z proj` já funciona
```

### Receitas compostas

```bash
# Pular pra pasta + escolher arquivo (zoxide → fzf → bat preview)
cd "$(zoxide query -l | fzf --preview 'eza --tree -L 2 {}')"
nvim "$(fd -t f | fzf --preview 'bat --color=always {}')"

# Buscar comando recente filtrado por pasta atual (atuin)
atuin search --cwd "$(pwd)" --search-mode fuzzy "git"

# Trocar branch via fzf (preview do log)
git checkout "$(git branch --format='%(refname:short)' | fzf --preview 'git log --oneline -10 {}')"

# Achar commit pra cherry-pick
git log --oneline | fzf --preview 'git show --color {1}' | awk '{print $1}'
```

### FZF customizado por binding

```bash
export FZF_CTRL_T_OPTS="--preview 'bat --color=always {}'"
export FZF_CTRL_R_OPTS="--preview 'echo {}' --preview-window=down:3:hidden"
export FZF_ALT_C_OPTS="--preview 'eza --tree -L 2 {}'"
```

Cada binding ganha preview apropriado pro tipo de item (arquivo → bat; comando → echo; pasta → eza tree).

### Convergência: por que esse stack

- Todas as 3 são Rust (binários standalone, sem deps runtime)
- Todas defendem TTY-aware behavior (funcionam em pipe sem quebrar scripts)
- Todas usam frecency-like ranking em algum lugar (zoxide explícito; atuin em ordering interno)

### Configurações finas

**Atuin sem auto-sync (sync manual):**

```toml
# ~/.config/atuin/config.toml
auto_sync = false
search_mode = "fuzzy"
inline_height = 25
style = "compact"
```

**zoxide com `cd` substituído:**

```bash
eval "$(zoxide init zsh --cmd cd)"
# Agora `cd foo` é zoxide search; `cd /caminho/absoluto` ainda funciona
# Trade-off: ergonômico; menos óbvio quando vê script seu
```

### Versão hedged

Verifique localmente: fzf 0.4x+, zoxide 0.9+, atuin 18+.

## Armadilhas

### (1) Init order quebra Ctrl-R

**Causa:** plugin Zsh (oh-my-zsh, fast-syntax-highlighting) que mexe em Ctrl-R carregado DEPOIS do `atuin init`.

**Sintoma:** Ctrl-R abre history clássico (`_history-incremental-search-backward`), não atuin TUI.

**Como detectar:** `bindkey '^R'` retorna widget de outro plugin em vez de `atuin`.

**Solução:** mover `eval "$(atuin init zsh)"` pro FIM do `.zshrc`, depois de tudo que mexe em bindkey.

### (2) zsh widget collisions

**Causa:** zoxide, atuin e plugin manager tentam definir o mesmo widget name (raro mas acontece em configs complexas).

**Sintoma:** binding intermitente; mensagem `widget already defined` no startup.

**Como detectar:** `zsh -lic exit 2>&1 | grep -i widget`.

**Solução:** ler logs de startup; renomear widget conflitante (raro precisar). Geralmente init order resolve.

### (3) `FZF_DEFAULT_OPTS` com preview pesado lentando tudo

**Causa:** colocar `--preview 'bat ...'` em `FZF_DEFAULT_OPTS` aplica em TODA invocação fzf — inclusive Ctrl-R (que mostra comandos, não files).

**Sintoma:** Ctrl-R lento; preview de comandos tenta bat e quebra.

**Como detectar:** lag perceptível em Ctrl-R; preview vazio ou estranho.

**Solução:** **NÃO** colocar `--preview` em `FZF_DEFAULT_OPTS`. Usar `FZF_CTRL_T_OPTS` pra preview de files; deixar `FZF_CTRL_R_OPTS` limpo.

### (4) atuin e zoxide ambos rastreando "lugares" — mental model

**Causa:** atuin rastreia cwd em cada comando; zoxide rastreia cwd em cada `cd`. Semânticas diferentes.

**Sintoma:** `atuin search --cwd /foo` mostra comandos rodados ali; `z foo` pula pra `/foo` mais frecente. Confusão de qual ferramenta "lembra" o quê.

**Como detectar:** notar uso sobreposto sem entender o domínio.

**Solução:** mental model claro — zoxide = "onde ir"; atuin = "o que fiz onde". Não competem; complementam.

### (5) Reinstalar shell init silently breaks

**Causa:** trocar shell ou reinstalar dotfiles pode sobrescrever `.zshrc` sem os `eval init` das ferramentas.

**Sintoma:** próximo shell aberto não tem `z`, Ctrl-R clássico voltou.

**Como detectar:** `command -v z` falha; `bindkey '^R'` aponta pra widget default.

**Solução:** dotfiles versionados (galho 5) com `.zshrc` controlado. Bootstrap script (galho 5 nota 08) reaplica configs e roda `eval init`s.

### (6) atuin sync com self-host quebra após troca de domínio/IP

**Causa:** `sync_address` no atuin config tem IP/hostname antigo do self-host; mudou e config não foi atualizada.

**Sintoma:** `atuin sync` retorna erro de connection refused ou DNS.

**Como detectar:** `atuin sync` logs explícitos.

**Solução:** atualizar `sync_address` em `~/.config/atuin/config.toml`. Se key ainda válida, sync resume; se nova instância sem dados, restaurar via backup `~/.local/share/atuin/history.db`.

## Em inglês

- **Ordem de inicialização** — *init order*. "Init order do shell determina qual ferramenta ganha o binding final."
- **Widget** — *widget*. "Cada widget Zsh responde a uma keypress específica."
- **Atalho de teclado** — *key binding*. "Ctrl-R é o key binding clássico pra history search."
- **Frecency** — *frecency*. "Tanto zoxide quanto atuin usam frecency pra ranquear resultados."
- **Composição** — *composition*. "A composition entre as três ferramentas vira maior que a soma."
- **Capstone** — *capstone*. "Esta nota é o capstone das três individuais."
- **Pesquisa fuzzy** — *fuzzy search*. "fzf é o engine fuzzy search compartilhado."
- **Histórico** — *history*. "atuin substitui o shell history puro por uma DB SQLite."
- **Diretório de trabalho** — *working directory*. "O working directory atual é capturado por atuin em cada comando."
- **Variável de ambiente** — *environment variable*. "`FZF_DEFAULT_OPTS` é a env variable pra opções globais do fzf."

## Veja também

- [[01 - fzf — fuzzy finder universal]] — motor de seleção
- [[05 - zoxide — cd inteligente com frecency]] — pastas via frecency
- [[06 - atuin — history shell com SQLite e sync]] — history rico
- [[13 - Pipeline JSON e YAML — jq yq fzf]] — outro capstone (composição em dados estruturados)
- [[03-Dominios/Tecnologia/Terminal/Shell/index|Shell (galho 2)]] — Zsh + OMZ; base pros init scripts
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#zsh widget|zsh widget]]
- [[Dicionário do Terminal#init script (shell)|init script (shell)]]
- [[Dicionário do Terminal#FZF_DEFAULT_OPTS|FZF_DEFAULT_OPTS]]
- [[Dicionário do Terminal#frecency|frecency]]

## Referências

- fzf wiki: https://github.com/junegunn/fzf/wiki
- zoxide wiki: https://github.com/ajeetdsouza/zoxide/wiki
- atuin docs: https://docs.atuin.sh/
