---
title: "Modos avançados, plugins e copy-mode"
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
  - plugins
  - wasm
aliases:
  - Plugins Zellij
  - Tmux compat
---

# Modos avançados, plugins e copy-mode

> [!abstract] TL;DR
> Locked mode passa keys pro app (Emacs/Helix): `Ctrl-g` entra e sai, status bar mostra "LOCKED". Scroll + search mode = `Ctrl-s` + navegação tipo vim no scrollback; `s` dentro do scroll entra em search com regex. Tmux compat mode (`default_mode "tmux"` no config) ativa prefixo `Ctrl-b` tmux-like — útil pra migração, tradeoff: perde discoverabilidade dos modos. Plugins Zellij são WASM (sandbox capability-based, qualquer linguagem que compila pra WASM); arquitetura: lifecycle `load`/`update`/`render` + Pipe API + permissões por capability. Plugins verificados e ativos: zjstatus (status bar customizável, último release abr/2026), vim-zellij-navigator (bridge Neovim ↔ Zellij, último release jul/2025), room (tab switcher fuzzy, último release jan/2026).

---

## O que é / Como funciona

### Locked mode

Locked mode desliga **todos** os keybindings do Zellij — cada tecla pressionada vai diretamente ao app no pane ativo, sem interceptação.

**Atalho:** `Ctrl-g` entra e sai (toggle). A status bar exibe "LOCKED" enquanto o modo está ativo.

**Quando usar:**
- **Emacs** — usa `Ctrl-x`, `Ctrl-c`, `Ctrl-g` e outros chords Ctrl que o Zellij interceptaria.
- **Helix** — usa `Ctrl-w` (que entra no modo Window do Helix) e outros prefixos de modo.
- **Apps com conflito de Ctrl-letra** — qualquer TUI que precisa de Ctrl-letras não capturadas pelo Zellij em modo normal.

> [!note] Locked mode vs normal mode
> Em modo normal, o Zellij captura `Ctrl-p`, `Ctrl-t`, `Ctrl-s`, etc. Locked mode garante passthrough total — o pane ativo recebe 100% das teclas. Para apps que precisam de apenas alguns atalhos, é mais cirúrgico remapear os conflitos no config do Zellij; locked mode é o "modo de emergência" pra apps complexos.

---

### Scroll mode + search mode

**Scroll mode** (`Ctrl-s`) para o output e permite navegar o scrollback buffer com teclas tipo vim:

| Tecla (dentro de Scroll) | Ação |
|---|---|
| `↑` / `↓` | Linha acima / abaixo |
| `PgUp` / `PgDn` | Página acima / abaixo |
| `u` | HalfPageUp (meia tela acima) |
| `d` | HalfPageDown (meia tela abaixo) |
| `g` | Ir para o início do scrollback |
| `G` | Ir para o final (output mais recente) |
| `ESC` ou `Ctrl-s` | Sair do scroll mode |

**Search mode** — dentro de Scroll, pressionar `s` entra em Search:

- O cursor muda pra uma barra de busca na borda do pane.
- Digite o padrão (suporta regex). Enter executa a busca.
- `n` vai para a próxima ocorrência; `N` vai para a anterior.
- `ESC` sai do search e volta ao scroll.
- Regex é case-sensitive por default — use `(?i)` pra case-insensitive (ex: `(?i)error`).

**Copy-mode:**

Dentro de scroll/search, você pode selecionar texto:
- **Mouse:** clicar e arrastar seleciona texto e copia para o clipboard (mouse mode ativo por default).
- **ESC** sai do scroll/search sem copiar.

> [!tip] Scrollback e histórico de shell
> O scrollback do Zellij é independente do histórico do shell. `Ctrl-r` busca no histórico de comandos; Scroll mode (`Ctrl-s` + `s`) busca no output visual do terminal — útil pra encontrar um erro que rolou na tela sem precisar redirecionar pra arquivo.

---

### Tmux compat mode

Zellij oferece um modo de compatibilidade com keybindings do tmux. Para ativar:

```kdl
// ~/.config/zellij/config.kdl
default_mode "tmux"
```

Com `default_mode "tmux"`, o Zellij usa `Ctrl-b` como prefixo (igual ao tmux). Após pressionar `Ctrl-b`:

| Tecla | Ação |
|---|---|
| `c` | Nova tab |
| `n` | Próxima tab |
| `p` | Tab anterior |
| `%` | Split vertical |
| `"` | Split horizontal |
| `d` | Detach da session |
| `z` | Toggle zoom do pane |
| `[` | Entrar em scroll mode |
| `x` | Fechar pane |

**Tradeoffs:**

| | Tmux compat mode | Modo padrão Zellij |
|---|---|---|
| Muscle memory tmux | Funciona imediatamente | Reaprender |
| Discoverabilidade | Status bar menos útil | Status bar exibe tudo |
| Idiomático | Menos (imita outro tool) | Nativo Zellij |
| Plugins que assumem modos | Podem quebrar | Funcionam normalmente |

> [!warning] Recomendação
> Use tmux compat mode **apenas** se você está migrando de tmux e precisa de produtividade imediata sem aprender os modos. Para novos usuários ou quem já passou o onboarding, os modos nativos do Zellij são mais ergonômicos e a discoverabilidade da status bar é uma vantagem real.

---

### Arquitetura de plugins WASM

Zellij usa WebAssembly (WASM/WASI) como runtime de plugins. Essa escolha tem consequências arquiteturais relevantes.

**Por que WASM:**

- **Sandbox:** plugins não acessam filesystem, network ou processos arbitrariamente — cada capability é declarada e aprovada pelo usuário.
- **Multilanguagem:** qualquer linguagem que compila pra WASM pode ser usada. Rust é a única com suporte oficial completo; Go, Zig e AssemblyScript têm suporte via esforços comunitários.
- **Hot reload:** plugins podem ser recarregados sem reiniciar o Zellij (`zellij action launch-plugin`).
- **Isolamento:** um plugin com bug não trava o Zellij — é um processo WASM separado.

**Lifecycle (callbacks que o plugin implementa):**

```
┌─────────────────────────────────────────────────────────┐
│                  Lifecycle do Plugin                    │
├─────────────────────────────────────────────────────────┤
│  load(config)         │ Inicialização; recebe config    │
│                       │ declarada no layout/manifest    │
├─────────────────────────────────────────────────────────┤
│  update(event) → bool │ Chamado em eventos do Zellij    │
│                       │ (mode change, pane change,      │
│                       │ tab update, PipeMessage, etc.)  │
│                       │ Retorna true = renderizar       │
├─────────────────────────────────────────────────────────┤
│  render(rows, cols)   │ Desenha a UI do plugin no       │
│                       │ espaço do pane (rows × cols)    │
└─────────────────────────────────────────────────────────┘
```

**Pipe API:**

A Pipe API é a interface de comunicação bidirecional entre Zellij e plugins (e entre plugins entre si):

- Plugin emite mensagem: chamada `pipe()` dentro do plugin.
- Plugin recebe mensagem: evento `PipeMessage` no callback `update`.
- Script shell envia mensagem pra plugin: `zellij action pipe --plugin <nome> --name <key> --value <val>`.
- Útil pra: plugins que reagem a eventos externos (deploy concluído, testes passaram), automação via shell scripts.

**Permissões capability-based:**

Cada plugin declara as permissões de que precisa. Na primeira carga, o Zellij exibe um prompt interativo para o usuário aprovar ou negar cada capability:

| Capability | O que permite |
|---|---|
| `ReadApplicationState` | Ler estado de panes, tabs, session |
| `ChangeApplicationState` | Modificar layout, fechar panes, trocar tabs |
| `OpenFiles` | Abrir arquivos no editor |
| `WriteToStdin` | Escrever no stdin de outro pane |
| `RunCommands` | Executar comandos no sistema |
| `OpenTerminalsOrPlugins` | Abrir novos panes/plugins |

> [!note] Aprovação persistente
> Após aprovação inicial, as permissões ficam cacheadas. Ao atualizar um plugin (novo `.wasm`), o Zellij pode pedir aprovação novamente se as capabilities mudaram.

---

## Na prática

### Carregar plugin externo

```bash
# Criar pasta de plugins (se não existir)
mkdir -p ~/.config/zellij/plugins

# Download do plugin (exemplo com zjstatus)
curl -L -o ~/.config/zellij/plugins/zjstatus.wasm \
  https://github.com/dj95/zjstatus/releases/latest/download/zjstatus.wasm
```

Referência no layout (`~/.config/zellij/layouts/custom-status.kdl`):

