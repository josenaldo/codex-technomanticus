---
title: "Integração com Neovim e shell"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - multiplexer
  - zellij
  - magus
  - integration
  - neovim
aliases:
  - Integração Zellij Neovim
---

# Integração com Neovim e shell

> [!abstract] TL;DR
> Zellij integra com Neovim de duas formas principais: focus events ([[Dicionário do Terminal#Autocmd|autocmds]] `FocusGained`/`FocusLost` disparam ao mudar de pane) e vim-zellij-navigator (`Ctrl-h/j/k/l` navega splits do Neovim e panes do Zellij com a mesma keybinding). Shell integration via `zellij action` permite scripts orquestrarem panes — abrir comando, enviar keys, focar tab por nome. Status bar dinâmico fecha o ciclo: plugin Neovim pode publicar modo e branch pro zjstatus via Pipe API.

---

## O que é / Como funciona

### Focus events

Ao mudar de pane no Zellij, o terminal envia escape sequences de foco padrão (DECSET `1004`) para o processo ativo. O Neovim detecta essas sequences e dispara [[Dicionário do Terminal#Autocmd|autocmds]] nos eventos `FocusGained` e `FocusLost`.

Isso habilita comportamentos automáticos que dependem de "quando o Neovim recebe foco":

```lua
-- ~/.config/nvim/lua/config/autocmds.lua
vim.api.nvim_create_autocmd("FocusGained", {
  desc = "Recarrega buffers ao retornar ao Neovim",
  callback = function()
    vim.cmd("checktime")  -- verifica se arquivos mudaram no disco
  end,
})
```

Com `checktime`, se outro processo modificou um arquivo aberto no Neovim enquanto você estava em outro pane (lazygit, sed, um editor CLI), o Neovim recarrega o buffer automaticamente ao receber o foco de volta — sem precisar rodar `:e` manualmente.

O evento `FocusLost` é o espelho: útil para salvar automaticamente ao sair do Neovim:

```lua
vim.api.nvim_create_autocmd("FocusLost", {
  desc = "Salva todos os buffers modificados ao perder foco",
  callback = function()
    vim.cmd("silent! wall")
  end,
})
```

> [!note] Pré-requisito: terminal que propaga focus events
> Nem todo emulador envia as escape sequences de foco. Terminais modernos que suportam: **kitty**, **WezTerm**, **foot**, **Alacritty** (com config). Terminais antigos (xterm básico, alguns VTEs) podem ignorar silenciosamente. Confirmar com: `printf '\e[?1004h'; echo "focus tracking enabled"` — ao entrar/sair da janela, o terminal deve ecoar `^[[I` (in) e `^[[O` (out).

---

### vim-zellij-navigator

**Repo:** https://github.com/hiasr/vim-zellij-navigator
**Versão atual verificada:** v0.3.0 (julho/2025). Versão mínima do Zellij: v0.42.2.

vim-zellij-navigator é um bridge bidirecional que unifica navegação entre splits do Neovim e panes do Zellij. A lógica é: ao pressionar `Ctrl-h/j/k/l`, o plugin detecta se o cursor está na borda do split do Neovim; se sim, "atravessa" para o pane Zellij vizinho na mesma direção. Funciona nos dois sentidos — do Zellij para o Neovim também.

É o análogo direto do vim-tmux-navigator para quem migra do tmux.

**Arquitetura do bridge:**

- **Lado Zellij:** plugin WASM que intercepta os Ctrl-hjkl em modo normal. Quando recebe a mensagem, move o foco entre panes (ou tabs, com `move_focus_or_tab`).
- **Lado Neovim (versão < 0.2.0):** plugin Lua que integra com smart-splits.nvim, zellij-nav.nvim ou Navigator.nvim (fork dynamotn para suporte a Zellij).
- **Versão 0.2.0+:** o lado Neovim não requer plugin separado — a integração é gerenciada diretamente pelo plugin Zellij via mensagem.

**Instalação no Neovim (versões < 0.2.0, com lazy.nvim):**

```lua
-- ~/.config/nvim/lua/plugins/vim-zellij-navigator.lua
{
  "hiasr/vim-zellij-navigator",
  config = function()
    require("vim-zellij-navigator").setup()
  end,
}
```

Verificar o README atual do repo para a lista de plugins de navegação compatíveis e se a versão instalada ainda requer este lado.

**Instalação no Zellij (plugin WASM via keybinds no config):**

O plugin carrega por URL remota ou arquivo local. Adicionar ao `~/.config/zellij/config.kdl`:

```kdl
keybinds {
    normal {
        bind "Ctrl h" {
            MessagePlugin "https://github.com/hiasr/vim-zellij-navigator/releases/download/0.3.0/vim-zellij-navigator.wasm" {
                name "move_focus_or_tab";
                payload "left";
                move_mod "ctrl";
            };
        }
        bind "Ctrl j" {
            MessagePlugin "https://github.com/hiasr/vim-zellij-navigator/releases/download/0.3.0/vim-zellij-navigator.wasm" {
                name "move_focus_or_tab";
                payload "down";
                move_mod "ctrl";
            };
        }
        bind "Ctrl k" {
            MessagePlugin "https://github.com/hiasr/vim-zellij-navigator/releases/download/0.3.0/vim-zellij-navigator.wasm" {
                name "move_focus_or_tab";
                payload "up";
                move_mod "ctrl";
            };
        }
        bind "Ctrl l" {
            MessagePlugin "https://github.com/hiasr/vim-zellij-navigator/releases/download/0.3.0/vim-zellij-navigator.wasm" {
                name "move_focus_or_tab";
                payload "right";
                move_mod "ctrl";
            };
        }
    }
}
```

> [!important] URL/versão do WASM
> O path `releases/download/0.3.0/...` é a versão verificada em julho/2025. Antes de configurar, confirmar o release mais recente no repo e substituir o número de versão. Plugins baixados ficam em cache no Zellij — atualizar a URL força o re-download.

**Opções de configuração disponíveis:**

| Opção | Default | Descrição |
|---|---|---|
| `move_mod` | `ctrl` | Modificador enviado ao Neovim com o comando de movimento |
| `resize_mod` | `alt` | Modificador para operações de resize |
| `use_arrow_keys` | `false` | Usar setas em vez de hjkl |

---

### Shell integration via `zellij action`

`zellij action` é a sub-CLI que permite controlar uma session Zellij de dentro de scripts ou de outro pane. Funciona com a session atual (inferida do ambiente) sem precisar especificar nome.

**Comandos essenciais:**

```bash
# Abrir novo pane com comando específico
zellij action new-pane --command "htop"

# Focar a próxima pane em ordem
zellij action focus-next-pane

# Focar tab pelo nome
zellij action go-to-tab-name "logs"

# Enviar texto como se fosse digitado (com newline explícito)
zellij action write-chars "npm test"
zellij action write-chars $'\n'

# Enviar tecla especial (raw key event)
zellij action write "10"    # envia o byte decimal 10 (newline)

# Comunicar com plugin via Pipe API
zellij action pipe --plugin zjstatus --name key --value "value"

# Recarregar plugin
zellij action launch-plugin "file:~/.config/zellij/plugins/meuplugin.wasm"
```

> [!note] `write-chars` vs `write`
> `write-chars` aceita string UTF-8 e insere caractere a caractere. `write` aceita bytes decimais separados por vírgula (ex: `zellij action write 10` = newline; `zellij action write 27 91 65` = seta para cima). Para enviar `Enter` de forma legível, use `zellij action write-chars $'\n'` (ANSI-C quoting) ou `zellij action write 10`.

---

### Status bar dinâmico com contexto Neovim

zjstatus (coberto em [[06 - Modos avançados, plugins e copy-mode]]) pode exibir variáveis publicadas via Pipe API. Um plugin Neovim pode usar essa canal para enviar contexto atual — modo, branch git, nome do buffer — para o zjstatus renderizar na status bar do Zellij.

**Exemplo de [[Dicionário do Terminal#Autocmd|autocmd]] que publica o modo atual:**

```lua
-- Publica modo Neovim pro zjstatus ao mudar de modo
vim.api.nvim_create_autocmd("ModeChanged", {
  desc = "Publica modo atual pro zjstatus",
  callback = vim.schedule_wrap(function()
    local mode = vim.api.nvim_get_mode().mode
    vim.defer_fn(function()
      vim.fn.system(
        string.format(
          'zellij action pipe --plugin zjstatus --name nvim_mode --value "%s"',
          mode
        )
      )
    end, 100)  -- debounce 100ms
  end),
})
```

> [!warning] Performance
> Autocmds frequentes (ex: `CursorMoved`) chamando `zellij action pipe` de forma síncrona podem gerar 50-100 chamadas de processo por segundo. Sempre usar `vim.defer_fn` (debounce) e eventos esparsos (`BufEnter`, `ModeChanged`, `FocusGained`) em vez de eventos de cursor.

---

## Na prática

### Workflow "edita-em-outro-pane-e-volta"

O focus event + checktime resolve o problema clássico de buffer desatualizado:

1. Abrir Neovim num pane com `app.js`.
2. Pressionar `Ctrl-p w` para toggle de pane floating — abre um shell limpo.
3. Editar o arquivo via lazygit, sed, ou qualquer ferramenta CLI.
4. Fechar o floating pane (`Ctrl-p w` de novo) ou navegar de volta com `Ctrl-hjkl` (vim-zellij-navigator).
5. O Neovim detecta `FocusGained`, roda `checktime`, e recarrega `app.js` automaticamente — sem mensagem de "arquivo modificado externamente" nem necessidade de `:e`.

Este workflow é especialmente útil com lazygit aberto em floating pane: faz o rebase, volta pro Neovim, os buffers refletem o HEAD atual.

---

### Workflow "dev session script"

Combina o layout declarativo da [[05 - Layouts declarativos em KDL]] com `zellij action` para montar o ambiente de desenvolvimento com um único comando:

```bash
#!/usr/bin/env bash
# dev.sh — abre setup completo do projeto

SESSION="myproj"

# Iniciar Zellij com layout dev e nome de session fixo
zellij --layout dev -s "$SESSION"
```

Com o layout `dev` configurado (editor + shell + watcher em splits pré-definidos), uma chamada a `./dev.sh` reproduz o ambiente completo — útil para onboarding e para voltar ao estado de trabalho após reboot.

Para orquestração mais avançada (abrir comandos em panes específicos após o layout carregar), o script pode usar `zellij action` depois de verificar que a session está ativa:

```bash
#!/usr/bin/env bash
SESSION="myproj"

# Subir a session com layout
zellij --layout dev -s "$SESSION" &

# Aguardar session estar disponível e enviar comandos
sleep 1
zellij action go-to-tab-name "watcher"
zellij action write-chars "npm run watch"
zellij action write-chars $'\n'
```

---

### Workflow "send command pra pane vizinho"

Útil para scripts de CI local ou automação de testes: enviar um comando para outro pane sem sair do contexto atual.

```bash
# Da pane atual, focar a próxima e rodar npm test
zellij action focus-next-pane
zellij action write-chars "npm test"
zellij action write-chars $'\n'
```

Para focar por tab ao invés de pane:

```bash
# Ir para a tab "logs" e enviar tail
zellij action go-to-tab-name "logs"
zellij action write-chars "tail -f app.log"
zellij action write-chars $'\n'
```

> [!tip] Alternativa com Pipe API
> Para scripts que precisam de comunicação mais estruturada (não apenas keystrokes), considerar o Pipe API com um plugin intermediário. O `room` (tab switcher do galho 06) pode suportar comunicação via pipe — porém a sintaxe exata depende da pipe API implementada pelo plugin; verifique o README antes de usar: https://github.com/rvcas/room
>
> ```bash
> # hipotético — sintaxe exata depende da pipe API do plugin room; verifique o README:
> # https://github.com/rvcas/room
> zellij action pipe --plugin room -- focus-tab <nome>
> ```

---

## Armadilhas

### (1) `zellij action` fora de uma session ativa

**Causa:** Comandos `zellij action` inferem a session atual pelo ambiente (`$ZELLIJ_SESSION_NAME`). Rodar de fora do Zellij (em terminal comum, em script de CI, em cron) falha silenciosamente ou com erro "no active session".

**Sintoma:** Script roda sem erros aparentes mas nada acontece no Zellij; ou: `Error: There was a problem serializing or deserializing data to/from zellij`.

**Como detectar:** Rodar `echo $ZELLIJ_SESSION_NAME` no contexto em que o script é executado; se vazio ou indefinido, o ambiente não está dentro de uma session ativa. Confirmar também com `zellij list-sessions`.

**Solução:** Verificar `$ZELLIJ_SESSION_NAME` antes de executar; ou usar `zellij action --session <nome>` para especificar explicitamente (verificar sintaxe na versão instalada com `zellij action --help`).

**Label:** `zellij action`, `session`, `$ZELLIJ_SESSION_NAME`, `CI`

---

### (2) vim-zellij-navigator só navega do lado Zellij — Neovim ignora

**Causa:** O plugin WASM do Zellij foi instalado mas o lado Neovim não foi configurado (para versões < 0.2.0) — ou o plugin de navegação companion (smart-splits.nvim, zellij-nav.nvim, Navigator.nvim) não está instalado no Neovim.

**Sintoma:** `Ctrl-hjkl` no Zellij move entre panes corretamente, mas ao entrar no Neovim, as teclas são enviadas como input em vez de navegar splits.

**Como detectar:** Dentro do Neovim, rodar `:checkhealth vim-zellij-navigator` (se disponível) ou `:map <C-h>` — se o mapeamento não existir ou não chamar o navigator, o lado Lua não está instalado. Verificar também a versão com `:Lazy show vim-zellij-navigator` (se usar lazy.nvim).

**Solução:** Verificar versão do vim-zellij-navigator. Se < 0.2.0: instalar o plugin Lua no Neovim e um dos plugins de navegação compatíveis listados no README. Se >= 0.2.0: o lado Neovim é desnecessário — conferir se o `move_mod` no KDL está correto.

**Label:** `vim-zellij-navigator`, `Neovim`, `split`, `plugin`

---

### (3) Focus events não disparam — `FocusGained` nunca é chamado

**Causa:** O emulador de terminal não envia as escape sequences de focus (`\e[?1004h`/`\e[?1004l`), ou o Zellij não propaga o evento pro processo interno.

**Sintoma:** `checktime` nunca roda ao mudar de pane; buffers ficam desatualizados mesmo com o [[Dicionário do Terminal#Autocmd|autocmd]] de `FocusGained` configurado.

**Como detectar:** Rodar `printf '\e[?1004h'` no terminal e mudar o foco da janela — se o emulador suportar, deve imprimir `^[[I` ao receber foco e `^[[O` ao perder. Dentro do Neovim, adicionar temporariamente `vim.api.nvim_create_autocmd("FocusGained", { callback = function() print("focus!") end })` e verificar se a mensagem aparece ao mudar de pane.

**Solução:** Usar emulador que suporta focus events — kitty, WezTerm, foot ou Alacritty (com `enable_focus_reporting = true` no config). Testar com: `printf '\e[?1004h'` e mudar o foco da janela; o terminal deve imprimir `^[[I` ao receber foco.

**Label:** `focus events`, `FocusGained`, `emulador`, `escape sequence`

---

### (4) `write-chars` com `\n` não envia newline — shell não executa o comando

**Causa:** Em Bash/Zsh, `"\n"` dentro de aspas duplas é literal `\n` (barra + n), não newline. `zellij action write-chars "\n"` envia a string `\n` ao pane.

**Sintoma:** O comando aparece no pane mas não é executado — fica esperando Enter.

**Como detectar:** Observar o pane de destino: se o texto do comando aparece mas o prompt não retorna (shell aguarda Enter), o newline não foi enviado. Confirmar rodando `printf '%s' "$(printf '\n')" | xxd` para ver se o byte `0a` (newline) está presente na string usada.

**Solução:** Usar ANSI-C quoting: `$'\n'` (expande para newline real em Bash e Zsh). Alternativas: `zellij action write 10` (byte decimal de newline) ou `printf '\n' | zellij action write-chars /dev/stdin` (se a versão suportar stdin).

```bash
# Correto
zellij action write-chars $'\n'

# Incorreto — envia literal \n
zellij action write-chars "\n"
```

**Label:** `write-chars`, `newline`, `shell quoting`, `ANSI-C`

---

### (5) Plugin Neovim de status polui performance — 100 chamadas/s ao zjstatus

**Causa:** [[Dicionário do Terminal#Autocmd|Autocmd]] configurado em eventos de alta frequência (`CursorMoved`, `TextChanged`) chama `vim.fn.system("zellij action pipe ...")` de forma síncrona — cada chamada faz um fork de processo.

**Sintoma:** Neovim fica lento ao editar; CPU sobe; digitação tem lag.

**Como detectar:** Rodar `:profile start /tmp/nvim-profile.log | profile func * | profile file *` no Neovim, editar por alguns segundos, rodar `:profile stop`, e analisar o log para ver quais autocmds consomem mais tempo. Alternativamente, monitorar o processo com `top` ou `htop` — picos de CPU durante digitação indicam forks excessivos.

**Solução:** Usar debounce com `vim.defer_fn` (100-500ms) e limitar triggers a eventos esparsos: `BufEnter`, `ModeChanged`, `FocusGained`. Para atualizações de branch git, `BufWritePost` é suficiente (git branch muda menos que o cursor).

```lua
-- Errado: CursorMoved é chamado a cada movimento do cursor
vim.api.nvim_create_autocmd("CursorMoved", {
  callback = function()
    vim.fn.system("zellij action pipe ...")  -- fork por movimento!
  end,
})

-- Correto: ModeChanged + debounce
vim.api.nvim_create_autocmd("ModeChanged", {
  callback = function()
    vim.defer_fn(function()
      vim.fn.system("zellij action pipe ...")
    end, 150)
  end,
})
```

**Label:** `performance`, `debounce`, `vim.defer_fn`, `autocmd`

---

### (6) vim-zellij-navigator carrega config da primeira execução — comportamento inconsistente

**Causa:** O plugin WASM do vim-zellij-navigator carrega as opções de configuração (`move_mod`, `resize_mod`, etc.) do **primeiro** `MessagePlugin` executado na session. Se as 4 direções têm configs diferentes (por exemplo, uma sem `move_mod`), a config da direção pressionada primeiro vira o padrão pra session inteira.

**Sintoma:** Navegação funciona de forma inconsistente — algumas direções aplicam o mod correto, outras não.

**Como detectar:** Comparar os 4 blocos `MessagePlugin` no `config.kdl` lado a lado; se algum tiver opções diferentes dos demais (campo ausente, valor diferente), esse é o problema. Testar: pressionar cada direção sequencialmente numa session nova e observar se o comportamento muda dependendo de qual foi a primeira usada.

**Solução:** Manter as opções de configuração idênticas nos 4 binds (`h`, `j`, `k`, `l`). O README do plugin indica explicitamente que "the plugin loads with the configuration of the first executed command".

**Label:** `vim-zellij-navigator`, `config`, `MessagePlugin`, `WASM`

---

## Em inglês

- **focus event** — *focus event*. "terminal event emitted when a pane gains or loses focus; triggers `FocusGained`/`FocusLost` autocmds in Neovim."
- **navigator** — *navigator*. "plugin that bridges split navigation between Neovim windows and Zellij panes using a shared keybinding."
- **bridge** — *bridge*. "two-way integration layer connecting Neovim and Zellij so navigation commands work transparently across both."
- **orchestrate** — *orquestrar*. "to control multiple panes or tabs from a script using `zellij action` subcommands."
- **send keys** — *send keys / enviar teclas*. "`zellij action write-chars` sends keystrokes to the currently focused pane as if typed by the user."
- **pipe** — *pipe*. "named communication channel between Zellij and plugins; used to push data (e.g., Neovim mode) to zjstatus via `zellij action pipe`."
- **autocmd** — *autocmd*. "Neovim autocommand that executes a callback when a specific event (e.g., `FocusGained`, `ModeChanged`) fires."
- **split** — *split*. "a subdivision of a Neovim window; vim-zellij-navigator detects split edges to decide whether to navigate within Neovim or cross into a Zellij pane."
- **pane** — *pane*. "terminal region managed by Zellij; analogous to a tmux pane; can hold any process (shell, Neovim, htop)."
- **escape sequence** — *sequência de escape*. "special byte sequence sent by the terminal to the running process; focus tracking uses `\e[?1004h` to enable and `\e[I`/`\e[O` to signal focus in/out."

---

## Veja também

- [[06 - Modos avançados, plugins e copy-mode]] — Pipe API e arquitetura de plugins WASM
- [[05 - Layouts declarativos em KDL]] — onde o plugin Zellij é declarado no layout
- [[03-Dominios/Terminal/Editor/index|Editor (Neovim)]] — galho 1: tudo sobre Neovim, LSP, autocmds e estrutura de config
- [[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Autocmd|autocmd]], [[Dicionário do Terminal#Plugin (Zellij)|plugin]], [[Dicionário do Terminal#Pipe API|pipe API]]

---

## Referências

- [vim-zellij-navigator](https://github.com/hiasr/vim-zellij-navigator) — bridge Neovim ↔ Zellij (ativo, v0.3.0, jul/2025)
- [Zellij — CLI / Actions](https://zellij.dev/documentation/cli) — referência completa de `zellij action`
