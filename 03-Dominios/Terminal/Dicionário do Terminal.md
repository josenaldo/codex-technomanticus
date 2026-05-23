---
title: "Dicionário do Terminal"
created: 2026-05-19
updated: 2026-05-22
type: glossary
status: seedling
aliases: []
tags:
  - glossary
  - terminal
lang: pt
publish: true
---

# Dicionário do Terminal

> Glossário do domínio Terminal: jargão de editor (Neovim, LazyVim, modal editing), shell, multiplexer, TUIs e workflow. Cada verbete é referenciado por uma ou mais notas das trilhas do domínio.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática.
- Verbetes em ordem alfabética dentro de cada bloco.
- Linkar de outra nota: [[Dicionário do Terminal#Nome do termo]]
- Customizar texto exibido: [[Dicionário do Terminal#Nome do termo|texto]]
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Ajuste `lang:` no frontmatter (`pt` ou `en`) — define o idioma das definições.
- Cada verbete tem (i) 1-3 frases de definição em PT-BR e (ii) "Veja também:" com wikilinks para a(s) nota(s) que aprofundam.
-->

## Vim / Neovim core

### Autocmd
Comando que dispara automaticamente em eventos do Neovim (salvar arquivo, abrir buffer, mudar tipo, etc.). Em Lua: `vim.api.nvim_create_autocmd`. Agrupados em `augroup` pra evitar duplicação ao recarregar config.

Veja também: [[06 - Estrutura de config]].

### Buffer
Representação em memória de um arquivo aberto no Neovim. Independente de windows e tabs — N buffers podem estar abertos sem nenhum visível, e o mesmo buffer pode aparecer em várias windows.

Veja também: [[03 - Edição e navegação]].

### Jump list
Pilha de saltos que o Neovim mantém para cada window. Comandos como `gd`, `*`, `}`, `/` empurram a posição. Navegar: `<C-o>` (back), `<C-i>` (forward). Listar: `:jumps`.

Veja também: [[03 - Edição e navegação]].

### Keymap
**Em Neovim:** mapeamento de uma sequência de teclas pra uma ação. Em Neovim moderno: `vim.keymap.set(mode, lhs, rhs, opts)`. Opções comuns: `desc` (descrição visível em which-key), `silent`, `noremap` (default true em vim.keymap.set).

**Em Zsh (ZLE):** conjunto nomeado de bindings de tecla → widget. Keymaps disponíveis: `main` (alias do default), `emacs`, `viins` (vi insert), `vicmd` (vi normal), `command` (vi `:`). Selecionado por `bindkey -e` (emacs, default) ou `bindkey -v` (vi). Binding em keymap específico: `bindkey -M vicmd '<seq>' <widget>`.

Veja também: [[06 - Estrutura de config]], [[06 - Keybindings práticos]].

### Leader key
Tecla "prefixo" pra atalhos custom. Default Neovim: `\`. Em LazyVim: `<Space>`. Configurada com `vim.g.mapleader = " "` ANTES de plugins carregarem.

Veja também: [[06 - Estrutura de config]], [[08 - Customizando LazyVim]].

### Macro
Sequência de teclas gravada e replicável em Neovim. Gravar: `q<reg>` + teclas + `q`. Replay: `@<reg>` (uma vez), `@@` (último), `N@<reg>` (N vezes). O macro é um register editável — `:put a` mostra/edita.

Veja também: [[10 - Registers, marks, macros]].

### Mark
Posição salva (linha + coluna) em um buffer. Locais (`a`-`z`, scope buffer) ou globais (`A`-`Z`, persistem entre arquivos e sessões). Criar: `m<letra>`. Saltar: `'<letra>` (linha) ou `` `<letra> `` (linha+coluna). Listar: `:marks`.

Veja também: [[10 - Registers, marks, macros]].

### Modal editing
Modelo de edição em que o editor opera em modos distintos (normal, insert, visual, command…); cada modo redefine o significado das teclas. É a base de Vim/Neovim e o que permite tratar edição como uma linguagem de comandos.

Veja também: [[01 - Modal editing]], [[02 - Motions, operadores e text objects]].

### Modo
Um dos estados internos do Neovim que define como as teclas são interpretadas. Os modos principais são: normal (comandos), insert (digitar), visual (selecionar), command-line (`:`), terminal (REPL embutido).

Veja também: [[01 - Modal editing]].

### Motion
Comando que move o cursor em modo normal (ex: `w`, `e`, `gg`, `f<x>`). Em Vim, motions são "substantivos" que combinam com operadores ("verbos") para formar comandos. Ex: `dw` = delete + word.

Veja também: [[02 - Motions, operadores e text objects]].

### Operador
Comando que age sobre um alvo definido por motion ou text object. Operadores principais: `d` (delete), `c` (change), `y` (yank), `v` (visual), `>`/`<` (indent), `gu`/`gU` (case).

Veja também: [[02 - Motions, operadores e text objects]].

### Quickfix list
Lista global de "lugares pra ir" no Neovim (resultados de grep, compile errors, LSP references, TODOs…). Editável em massa via `:cdo <cmd>`. Comandos: `:copen` (abre), `:cnext`/`:cprev` (navega), `:cc N` (item N). Em LazyVim: `]q`/`[q` é keymap default.

Veja também: [[11 - Workflow avançado]].

### Register
"Clipboard" nomeado do Vim. Yank/delete/change escrevem em registers; paste lê. Classes: named (`a`-`z`), numbered (`0`-`9`, histórico), system (`+`/`*`), expression (`=`), search (`/`), command (`:`), black hole (`_`). Listar: `:reg`.

Veja também: [[10 - Registers, marks, macros]].

### Text object
Região textual delimitada semanticamente (palavra, parágrafo, par de delimitadores, tag HTML…). Acessada por prefixos `i` (inner — só o conteúdo) ou `a` (around — inclui delimitadores). Ex: `ci"` muda o conteúdo entre aspas; `da{` deleta o bloco `{ }` inteiro.

Veja também: [[02 - Motions, operadores e text objects]], [[12 - Treesitter avançado]].

### Undotree
Estrutura em árvore (não linear) que o Neovim mantém para desfazer/refazer. Cada `u` volta no tempo; mas se você edita após um undo, cria um novo ramo. Plugin `undotree.nvim` (LazyVim Extra) navega visualmente; comandos `:earlier`/`:later` movem por tempo (`:earlier 5m`).

Veja também: [[03 - Edição e navegação]].

## Ecossistema LazyVim

### AST
Abstract Syntax Tree — árvore sintática abstrata. Representação hierárquica da estrutura de um código por um parser. Em Neovim, fornecida por Treesitter por linguagem; viabiliza highlight preciso, text objects estruturais e navegação por nó.

Veja também: [[12 - Treesitter avançado]].

### Distribuição
Preset de configuração de Neovim que combina um conjunto de plugins, opções e keymaps. Exemplos: LazyVim, LunarVim, AstroNvim, NvChad, kickstart.nvim. Diferente de Neovim "vanilla", onde tudo é configurado do zero.

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### Lazy-loading
Carregar um plugin apenas quando necessário (em evento, comando, filetype ou tecla específica), ao invés de no startup. Reduz tempo de boot. Em lazy.nvim: campos `event`, `cmd`, `ft`, `keys` na plugin spec.

Veja também: [[07 - lazy.nvim]].

### lazy.nvim
Plugin manager moderno do Neovim mantido por Folke Lemaitre. Usa Lua DSL pra spec de plugins. Recursos: lazy-loading nativo, lockfile (`lazy-lock.json`), profiling, UI interativa (`:Lazy`).

Veja também: [[07 - lazy.nvim]].

### LazyVim
Distribuição Neovim opinada mantida por Folke Lemaitre. Bundle inclui Telescope (fuzzy), neo-tree (explorer), which-key, lazy.nvim (plugin manager), LSP stack (mason + nvim-lspconfig + nvim-cmp + conform). Filosofia: "use defaults; customize on top".

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### neo-tree
Plugin de file explorer (árvore de arquivos lateral) que LazyVim usa como default. Atalho `<leader>e`. Suporta operações sobre arquivos (add, delete, rename, copy/paste) por keymaps dentro da árvore.

Veja também: [[04 - LazyVim tour]].

### Plugin manager
Ferramenta que instala, atualiza e carrega plugins do Neovim. Os principais: lazy.nvim (atual, em LazyVim), packer.nvim (legado), vim-plug (legado, Vimscript). LazyVim usa lazy.nvim por default.

Veja também: [[07 - lazy.nvim]], [[04 - LazyVim tour]].

### Plugin spec
Descrição de um plugin em formato tabela Lua, usada pelo lazy.nvim. Campos comuns: URL/source, `opts` (config passada ao setup), `config` (callback de init custom), `event`/`cmd`/`ft`/`keys` (triggers de lazy-load), `dependencies`.

Veja também: [[07 - lazy.nvim]], [[08 - Customizando LazyVim]].

### Query
Pattern em Tree-sitter (sintaxe S-expression em arquivos `.scm`) que casa contra a AST. Usada pra definir highlights, text objects, captures custom. Composta de patterns, captures (`@nome`) e predicates (`#match?`, `#any-of?`).

Veja também: [[12 - Treesitter avançado]].

### Telescope
Plugin de fuzzy finder pra Neovim. Em LazyVim, atalhos principais: `<leader>ff` (find files), `<leader>fg` (live grep), `<leader>,` (buffers), `<leader>fh` (help). Pode mandar resultados pra quickfix com `<C-q>`.

Veja também: [[04 - LazyVim tour]], [[11 - Workflow avançado]].

### Treesitter
Biblioteca de parsing incremental (do GitHub). No Neovim, integrada via `nvim-treesitter` — gera AST por linguagem em tempo real, usada pra highlight preciso, text objects estruturais (`af`, `ic`), navegação por nó. Parsers instaláveis via `:TSInstall <lang>`.

Veja também: [[12 - Treesitter avançado]].

### which-key
Plugin de descoberta de keymaps. Após pressionar uma key prefix (ex: `<leader>`), espera ~1s e mostra popup com os keymaps disponíveis e o que fazem. Atalho `<leader>sk` no LazyVim faz search-keymap.

Veja também: [[04 - LazyVim tour]].

## LSP & dev

### Code action
Operação contextual sugerida pelo LSP — refactoring, fix automático, import, etc. Em LazyVim: `<leader>ca` lista as code actions disponíveis na linha/cursor atual.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Diagnostic
Mensagem de problema (erro, warning, info, hint) emitida por um language server ou linter sobre um arquivo. Em Neovim: rendered como sign no gutter, virtual text inline, underline. Listada via `:lopen` ou Telescope `<leader>xd`.

Veja também: [[09 - LSP no Neovim]].

### Format on save
Comportamento (default no LazyVim) de rodar o formatter (conform.nvim no LazyVim) automaticamente ao salvar (`:w`). Toggle: `<leader>uf`.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Formatter
Ferramenta que reformata código segundo regras (prettier, ruff, gofmt, stylua…). Em LazyVim moderno, dispatcher é conform.nvim. Acionado em `:w` (format on save) ou explicitamente via `<leader>cf`.

Veja também: [[09 - LSP no Neovim]].

### Language server
Processo separado que implementa a Language Server Protocol pra uma linguagem específica (ex: `ts_ls` pra TypeScript, `lua_ls` pra Lua, `rust_analyzer` pra Rust). Editor é cliente; server responde requests sobre o código (hover, definition, refactor).

Veja também: [[09 - LSP no Neovim]].

### Linter
Ferramenta que analisa código por padrões problemáticos sem necessariamente quebrar build (eslint, ruff, shellcheck…). Em LazyVim, dispatcher é nvim-lint. Diagnostics aparecem no mesmo flow do LSP.

Veja também: [[09 - LSP no Neovim]].

### LSP
Language Server Protocol — protocolo cliente/servidor que dá a editores recursos como go-to-definition, hover, completions, diagnostics, formatting. Implementado em Neovim via cliente built-in (`vim.lsp`) e `nvim-lspconfig`. Servers são instalados via Mason.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Mason
Plugin de Neovim que gerencia instalação/atualização de language servers, formatters, linters e DAP adapters. `:Mason` abre TUI. Bundle do LazyVim.

Veja também: [[09 - LSP no Neovim]], [[13 - Snippets e DAP]].

### nvim-cmp
Engine de completion pra Neovim. Aceita múltiplas sources (LSP, buffer, path, snippet). Renderiza popup em insert mode. Bundle do LazyVim.

Veja também: [[09 - LSP no Neovim]].

### nvim-lspconfig
Plugin que provê configs padronizadas pra ~200 language servers em Neovim. Em LazyVim, customização via `opts.servers.<nome> = { settings = {...} }`.

Veja também: [[09 - LSP no Neovim]].

## Avançado

### DAP
Debug Adapter Protocol — protocolo open source (Microsoft) que padroniza comunicação entre editores e debuggers. Em Neovim: `nvim-dap` (cliente) + adapter por linguagem (instalável via Mason). UI: `nvim-dap-ui`.

Veja também: [[13 - Snippets e DAP]].

### init.lua
Arquivo principal de configuração do Neovim moderno (sucessor do `init.vim` em Vimscript). Localização: `~/.config/nvim/init.lua`. No LazyVim, é minimal — apenas faz `require("config.lazy")` que carrega o bootstrap.

Veja também: [[05 - Lua para Neovim]], [[06 - Estrutura de config]].

### Lua
Linguagem de scripting embutida em Neovim (via LuaJIT — Lua 5.1-compatible). Substitui Vimscript pra config moderna. Tipos minimal (nil, boolean, number, string, table, function), 1-indexed em tabelas, truthiness peculiar (`0` é truthy).

Veja também: [[05 - Lua para Neovim]].

### LuaSnip
Snippet engine pra Neovim, escrita em Lua. Suporta snippets em Lua puro (mais expressivo) e em formato VS Code JSON (mais portável, pacotes como `friendly-snippets`). Integra com `nvim-cmp`.

Veja também: [[13 - Snippets e DAP]].

### Snippet
Trecho de código parametrizável que expande a partir de um trigger. Tabstops (`$1`, `$2`, `$0`) permitem navegação ordenada entre campos editáveis. Em Neovim moderno: LuaSnip (engine) + friendly-snippets (catálogo VS Code-style).

Veja também: [[13 - Snippets e DAP]].

## Shell / Zsh / OMZ

### Alias
Atalho que expande pra outra string antes da execução. Zsh tem 3 tipos: regular (`alias gco='git checkout'`), global (`alias -g G='| grep'`, expande em qualquer posição), e suffix (`alias -s md=nvim`, dispara pelo sufixo do arquivo).

Veja também: [[02 - Zsh essencial]].

### Bindkey
Builtin do Zsh que mapeia sequências de tecla a widgets do ZLE. Sintaxe: `bindkey '<seq>' <widget>` (define), `bindkey -r '<seq>'` (remove), `bindkey -M <keymap> ...` (em keymap específico). Aceita modo emacs (`bindkey -e`, default) ou vi (`bindkey -v`).

Veja também: [[06 - Keybindings práticos]], [[07 - ZLE]].

### Builtin
Comando implementado diretamente pelo shell (não é binário externo no `$PATH`). Em Zsh: `setopt`, `bindkey`, `zstyle`, `compinit`, `print`, `read`, `typeset`. Mais rápido que comando externo; semântica integrada ao shell.

Veja também: [[01 - Zsh vs Bash]], [[02 - Zsh essencial]].

### Compdef
Builtin do Zsh (`compdef <function> <command>`) que registra uma função de completion para um comando. Exemplo: `compdef _git mygit` faz `mygit` completar com a lógica de `_git`. Útil pra binários sem completion própria ou aliases.

Veja também: [[08 - Completion system (compsys)]].

### Compinit
Builtin do Zsh que inicializa o completion system. Lê `fpath`, indexa funções `_<comando>`, gera `~/.zcompdump` (cache compilado). Setup canônico: `autoload -Uz compinit && compinit`. Variações: `-i` (ignora arquivos inseguros), `-C` (pula security check, mais rápido).

Veja também: [[08 - Completion system (compsys)]].

### Compsys
Sistema de completion programável do Zsh. Cada comando pode ter função `_<comando>` no `fpath` que define como completar. Inicializado por `compinit`; customizado por `zstyle`; troubleshooting com `compaudit`.

Veja também: [[08 - Completion system (compsys)]].

### Extended glob
Padrões adicionais de globbing do Zsh ativados por `setopt EXTENDED_GLOB`: `^pat` (negação), `~pat` (exclusão), `(p1|p2)` (alternation), `pat#`/`pat##` (zero/um ou mais). Glob qualifiers `(...)` NÃO precisam de `EXTENDED_GLOB` — são feature nativa do globbing do Zsh.

Veja também: [[09 - Globbing avançado e parameter expansion]], [[02 - Zsh essencial]].

### fc
Builtin do Zsh ("fix command") que lista (`fc -l`) ou edita (`fc` puro abre `$EDITOR` com o último comando) entradas do history. `fc <substring>` re-executa o último comando que casa com a substring.

Veja também: [[03 - History do Zsh]].

### Fpath
Array com diretórios onde Zsh procura funções autoload — incluindo funções de completion (`_<comando>`). OMZ adiciona `$ZSH/plugins/*/` e `$ZSH/completions/`. Ordem importa: primeiro no fpath, primeiro encontrado.

Veja também: [[08 - Completion system (compsys)]].

### Function (shell)
Bloco nomeado de comandos executável como se fosse comando. Sintaxe Zsh: `f() { ... }` ou `function f { ... }`. Aceita parâmetros (`$1`, `$@`), variáveis `local`, e `return <código>`. Diferente de alias: tem lógica.

Veja também: [[02 - Zsh essencial]].

### Glob qualifier
Sufixo entre parênteses pós-fixado a um glob, filtra por atributo do arquivo. Exemplos: `(.)` (regular files), `(/)` (dirs), `(N)` (null glob), `(L+N)` (size > N), `(mh-N)` (modificado em N horas), `(om[1,5])` (ordenar por mtime, 5 mais recentes). Feature nativa do globbing — não requer `EXTENDED_GLOB` (que cobre apenas `^`, `~`, `#`, `##`, alternation).

Veja também: [[09 - Globbing avançado e parameter expansion]].

### Globbing
Geração de nomes de arquivo a partir de padrões (`*`, `?`, `[abc]`, `**/`). Zsh tem extensões poderosas (EXTENDED_GLOB) que substituem dezenas de combinações `find`/`grep` por one-liners. Apoiado por glob qualifiers pra filtrar por atributos do arquivo.

Veja também: [[09 - Globbing avançado e parameter expansion]].

### History
Registro persistente de comandos digitados, gravado em `HISTFILE` (default `~/.zsh_history`). Configurado por `HISTSIZE`/`SAVEHIST` + opts (`SHARE_HISTORY`, `EXTENDED_HISTORY`, `HIST_IGNORE_ALL_DUPS`, `HIST_VERIFY`). Acessado via `history`, `Ctrl-R`, `!!`, `!$`, `fc`.

Veja também: [[03 - History do Zsh]].

### Instant prompt
Mecanismo do Powerlevel10k que cacheia o prompt renderizado e o exibe ANTES de `~/.zshrc` terminar de carregar. Acelera startup percebido. Configurado por `POWERLEVEL9K_INSTANT_PROMPT` (`verbose`/`quiet`/`off`). O bloco do instant prompt deve ficar no TOPO do `.zshrc`.

Veja também: [[05 - Powerlevel10k]].

### Nerdfont
Família de fonts patched (Nerd Fonts) com glyphs adicionais — ícones de Git, Linux distros, dev tools, devicons. Powerlevel10k recomenda **MesloLGS NF**. Sem nerdfont configurada no terminal, ícones do prompt aparecem como `□` ou `?`.

Veja também: [[05 - Powerlevel10k]].

### Oh-My-Zsh
Framework de config pra Zsh: clonado em `~/.oh-my-zsh/`, sourced no `.zshrc`, fornece um loader de plugins (`plugins=(...)`) + 300+ plugins embarcados + 150+ temas. Não substitui o Zsh — é overlay. Pasta `custom/` é o terreno do usuário (plugins/themes próprios, overrides).

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]], [[10 - Plugins, themes e custom no OMZ]].

### Parameter expansion
Expansão do valor de variáveis com transformações inline. Sintaxe: `${var:-default}` (default), `${var//pat/repl}` (replace global), `${var##pre}` (remove prefix longo), `${(L)var}` (lowercase), `${(s:.:)var}` (split). Zsh estende a sintaxe de Bash com flags `(L)/(U)/(C)/(s:x:)/(j:x:)/(@)/(P)/(k)/(v)`.

Veja também: [[09 - Globbing avançado e parameter expansion]].

### Plugin (OMZ)
Unidade de funcionalidade para Oh-My-Zsh: pasta com `<nome>.plugin.zsh` em `~/.oh-my-zsh/plugins/<nome>/` (embarcado) ou `~/.oh-my-zsh/custom/plugins/<nome>/` (custom). Carregado adicionando `<nome>` ao array `plugins=(...)` no `.zshrc`. Pode trazer aliases, funções e completion (`_<comando>`).

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]], [[10 - Plugins, themes e custom no OMZ]].