```kdl
layout {
    pane size=1 borderless=true {
        plugin location="file:~/.config/zellij/plugins/zjstatus.wasm"
    }
    pane
}
```

O campo `location` aceita:
- `file:<path>` — plugin local (arquivo `.wasm`).
- `https://<url>` — plugin remoto (baixado na primeira carga, cacheado).
- `zellij:<nome>` — plugin built-in do Zellij (ex: `zellij:status-bar`).

---

### Plugin 1 — zjstatus

**Repo:** https://github.com/dj95/zjstatus
**Status:** ativo — último release v0.23.0 em abril/2026. 970 stars.

zjstatus é um substituto customizável para a status bar built-in do Zellij. Em vez de uma barra fixa, zjstatus expõe módulos configuráveis por layout:

**Módulos disponíveis:** `mode` (modo atual), `tabs` (lista de tabs), `datetime` (data/hora), `command` (output de comando shell), `session` (nome da session), `swap_layout` (layout de swap ativo), `pipe` (mensagens recebidas via Pipe API), `notifications`.

**Configuração inline no layout:**

```kdl
layout {
    pane size=1 borderless=true {
        plugin location="file:~/.config/zellij/plugins/zjstatus.wasm" {
            // Formato dos módulos na barra (esquerda → direita)
            format_left  "{mode} #[fg=#89b4fa,bold]{session}"
            format_right "{datetime}"
            format_space "#[bg=#1e1e2e]"

            // Módulo datetime
            datetime          "#[fg=#cdd6f4] {format} "
            datetime_format   "%d/%m %H:%M"
            datetime_timezone "America/Sao_Paulo"

            // Cores dos modos
            mode_normal  "#[bg=#a6e3a1,fg=#1e1e2e,bold] NORMAL "
            mode_locked  "#[bg=#f38ba8,fg=#1e1e2e,bold] LOCKED "
            mode_pane    "#[bg=#cba6f7,fg=#1e1e2e,bold] PANE "
            mode_tab     "#[bg=#89dceb,fg=#1e1e2e,bold] TAB "
            mode_scroll  "#[bg=#f9e2af,fg=#1e1e2e,bold] SCROLL "
        }
    }
    pane
}
```

O zjstatus também inclui **zjframes**: plugin companion que oculta bordas de panes baseado em condições (ex: single pane ativo).

---

### Plugin 2 — vim-zellij-navigator

**Repo:** https://github.com/hiasr/vim-zellij-navigator
**Status:** ativo — último release v0.3.0 em julho/2025. 172 stars.

vim-zellij-navigator é um plugin que unifica navegação entre splits do Neovim e panes do Zellij. Com ele, `Ctrl-h/j/k/l` funciona de forma transparente: se o foco está no Neovim, navega entre windows do Neovim; se está num pane terminal, navega entre panes do Zellij.

Esta nota cobre o plugin brevemente como exemplo de integração WASM. A [[07 - Integração com Neovim e shell]] tem cobertura completa: configuração do lado Neovim (smart-splits.nvim, zellij-nav.nvim), configuração do lado Zellij, keybindings, edge cases.

---

### Plugin 3 — room

**Repo:** https://github.com/rvcas/room
**Status:** ativo — último release v1.2.1 em janeiro/2026. 278 stars.

room é um plugin de tab switching fuzzy — um fuzzy finder para as tabs da session atual, exibido como pane floating:

- Abrir room: bind customizado (ex: `Ctrl-f` em modo normal, ou via layout).
- Digitar filtra tabs pelo nome (case-insensitive configurável).
- `Tab` / `↑` / `↓` navega pelos resultados.
- `Enter` salta para a tab selecionada.
- Suporta pipe commands: `zellij action pipe --plugin room -- focus-tab <nome>` para automação.

**Download e configuração:**

```bash
curl -L -o ~/.config/zellij/plugins/room.wasm \
  https://github.com/rvcas/room/releases/latest/download/room.wasm
```

```kdl
// ~/.config/zellij/config.kdl — bind pra abrir room
keybinds {
    normal {
        bind "Ctrl f" {
            LaunchPlugin "file:~/.config/zellij/plugins/room.wasm" {
                floating true
            }
        }
    }
}
```

---

### Debugar plugin

**Recarregar plugin sem reiniciar o Zellij:**

```bash
zellij action launch-plugin "file:~/.config/zellij/plugins/meuplugin.wasm"
```

**Inspecionar logs do Zellij:**

```bash
# Listar sessions ativas e encontrar o nome da session atual
zellij ls

# Tail dos logs (substituir <session> pelo nome real)
tail -f ~/.cache/zellij/<session>/zellij-log/zellij.log
```

**Enviar mensagem pra plugin via Pipe API (para testes):**

```bash
zellij action pipe --plugin zjstatus --name test --value "hello"
```

**Verificar versão WASM do plugin vs Zellij:**

Plugins compilados pra uma versão de API do Zellij podem falhar silenciosamente em versões diferentes. Se um plugin para de funcionar após upgrade:

```bash
# Verificar versão do Zellij
zellij --version

# Baixar o release do plugin compilado para essa versão
# (verificar README do plugin — muitos listam compatibility matrix)
```

---

## Armadilhas

### (1) Locked mode + `Ctrl-g` colide com Emacs

**Causa:** O `Ctrl-g` é o atalho padrão do Zellij para entrar/sair do locked mode. Mas dentro do Emacs (que você abriu justamente pra usar com locked mode), `Ctrl-g` é "abort" — cancela o comando atual. O conflito ocorre na **saída** do locked mode: você pressiona `Ctrl-g` pra sair, mas se o foco está no Emacs, o Emacs intercepta primeiro.

**Sintoma:** `Ctrl-g` dentro do Emacs com locked mode ativo aborta a operação do Emacs em vez de sair do modo.

**Como detectar:** Tente pressionar `Ctrl-g` dentro do Emacs com locked mode ativo — se o Emacs "aborta" algo, o conflito está ocorrendo.