### POSIX
Portable Operating System Interface — padrão IEEE que define APIs e comportamento de shell mínimos. Bash é mais próximo do POSIX por default; Zsh estende livremente mas oferece `emulate sh|bash|ksh` quando precisa de compat.

Veja também: [[01 - Zsh vs Bash]].

### Powerlevel10k
Theme externo pra Zsh por Roman Perepelitsa (romkatv/powerlevel10k). Oferece prompt rico configurável (status git, exit code, tempo de comando), `instant prompt` pra startup rápido, wizard `p10k configure`. Em modo manutenção desde 2024-07 — funcional, mas não evolui ativamente.

Veja também: [[05 - Powerlevel10k]].

### Prompt
Texto exibido pelo shell antes de aceitar comando, configurado pelas variáveis `PROMPT` (left) e `RPROMPT` (right). Suporta sequências de escape (`%n` user, `%~` cwd, `%F{color}` cor). Themes (Powerlevel10k, Starship, Pure) substituem `PROMPT` com lógica rica.

Veja também: [[05 - Powerlevel10k]], [[10 - Plugins, themes e custom no OMZ]].

### Setopt
Builtin do Zsh que ativa/desativa opções do shell. `setopt EXTENDED_GLOB` liga, `unsetopt` desliga, `setopt` sozinho lista as ativas. Opts comuns: `AUTO_CD`, `EXTENDED_GLOB`, `INTERACTIVE_COMMENTS`, `NO_BEEP`, `CORRECT`, `PROMPT_SUBST`, `SHARE_HISTORY`.

Veja também: [[02 - Zsh essencial]], [[03 - History do Zsh]].

### Shell
Interpretador de comandos de um sistema Unix-like. Pode ser interativo (lê `.zshrc`, edita linha) ou não-interativo (script). A família Bourne agrupa sh, ksh, bash e zsh — sintaxe próxima mas extensões e defaults divergem.

Veja também: [[01 - Zsh vs Bash]].

### Theme (custom OMZ)
Theme próprio de Oh-My-Zsh, arquivo `~/.oh-my-zsh/custom/themes/<nome>.zsh-theme`. Define `PROMPT` (left) e `RPROMPT` (right) usando prompt expansion (`%F{...}`, `%K{...}`, `%n`, `%~`, `%#`). Ativado com `ZSH_THEME="<nome>"` no `.zshrc`. Powerlevel10k é theme externo (não-OMZ-customizado) — vive em `~/powerlevel10k/` e é sourced direto.

Veja também: [[10 - Plugins, themes e custom no OMZ]], [[05 - Powerlevel10k]].

### Transient prompt
Recurso do Powerlevel10k que "encolhe" prompts antigos quando você executa novos comandos, liberando espaço visual. Configurado por `POWERLEVEL9K_TRANSIENT_PROMPT` (`same-dir`/`always`/`off`).