**Solução:** Remapear o unlock key pra algo que Emacs não usa, como `Ctrl-\` ou `Alt-g`:
```kdl
// ~/.config/zellij/config.kdl
keybinds {
    locked {
        bind "Ctrl \\" { SwitchToMode "Normal"; }
    }
}
```

---

### (2) Tmux compat mode + plugins que assumem modos nativos

**Causa:** Plugins que se integram com modos do Zellij (ex: zjstatus exibindo o nome do modo atual) esperam modos como `Normal`, `Pane`, `Tab`, etc. Com `default_mode "tmux"`, o modo base é `Tmux` e a transição para sub-modos funciona de forma diferente — plugins que assumem os modos canônicos podem exibir estado incorreto ou não disparar as ações esperadas.

**Sintoma:** zjstatus exibe o modo errado, ou plugin de navegação não funciona corretamente.

**Como detectar:** Ativar tmux compat mode e observar o comportamento dos plugins instalados.

**Solução:** Escolher entre tmux compat mode e plugins que dependem dos modos nativos — os dois não coexistem perfeitamente. Se usar zjstatus, preferir o modo padrão do Zellij.

---

### (3) Plugin com permissão negada — sem mensagem clara

**Causa:** Na primeira carga de um plugin, o Zellij exibe um prompt interativo pedindo aprovação de capabilities. Se o terminal não está em foco, o prompt pode passar despercebido. Se você negar (ou não responder), o plugin carrega mas sem as permissões necessárias — e pode falhar silenciosamente.

**Sintoma:** Plugin abre mas não funciona (não exibe dados, não reage a eventos, não executa ações). Sem mensagem de erro óbvia na tela.

**Como detectar:** Verificar os logs do Zellij:
```bash
tail -f ~/.cache/zellij/<session>/zellij-log/zellij.log
```
Buscar por `permission denied` ou o nome do plugin.

**Solução:** Abrir o plugin novamente (`zellij action launch-plugin "file:..."`) — o prompt de permissão reaparece. Aprovar todas as capabilities necessárias. Como alternativa, é possível pré-declarar permissões no layout (verificar docs da versão atual).

---

### (4) Versão WASM incompatível após upgrade do Zellij

**Causa:** A API de plugins do Zellij muda entre versões. Um plugin compilado pra Zellij 0.40 pode não funcionar em 0.44 — a interface WASM mudou, e o plugin chama funções que não existem mais ou têm assinaturas diferentes. O erro pode ser um panic silencioso no runtime WASM.

**Sintoma:** Plugin que funcionava para de abrir, ou abre mas não renderiza nada. Log mostra erro de WASM/WASI.

**Como detectar:**
```bash
tail -f ~/.cache/zellij/<session>/zellij-log/zellij.log
# Buscar: "wasm", "plugin error", "trap", "unreachable"
```

**Solução:** Baixar o release mais recente do plugin (compilado pra versão atual do Zellij). Plugins bem mantidos (zjstatus, room, vim-zellij-navigator) lançam novos binários junto com releases do Zellij.

---

### (5) Search regex case-sensitive por default

**Causa:** O search mode do Zellij (dentro de Scroll) usa regex case-sensitive por default. Buscar `error` não acha `Error` ou `ERROR`.

**Sintoma:** Busca retorna "não encontrado" para termos que você sabe que estão na saída.

**Como detectar:** Buscar `Error` e não achar nada; buscar `error` e achar — ou vice-versa.

**Solução:** Usar o modificador `(?i)` no início do regex para torná-lo case-insensitive:
```
(?i)error         # casa Error, ERROR, error, eRrOr
(?i)connection    # casa Connection, CONNECTION, etc.
```

---

### (6) Plugin remoto travado em cache de versão antiga

**Causa:** Quando você usa `location="https://..."` no layout, o Zellij faz download do plugin uma vez e cacheia o binário. Se o plugin lança uma nova versão mas o cache não é invalidado, você continua usando a versão antiga — mesmo após remover e recriar a session.

**Sintoma:** Bug corrigido na nova versão do plugin ainda ocorre; `zellij --version` confirma versão nova, mas o plugin está desatualizado.

**Como detectar:** Verificar o cache de plugins:
```bash
ls ~/.cache/zellij/
```

**Solução:** Apagar o cache do plugin específico e deixar o Zellij baixar novamente, ou usar `location="file:..."` com plugin local (mais controle sobre versão).

---

## Em inglês

- **plugin** — *plugin*. "módulo externo que estende o comportamento do Zellij via interface WASM padronizada."
- **WASM** — *WebAssembly (WASM)*. "formato binário portável e sandboxado que permite rodar código compilado de múltiplas linguagens no runtime do Zellij."
- **sandbox** — *sandbox*. "ambiente de execução isolado onde o plugin só pode acessar recursos explicitamente autorizados por capability."
- **hot reload** — *hot reload*. "recarregar um plugin sem reiniciar o Zellij; as mudanças no `.wasm` entram em vigor imediatamente."
- **capability** — *capability*. "permissão granular que o plugin declara e o usuário aprova na primeira carga; ex: `ReadApplicationState`, `WriteToStdin`."
- **permission** — *permission*. "sinônimo de capability no contexto Zellij; controla o que o plugin pode fazer no sistema e na session."
- **lifecycle** — *lifecycle*. "sequência de callbacks (`load`, `update`, `render`) que definem como o plugin é inicializado, reage a eventos e desenha sua UI."
- **pipe** — *pipe*. "canal de comunicação nomeado entre Zellij e plugins (ou entre plugins); dados fluem via eventos `PipeMessage` e chamadas `pipe()`."
- **event** — *event*. "notificação emitida pelo Zellij pra um plugin (ex: mudança de modo, tab atualizada, `PipeMessage`); recebida no callback `update(event)`."
- **render** — *render*. "callback chamado pelo Zellij quando o plugin precisa redesenhar sua UI; recebe dimensões `(rows, cols)` do pane."

---

## Veja também

- [[03 - Modos básicos e keybindings essenciais]] — modos base (locked, scroll, search introduzidos lá)
- [[05 - Layouts declarativos em KDL]] — onde plugin é referenciado em layout KDL
- [[07 - Integração com Neovim e shell]] — vim-zellij-navigator em profundidade
- [[03-Dominios/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Plugin (Zellij)|plugin]], [[Dicionário do Terminal#Pipe API|pipe API]], [[Dicionário do Terminal#Locked mode|locked mode]], [[Dicionário do Terminal#Tmux compat mode|tmux compat]]

---

## Referências

- [Zellij — Plugins](https://zellij.dev/documentation/plugins)
- [awesome-zellij](https://github.com/zellij-org/awesome-zellij)
- [zjstatus](https://github.com/dj95/zjstatus) — status bar customizável (ativo, último release abr/2026)
- [vim-zellij-navigator](https://github.com/hiasr/vim-zellij-navigator) — bridge Neovim ↔ Zellij (ativo, último release jul/2025)
- [room](https://github.com/rvcas/room) — tab switcher fuzzy (ativo, último release jan/2026)