Veja também: [[05 - Powerlevel10k]].

### Widget
Função registrada no ZLE (`zle -N <name>`) que pode ser bindada a uma sequência de tecla via `bindkey`. Widgets builtin: `self-insert`, `beginning-of-line`, `backward-kill-word`, `history-incremental-search-backward`. Custom: função Zsh + `zle -N`.

Veja também: [[06 - Keybindings práticos]], [[07 - ZLE]].

### ZLE
Zsh Line Editor — o editor de linha embutido no Zsh, responsável por receber teclas, manter o buffer da linha sendo editada, e dispatchar widgets (ações). Tudo que `bindkey` mapeia é executado pelo ZLE. Hooks: `zle-line-init`, `zle-keymap-select`, `zle-line-finish`.

Veja também: [[06 - Keybindings práticos]], [[07 - ZLE]].

### Zsh-autosuggestions
Plugin (`zsh-users/zsh-autosuggestions`) que sugere comandos enquanto você digita, em cinza inline, baseado no history. Aceitar com `→` (right-arrow) ou `Ctrl-F`. Frequentemente usado junto com history extended + `Ctrl-R`.

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]], [[03 - History do Zsh]].

### Zsh-syntax-highlighting
Plugin (`zsh-users/zsh-syntax-highlighting`) que colore comandos enquanto você digita: verde pra comandos válidos, vermelho pra inválidos, underline pra paths existentes. Cores específicas de aliases e outros elementos variam por tema/config — o highlighter default não distingue aliases de comandos normais com cor separada. Alternativa mais rápida: `fast-syntax-highlighting`. **Regra crítica:** deve ser o último plugin no array `plugins=(...)` — senão perde highlight de comandos adicionados por plugins posteriores.

Veja também: [[04 - Oh-My-Zsh — anatomia e plugins essenciais]].

### Zstyle
Builtin do Zsh que customiza estilos de subsistemas (completion, prompts, vcs_info, etc.). Sintaxe: `zstyle '<context>' '<style>' '<value>'`. No completion: `zstyle ':completion:*' menu select` ativa menu navegável; `matcher-list 'm:{a-z}={A-Za-z}'` ativa case-insensitive.

Veja também: [[08 - Completion system (compsys)]].

## Multiplexer / Zellij

### Attach
Reconectar a uma session Zellij em background. Comando: `zellij attach <nome>` ou `zellij attach --create <nome>` (idempotente — cria se não existir). Múltiplos clients podem anexar à mesma session simultaneamente (input replicado).

Veja também: [[04 - Sessões persistentes — detach, attach, gerenciamento]].

### Detach
Desconectar de uma session Zellij sem matar — server segue rodando, panes seguem executando comandos. Keybinding: `Ctrl-o d` (modo Session + tecla d). Não é destrutivo; reconectar via `zellij attach`.

Veja também: [[04 - Sessões persistentes — detach, attach, gerenciamento]].

### Floating pane
Pane que aparece sobreposto ao grid de outros panes, sem ocupar espaço deles. Pode ser movido e redimensionado livremente. Útil pra terminal extra temporário (e.g. consultar `man` enquanto outro pane roda código).

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### KDL
KDL Document Language — linguagem de configuração declarativa com sintaxe humana (sem aspas obrigatórias na maioria das chaves, comentários nativos, suporte a tipos básicos e children). Usada pela config e pelos layouts do Zellij.

Veja também: [[05 - Layouts declarativos em KDL]].

### Layout (Zellij)
Definição declarativa em KDL de tabs, panes, splits, cwd, comandos de auto-start. Arquivo `.kdl` em `~/.config/zellij/layouts/`. Carregado via `default_layout "<nome>"` no config ou ad-hoc com `zellij --layout <nome>`.

Veja também: [[05 - Layouts declarativos em KDL]].

### Locked mode
Modo do Zellij que desliga todos os keybindings internos — input vai direto pro app no pane ativo. Útil pra Emacs, Helix, apps que usam Ctrl-letra. Atalho default: `Ctrl-g` (entra e sai).

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### Mode (Zellij)
Estado modal do Zellij — controla quais keybindings estão ativas. 9 modos default: normal (input vai pro shell), locked (passthrough), pane, tab, resize, scroll, search, session, move. Entrar via `Ctrl-<letra>`; sair via ESC ou repetir o atalho.

Veja também: [[03 - Modos básicos e keybindings essenciais]].

### Multiplexer
Programa que divide 1 terminal em múltiplas sessions, tabs e panes que sobrevivem a detach (desconexão do emulador). Server roda em background; cliente anexa/desanexa via `attach`/`detach`. Exemplos: Zellij, tmux, screen.

Veja também: [[01 - Zellij vs tmux vs screen]].

### Pane
Divisão interna de uma tab Zellij, rodando um shell ou comando. 3 tipos: split (ocupa grid), floating (sobreposto), stacked (empilhado). Pane ativa recebe input; outras seguem rodando.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### Pipe API
Interface bidirecional Zellij ↔ plugin pra comunicação assíncrona via "pipes" nomeados. Plugin pode emitir (`pipe()`) e receber (`PipeMessage` event); scripts shell externos podem injetar mensagens com `zellij action pipe`.

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### Plugin (Zellij)
Módulo WASM que estende Zellij (status bar, navegador entre Neovim/Zellij, plugins de produtividade, etc.). Sandbox capability-based: plugin declara permissões; user aprova na primeira carga. Lifecycle: `load`/`update`/`render`. Multilang (Rust, Zig, Go, AssemblyScript).

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### Session (Zellij)
Container nomeado de uma instância Zellij. Sobrevive a detach (fechar emulador, SSH drop). Contém N tabs, cada uma com N panes. Criar com `zellij -s <nome>`; listar com `zellij ls`; anexar com `zellij attach <nome>`.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]], [[04 - Sessões persistentes — detach, attach, gerenciamento]].

### Stacked pane
Modo de empilhamento de panes onde 1 é expandido e os outros aparecem só como barra de título (minimizados). Útil pra agrupar múltiplos logs/jobs com apenas 1 em foco.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### Status bar
Barra de informações na borda inferior do Zellij que mostra modo ativo, tabs abertas e atalhos disponíveis. Implementada como plugin (default ativo). Pode ser substituída por plugins custom como zjstatus.

Veja também: [[03 - Modos básicos e keybindings essenciais]], [[06 - Modos avançados, plugins e copy-mode]].

### Tab (Zellij)
Agrupamento horizontal de panes dentro de uma session Zellij. Cada tab tem layout próprio. Mostra nome na barra superior. Diferente de tab do emulador (kitty/wezterm) — tabs Zellij vivem dentro da session.

Veja também: [[02 - Modelo mental — sessions, tabs, panes]].

### Tmux compat mode
Modo de configuração do Zellij (`default_mode "tmux"`) que ativa keybindings tmux-like (prefixo `Ctrl-b`, `c` novo tab, `%` split, etc.). Útil pra migração; tradeoff: perde discoverabilidade dos modos.

Veja também: [[06 - Modos avançados, plugins e copy-mode]].

### WASM
WebAssembly — formato binário portátil e sandboxed pra rodar código compilado em browsers e em runtimes standalone (wasmtime, Wasmer). No contexto do terminal, é a tecnologia que o Zellij usa pra plugins: módulos `.wasm` compilados de Rust/Zig/Go/AssemblyScript, executados num sandbox capability-based. Vantagem: linguagem-agnóstico e seguro por default (sem syscalls não autorizadas).

Veja também: [[Dicionário do Terminal#Plugin (Zellij)]].

## TUIs de Dev / Lazygit / Lazydocker

### Bisect (Lazygit)
UI visual do `git bisect` no Lazygit. Painel Commits, `b` em commit → escolhe Good/Bad. Lazygit faz checkout do commit do meio; você testa; marca; em ~log₂(N) iterações identifica a regressão. "Reset bisect" aborta e retorna ao HEAD original.

Veja também: [[06 - Lazygit — operações avançadas]].

### Cherry-pick
Copiar 1 ou mais commits de uma branch pra outra. No Lazygit: painel Commits, `C` (uppercase) na branch origem → checkout destino → `V` (uppercase) paste. Conflitos tratados como merge conflict normal.

Veja também: [[03 - Lazygit — operações intermediárias]].

### Command log
Painel inferior do Lazygit que exibe cada comando git executado pela TUI. Útil pra aprender que comando shell equivale a uma ação visual e debuggar quando algo não funciona.

Veja também: [[01 - Lazygit — overview e operações essenciais]].

### Custom command (Lazygit)
Atalho YAML no `config.yml` mapeando key → shell command. Schema: `key`, `command`, `context`, `description`, `output`, `prompts`. Placeholders Go template como `{{ .CheckedOutBranch.Name }}`. Viabiliza force-push with lease, conventional commits, fast PR creation, branch creation com prefixo.

Veja também: [[06 - Lazygit — operações avançadas]], [[04 - Lazygit — config e customização]].

### Docker-compose
Orquestrador multi-container Docker. Define services em `docker-compose.yml` (ou `compose.yaml`). Comando: `docker compose up/down/logs/exec`. Lazydocker auto-detecta o arquivo no cwd e agrupa containers como services.

Veja também: [[02 - Lazydocker — overview e operações comuns]], [[07 - Lazydocker — debugging avançado e docker-compose]].

### Editor preset
Preset YAML do Lazygit (`os.editPreset`) que define como abrir arquivos no editor configurado. Built-ins suportados: `nvim`, `vim`, `nvim-remote`, `lvim`, `emacs`, `nano`, `micro`, `vscode`, `sublime`, `bbedit`, `kakoune`, `helix`, `xcode`, `zed`, `acme`. Para editor não listado, usar `os.edit` / `os.editAtLine` com placeholders `{{filename}}` e `{{line}}`.

Veja também: [[04 - Lazygit — config e customização]].

### Exec (Lazydocker)
Abrir shell interativo dentro de container rodando. Default key `E` (executa `/bin/sh`). Pra shell custom (`bash`, `zsh`), usar `customCommands` no config (nota 05) ou flag de imagem.

Veja também: [[02 - Lazydocker — overview e operações comuns]], [[05 - Lazydocker — config, customização e workflow]].

### Hunk
Bloco contíguo de mudanças num diff git — várias linhas próximas marcadas como `+`/`-`. Lazygit permite stage hunk-por-hunk (`enter` em arquivo no painel Files + `space`) ou linha-por-linha (`a` na staging view alterna pra modo linha). Diff tools chamam isso de "chunk" também.

Veja também: [[03 - Lazygit — operações intermediárias]].

### Interactive rebase
`git rebase -i <base>` com UI Lazygit. Painel Commits: `i` (todos os commits da branch) ou `e` em commit específico (a partir daquele commit). Cada commit ganha ação: `s` squash, `f` fixup, `d` drop, `e` edit, `r` reword. Reordenar com `<c-k>`/`<c-j>`. `m` → Continue após marcar as ações.

Veja também: [[03 - Lazygit — operações intermediárias]].

### Lazydocker
TUI Docker em Go por Jesse Duffield. Painéis: Project, Services, Containers, Images, Volumes, Networks; com tabs Logs/Config/Stats por seleção. Auto-detecta `docker-compose.yml` no cwd. Config YAML em `~/.config/lazydocker/config.yml`.

Veja também: [[02 - Lazydocker — overview e operações comuns]], [[05 - Lazydocker — config, customização e workflow]].

### Lazygit
TUI git em Go por Jesse Duffield. Painéis keyboard-first pra status, files, branches, commits, stash. Operações por painel com atalhos contextuais; `?` mostra help. Config YAML em `~/.config/lazygit/config.yml`.

Veja também: [[01 - Lazygit — overview e operações essenciais]], [[04 - Lazygit — config e customização]].

### Reflog
Log de movimentos de HEAD (commits, checkouts, resets, rebases). No Lazygit: aba Reflog no painel Branches (`3`), acessada via `]`/`[`. Útil pra recuperar branch deletada ou desfazer reset acidental. Não cobre changes uncommitted (não há reflog do working tree).

Veja também: [[03 - Lazygit — operações intermediárias]].

### TUI
Terminal User Interface — UI keyboard-first dentro do terminal, com painéis, scroll, cores, mouse opcional. Diferente de CLI (entrada e saída por linha) e GUI (gráfica). Exemplos: Lazygit, Lazydocker, htop, neomutt, ranger.

Veja também: [[01 - Lazygit — overview e operações essenciais]].

### Worktree
Múltiplos working dirs do mesmo repo git, cada um em branch própria. Comando: `git worktree add <path> <branch>`. No Lazygit: `w` em Branches abre opções de worktree pra criar/listar/switch. Útil pra hotfix sem stash do trabalho atual; preferir paths irmãos (`../myproj-hotfix`) aos filhos.

Veja também: [[06 - Lazygit — operações avançadas]].

## Dotfiles

### age
Ferramenta de encryption moderna (2019+) por Filippo Valsorda. Alternativa simples ao GPG, com ssh-key based (`-R ~/.ssh/id_ed25519.pub`) ou X25519 keys próprias (`age1...`). Gerar key: `age-keygen -o ~/.age/key.txt`. Encriptar: `age -e -r <recipient> -o out.age in.txt`. Decriptar: `age --decrypt -i ~/.age/key.txt out.age`.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### Bare repo (dotfiles)
Abordagem minimalista de versionar dotfiles usando só git: `git init --bare $HOME/.dotfiles` cria repo separado; `--work-tree=$HOME` rastreia files no home. Alias `dotfiles='git --git-dir=$HOME/.dotfiles --work-tree=$HOME'` no shell. Vantagens: zero ferramentas extras; portabilidade total. Desvantagens: sem templates, sem secrets, sem cross-OS automático.

Veja também: [[06 - Bare git repo — abordagem minimalista]].

### Bootstrap
Script idempotente que provisiona máquina nova zero-to-ready em 1 comando. Etapas típicas: detectar OS, instalar package manager (Homebrew em macOS), instalar deps (`brew bundle`/`apt`), clonar dotfiles, aplicar (stow/chezmoi/bare). Sempre com `set -euo pipefail` + verificações de estado antes de cada operação destrutiva.

Veja também: [[08 - Bootstrap — máquina nova zero-to-ready]].

### chezmoi
Manager de dotfiles em Go com state machine declarativo. Source em `~/.local/share/chezmoi/`; `chezmoi apply` aplica diff. Features: templates (Go), encryption nativa (age/gpg), scripts (`run_once_`), cross-OS automático. Workflow: `chezmoi edit`, `chezmoi diff`, `chezmoi apply`, `chezmoi update`.

Veja também: [[05 - chezmoi — manager completo com templates]].

### Dotfile
Arquivo de configuração de aplicação cujo nome começa com `.` (oculto no `ls` por default), tipicamente em `$HOME` ou `~/.config/`. Exemplos: `~/.zshrc`, `~/.gitconfig`, `~/.config/nvim/init.lua`. Versionar dotfiles permite setup repetível, sync entre máquinas e history de mudanças.

Veja também: [[01 - Princípios — o que são dotfiles e por que versionar]].

### git-crypt
Ferramenta que encripta transparentemente files no git, marcados em `.gitattributes` (`file filter=git-crypt diff=git-crypt`). GPG-based; usa AES-256 CTR. Comandos: `git-crypt init`, `git-crypt add-gpg-user <email>`, `git-crypt unlock`, `git-crypt export-key`. Integra com workflow git normal — files plaintext localmente, ciphertext no repo.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### Idempotente
Propriedade de operação que produz o mesmo resultado se executada N vezes. Em bootstrap: rodar `bash bootstrap.sh` 2x não quebra (pula etapas já completas). Implementação: `if ! command -v ... >/dev/null; then ...`; ou ferramentas com idempotência nativa (`brew bundle`, chezmoi state machine).

Veja também: [[08 - Bootstrap — máquina nova zero-to-ready]].

### Provisioning
Automação de setup inicial de uma máquina (deps, configs, services). Pode ser single-machine (script bash) ou fleet (Ansible, Salt, Puppet). Pra dev individual no terminal, bootstrap em shell + Brewfile resolve sem overhead de Ansible.

Veja também: [[08 - Bootstrap — máquina nova zero-to-ready]].

### Secret (dotfiles)
Credencial ou informação sensível em arquivos de config: API tokens, SSH/GPG private keys, OAuth refresh tokens, DB credentials. Versionar plaintext = vazar pro histórico git permanentemente. Soluções: encryption (git-crypt, age, sops), ou excluir do repo (`.gitignore`) + setup manual em cada máquina. Regra: commitar plaintext UMA vez = rotação obrigatória.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### sops
Secrets OPerationS (Mozilla, hoje CNCF) — encryption YAML/JSON-aware. Encripta VALORES preservando estrutura (chaves visíveis); permite multi-backend (age, GPG, AWS/GCP/Azure KMS, HashiCorp Vault). Comandos: `sops -e -i file.yaml` (encripta in-place), `sops -d file.yaml` (decripta pra stdout), `sops file.yaml` (editar). Config via `.sops.yaml` no repo.

Veja também: [[07 - Secrets em dotfiles — git-crypt, age, sops]].

### Stow
GNU stow — gerenciador de symlinks declarativos pra dotfiles. Estrutura: 1 pasta por "package" no repo; `stow <pkg>` cria symlinks no home replicando a estrutura. Comandos: `stow` (aplicar), `stow -D` (unstow), `stow -R` (restow), `stow -n` (dry-run), `stow --adopt` (adota file existente do home pro repo). Simples, sem state file, mas sem templates ou cross-OS automático.

Veja também: [[04 - GNU stow — symlinks declarativos]].

### Symlink
Symbolic link — arquivo no filesystem que aponta para outro path (arquivo ou diretório). Criado com `ln -s <alvo> <link>`. Inspecionar: `ls -la` (mostra `link -> alvo`). Editar via symlink edita o arquivo alvo. Remover o symlink não afeta o alvo. Base do funcionamento do stow.

Veja também: [[04 - GNU stow — symlinks declarativos]].

### Template (dotfiles)
Arquivo com placeholders renderizados em apply-time. chezmoi usa Go template syntax — `{{ .chezmoi.os }}`, `{{ .email }}`, `{{ if ... }}`. Permite single source funcionar cross-OS (`if eq .chezmoi.os "darwin"`) ou por hostname/user. Arquivos `.tmpl` no source são processados antes de serem copiados para o target.

Veja também: [[05 - chezmoi — manager completo com templates]].

### Whitelist (.gitignore)
Padrão de `.gitignore` que ignora tudo (`*`) e libera só o explícito (`!arquivo`). Útil em bare repo dotfiles onde o working tree é `$HOME` (com milhares de files que NÃO devem ser tracked). Ordem importa: liberar parent dirs antes de children.

Veja também: [[06 - Bare git repo — abordagem minimalista]].

### WSL
Windows Subsystem for Linux — execução de Linux dentro de Windows via WSL2 (com kernel completo). Filesystem cross-OS: `/mnt/c/` é Windows visto do WSL; `\\wsl$\Ubuntu\` é WSL visto do Windows. I/O entre os dois é lento — trabalhar em `/home/` por padrão. Interop via `cmd.exe`, `powershell.exe`, `clip.exe`.

Veja também: [[03 - Cross-OS — Linux vs macOS vs WSL]].

### XDG Base Directory
Spec freedesktop.org que define paths padronizados pra configs (`$XDG_CONFIG_HOME` → `~/.config/`), dados (`$XDG_DATA_HOME` → `~/.local/share/`), cache (`$XDG_CACHE_HOME` → `~/.cache/`) e state (`$XDG_STATE_HOME` → `~/.local/state/`). Apps modernos respeitam; legados (bash, git, ssh) tipicamente ignoram.

Veja também: [[02 - Anatomia — estrutura típica e XDG Base Directory]].

## CLI Utils

### extended search syntax (fzf)
Linguagem de filtro do fzf que estende fuzzy match com âncoras e operadores: `^prefix` (começa com), `suffix$` (termina com), `'exato` (substring exata sem fuzzy), `!negar` (exclui), `a b` (E lógico), `a | b` (OU lógico). Combina com fuzzy default quando não há modificador.

Veja também: [[01 - fzf — fuzzy finder universal]].

### fuzzy finder
Ferramenta interativa de match aproximado em listas — recebe linhas pelo stdin, mostra TUI com filtro em tempo real, emite seleção no stdout. fzf é o canônico no shell; Telescope é o equivalente integrado ao Neovim. Foco no fluxo: substitui `grep | head | escolher` por seleção visual rápida.

Veja também: [[01 - fzf — fuzzy finder universal]], [[12 - Stack interativo — fzf zoxide atuin]].

### FZF_DEFAULT_OPTS
Env var com flags default aplicadas em toda invocação do fzf (a menos que sobrescritas localmente). Lugar típico pra configurar layout (`--height`, `--layout=reverse`), bordas (`--border`), preview default (`--preview-window`). Aplicar também em `FZF_CTRL_R_OPTS`, `FZF_CTRL_T_OPTS`, `FZF_ALT_C_OPTS` pra customizar por binding.

Veja também: [[01 - fzf — fuzzy finder universal]], [[12 - Stack interativo — fzf zoxide atuin]].

### preview window (fzf)
Painel auxiliar do fzf que renderiza preview do item highlighted (arquivo, branch, processo). Configurado via `--preview '<cmd>'` com substituições `{}` (item inteiro), `{1}` (campo 1), etc. Layout via `--preview-window=right:60%:wrap`. Comum usar `bat --color=always {}` pra arquivos.

Veja também: [[01 - fzf — fuzzy finder universal]], [[03 - bat — cat moderno com syntax highlight]].
