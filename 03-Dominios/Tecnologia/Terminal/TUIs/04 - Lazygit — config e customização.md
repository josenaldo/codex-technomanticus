---
title: "Lazygit — config e customização"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - tuis
  - lazygit
  - adepto
  - config
aliases:
  - Lazygit config
---

# Lazygit — config e customização

> [!abstract] TL;DR
> Lazygit lê `~/.config/lazygit/config.yml` (YAML). Seções principais: `gui` (theme, scrollOff), `git` (paging, log args), `os` (editPreset), `keybinding` (rebind raro), `customCommands` (intro — profundo em nota 06). Theme custom usa cores hex ou nome; `editPreset: "nvim"` integra com Neovim; mouse, ícones e statusBar tudo configurável. Versionar config nos dotfiles = setup repetível.

## O que é / Como funciona

### Local e formato

- **Path:** `~/.config/lazygit/config.yml` — respeita `$XDG_CONFIG_HOME` se definido
- **Formato:** YAML; comentários com `#`
- **Sem arquivo:** Lazygit aplica defaults internos — nenhuma config é obrigatória
- **Reload:** Lazygit lê config na startup; alterações requerem restart (`q` + `lazygit`)

### Seções principais

#### `gui:`

Controla aparência e comportamento da interface.

Propriedades mais usadas:

- `theme:` — mapa de cores dos elementos visuais (ver seção Theme)
- `showFileTree: true` *(default: true)* — tree view vs flat list no painel Files
- `scrollOffMargin: 2` *(default: 2)* — linhas de buffer visíveis ao scroll (context lines)
- `mouseEvents: true` *(default: true)* — habilita clique do mouse
- `nerdFontsVersion: "3"` *(default: "")* — `"2"`, `"3"` ou vazio (sem ícones)
- `showFileIcons: true` *(default: true)* — ícones de arquivo (requer nerdFont)
- `language: "en"` *(default: auto)* — `"en"`, `"zh-CN"`, `"zh-TW"`, `"pl"`, `"nl"`, `"ja"`, `"ko"`, `"ru"`, `"pt"`
- `border: "rounded"` *(default: rounded)* — estilo de borda: `"rounded"`, `"single"`, `"double"`, `"hidden"`, `"bold"`
- `filterMode: "substring"` *(default: substring)* — modo de filtro: `"substring"` ou `"fuzzy"`

Exemplo:

```yaml
gui:
  theme:
    activeBorderColor:
      - "#74c7ec"
      - bold
    inactiveBorderColor:
      - "#7f849c"
  showFileTree: true
  showFileIcons: true
  mouseEvents: true
  nerdFontsVersion: "3"
```

#### `git:`

Controla como Lazygit interage com o git subjacente.

Propriedades mais usadas:

- `paging.colorArg: "always"` *(default: "always")* — passa `--color=always` pro git pager
- `paging.useConfig: false` *(default: false)* — se `true`, usa `core.pager` do `git config`
- `log.order: "topo-order"` *(default: "topo-order")* — ordem de commits: `"date-order"`, `"author-date-order"`, `"topo-order"`, `"default"`
- `log.showGraph: "when-maximised"` *(default: "when-maximised")* — exibir graph ASCII: `"always"`, `"never"`, `"when-maximised"`
- `log.showWholeGraph: false` *(default: false)* — exibir `--all` no log (slow em repos grandes)
- `pull.rebase: false` *(default: false)* — usar `--rebase` no pull por default
- `branchLogCmd: ""` *(default: "")* — comando custom pra branch log (substitui o built-in)
- `autoFetch: true` *(default: true)* — auto-fetch em background
- `skipHookPrefix: "WIP"` *(default: "WIP")* — commits com esse prefixo pulam hooks

Exemplo:

```yaml
git:
  paging:
    colorArg: "always"
    useConfig: false
  log:
    order: "topo-order"
    showGraph: "when-maximised"
    showWholeGraph: false
  pull:
    rebase: true
```

#### `os:`

Controla como Lazygit abre arquivos em editores e links no sistema.

Propriedades:

- `editPreset:` — preset built-in de editor; valores aceitos: `"vim"`, `"nvim"`, `"nvim-remote"`, `"lvim"`, `"emacs"`, `"nano"`, `"micro"`, `"vscode"`, `"sublime"`, `"bbedit"`, `"kakoune"`, `"helix"`, `"xcode"`, `"zed"`, `"acme"`
- `edit: ""` — comando custom pra abrir arquivo; placeholder `{{filename}}`
- `editAtLine: ""` — comando custom abrindo na linha específica; placeholders `{{filename}}` e `{{line}}`
- `editAtLineAndWait: ""` — igual ao anterior, mas Lazygit bloqueia até o editor fechar
- `editInTerminal: false` *(default: false)* — se `true`, Lazygit suspende e cede o terminal ao editor
- `open: ""` — comando pra abrir arquivo no app default; placeholder `{{filename}}`
- `openLink: ""` — comando pra abrir URL; placeholder `{{link}}`

Quando `editPreset` está definido, os campos `edit`/`editAtLine` são ignorados (o preset define os comandos). Para override completo, omitir `editPreset` e usar `edit`/`editAtLine` diretamente.

Exemplo:

```yaml
os:
  editPreset: "nvim"
  # Alternativa manual (editPreset deve estar vazio ou ausente):
  # edit: "nvim {{filename}}"
  # editAtLine: "nvim +{{line}} {{filename}}"
```

#### `keybinding:`

Permite rebindar ações — uso raro; a maioria dos usuários não precisa mexer.

Estrutura hierárquica por contexto: `keybinding.<context>.<action>: <key>`.

Contextos: `universal`, `status`, `files`, `branches`, `commits`, `stash`, `main`, `submodules`, `worktrees`.

Para desativar um keybinding: `<disabled>`.

Exemplo mínimo:

```yaml
keybinding:
  universal:
    quit: "q"
  commits:
    moveDownCommit: "<c-j>"
    moveUpCommit: "<c-k>"
```

#### `customCommands:` (intro)

Lista de comandos shell customizados mapeados a atalhos de teclado. Cada item define `key`, `command`, `context` e `description`. A cobertura detalhada fica em [[06 - Lazygit — operações avançadas]].

Exemplo simples:

```yaml
customCommands:
  - key: "<C-f>"
    command: "git push --force-with-lease"
    context: "global"
    description: "Force-push with lease"
```

### Theme custom

O `gui.theme` aceita mapa de elementos visuais para arrays `[cor, modificador?]`.

Cores aceitas: nomes (`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`) ou hex (`#rrggbb`).

Modificadores aceitos: `bold`, `default`, `reverse`, `underline`, `strikethrough`.

Propriedades de tema disponíveis:

| Propriedade | Descrição |
|---|---|
| `activeBorderColor` | Borda do painel ativo |
| `inactiveBorderColor` | Borda dos painéis inativos |
| `searchingActiveBorderColor` | Borda durante busca ativa |
| `optionsTextColor` | Cor do texto de ajuda (bottom bar) |
| `selectedLineBgColor` | Background da linha selecionada |
| `inactiveViewSelectedLineBgColor` | Seleção em painéis inativos |
| `cherryPickedCommitFgColor` | Texto de commit marcado pra cherry-pick |
| `cherryPickedCommitBgColor` | Background de commit marcado pra cherry-pick |
| `unstagedChangesColor` | Indicador de mudanças unstaged |
| `defaultFgColor` | Cor de texto padrão |

Exemplo Catppuccin-ish:

```yaml
gui:
  theme:
    activeBorderColor: ["#a6e3a1", "bold"]
    inactiveBorderColor: ["#585b70"]
    optionsTextColor: ["#cdd6f4"]
    selectedLineBgColor: ["#313244"]
    unstagedChangesColor: ["#f38ba8"]
    defaultFgColor: ["#cdd6f4"]
```

### Versionar nos dotfiles

Manter o `config.yml` no repositório de dotfiles garante setup repetível em qualquer máquina.

Estratégia com symlink manual:

```bash
mkdir -p ~/dotfiles/lazygit
mv ~/.config/lazygit/config.yml ~/dotfiles/lazygit/config.yml
ln -s ~/dotfiles/lazygit/config.yml ~/.config/lazygit/config.yml
```

Estratégia com GNU Stow (se o repo de dotfiles usar Stow):

```bash
# Estrutura: ~/dotfiles/lazygit/.config/lazygit/config.yml
stow -d ~/dotfiles -t ~ lazygit
```

Galho 5 (Dotfiles, planejado) cobre estratégias completas de gerenciamento de dotfiles.

---

## Na prática

### Setup mínimo recomendado

Config funcional e opinada para dev workflow com Neovim:

```yaml
# ~/.config/lazygit/config.yml
gui:
  nerdFontsVersion: "3"
  showFileTree: true
  showFileIcons: true
  mouseEvents: true
git:
  paging:
    colorArg: "always"
    useConfig: false
  log:
    order: "topo-order"
    showGraph: "when-maximised"
  pull:
    rebase: true
os:
  editPreset: "nvim"
```

Justificativas:
- `nerdFontsVersion: "3"` — habilita ícones modernos (requer Nerd Font instalada no emulador)
- `colorArg: "always"` com `useConfig: false` — cores confiáveis no diff view
- `pull.rebase: true` — evita merge commits desnecessários no fetch/pull
- `editPreset: "nvim"` — `o` em arquivo abre Neovim; `e` abre na linha do conflito

### Theme escuro custom (Catppuccin Mocha)

Paleta consistente com o Catppuccin Mocha, compatível com outros apps do terminal:

```yaml
gui:
  theme:
    activeBorderColor: ["#a6e3a1", "bold"]
    inactiveBorderColor: ["#585b70"]
    searchingActiveBorderColor: ["#f9e2af", "bold"]
    optionsTextColor: ["#cdd6f4"]
    selectedLineBgColor: ["#313244"]
    inactiveViewSelectedLineBgColor: ["#1e1e2e"]
    cherryPickedCommitFgColor: ["#1e1e2e"]
    cherryPickedCommitBgColor: ["#cba6f7"]
    unstagedChangesColor: ["#f38ba8"]
    defaultFgColor: ["#cdd6f4"]
```

Temas prontos da comunidade (Catppuccin, Gruvbox, Nord, Tokyo Night) disponíveis em https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Pagers.md e no repositório de themes do lazygit.

### Integração com Neovim em pane vizinho

Com `editPreset: "nvim"`, pressionar `o` em um arquivo no painel Files abre Neovim no pane atual do Lazygit (o Lazygit suspende e cede o terminal).

Para abrir o arquivo num pane vizinho do Zellij sem sair do Lazygit, usar `editAtLine` com `zellij action`:

```yaml
os:
  editPreset: ""
  editAtLine: "zellij action write-chars ':e {{filename}}' && zellij action move-focus right"
  # Alternativa mais robusta: custom script que envia comando pro pane Neovim adjacente
```

A estratégia completa de integração Lazygit ↔ Zellij ↔ Neovim (incluindo plugin `lazygit.nvim`) é coberta em nota 07 do galho 3 (Multiplexer).

---

## Armadilhas

**1. `paging.useConfig: true` causa diff sem cores**

- **Causa:** Lazygit passa o controle de paginação pro `core.pager` do git, que frequentemente é `less` sem flag `--color`. O pager stripa os escape codes de cor antes de exibir.
- **Sintoma:** diff view em preto-e-branco; nenhuma linha colorida de `+`/`-`.
- **Como detectar:** ativar `useConfig: true` e observar o diff; comparar com `useConfig: false`.
- **Solução:** manter `useConfig: false` (default) + `colorArg: "always"`. Se quiser usar pager custom, definir em `paging.pager` dentro do config do Lazygit, não no git global.

**2. `editPreset` errado — editor não abre**

- **Causa:** typo no valor do preset ou preset não instalado no sistema. Ex: `editPreset: "nvm"` (typo de `nvim`).
- **Sintoma:** pressionar `o` ou `e` no painel Files não faz nada ou exibe erro de "command not found".
- **Como detectar:** `cat ~/.config/lazygit/config.yml` e conferir o valor; testar o comando do editor diretamente no shell.
- **Solução:** checar a lista de presets em Config.md (valores exatos: `nvim`, `vim`, `vscode`, `helix`, `emacs`, `nano`, `micro`, `lvim`, `nvim-remote`, `sublime`, `bbedit`, `kakoune`, `xcode`, `zed`, `acme`). Se o preset não contemplar o editor desejado, usar `os.edit` e `os.editAtLine` com comando custom.

**3. Indentação YAML errada quebra toda a config**

- **Causa:** YAML é sensível a indentação (2 espaços); copy-paste de snippets com tabs ou 4 espaços gera parse error. Um único nível incorreto invalida a seção inteira ou o arquivo todo.
- **Sintoma:** Lazygit ignora o config ou exibe erro de startup ("failed to parse config"). Pode iniciar com defaults, mascarando o problema.
- **Como detectar:** `yq . ~/.config/lazygit/config.yml` valida o YAML e mostra o erro com número de linha. Sem `yq`: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" ~/.config/lazygit/config.yml`.
- **Solução:** usar sempre 2 espaços; configurar o editor para expandir tabs em YAML (`expandtab` no Neovim com `FileType yaml`).

**4. Cor de tema inválida — elemento sem cor ou erro na startup**

- **Causa:** hex sem `#` (ex: `aabbcc` em vez de `#aabbcc`) ou nome de cor inexistente (ex: `"gray"` — não é suportado; usar `"white"` ou hex).
- **Sintoma:** borda ou texto sem cor; em casos extremos, Lazygit não inicia.
- **Como detectar:** isolar a propriedade de tema suspeita; testar com valor conhecido (`"green"` ou `"#00ff00"`).
- **Solução:** usar apenas nomes da lista oficial (`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`) ou hex `#rrggbb`. Arrays de tema devem ser lista YAML: `["#aabbcc", "bold"]` ou notação multi-linha com `- "#aabbcc"`.

**5. `customCommands` não dispara — `context` errado**

- **Causa:** o campo `context` define em qual painel o keybinding é ativo. Contexto errado (ex: `"commits"` quando o cursor está em `"files"`) faz o atalho não responder.
- **Sintoma:** pressionar a `key` definida no custom command não faz nada.
- **Como detectar:** trocar `context` pra `"global"` temporariamente — se funcionar, o contexto original estava errado. Valores válidos incluem: `"global"`, `"files"`, `"branches"`, `"commits"`, `"stash"`, `"main"`.
- **Solução:** consultar `Custom_Command_Keybindings.md` no repo oficial pra lista de contextos; usar `"global"` para comandos que devem funcionar em qualquer painel.

**6. `log.showWholeGraph: true` trava em repos grandes**

- **Causa:** o flag passa `--all` pro `git log`, que inclui todos os branches e tags no grafo. Repos com histórico extenso ou muitos branches remote tornam o carregamento muito lento.
- **Sintoma:** Lazygit congela ou demora vários segundos ao abrir ou ao navegar para o painel Commits.
- **Como detectar:** ativar `showWholeGraph: true` e medir tempo de abertura; desativar e comparar.
- **Solução:** manter `showWholeGraph: false` (default). Para ver `--all` ocasionalmente, usar `branchLogCmd` com flag condicional ou abrir o log num terminal separado.

---

## Em inglês

- **configuração** — *configuration / config file*. "arquivo YAML que persiste preferências do Lazygit entre sessões."
- **tema** — *theme*. "mapa de cores e modificadores aplicados aos elementos visuais da TUI."
- **preset** — *preset*. "configuração predefinida e embutida; `editPreset` define o editor sem precisar especificar o comando completo."
- **keybinding** — *keybinding*. "mapeamento de tecla (ou combinação) pra ação específica num contexto do Lazygit."
- **comando customizado** — *custom command*. "ação shell definida pelo usuário e ativada por atalho; configurada em `customCommands`."
- **paginação** — *paging*. "exibição de diff longa com suporte a scroll via pager externo (delta, diff-so-fancy, bat)."
- **cor hexadecimal** — *hex color*. "código de cor no formato `#rrggbb`; alternativa aos nomes de cor nominais do Lazygit."
- **indentação** — *indentation*. "espaços que estruturam o YAML; 2 espaços por nível — tabs causam parse error."
- **parse** — *parse*. "leitura e interpretação do arquivo YAML pelo Lazygit na startup; erro de parse geralmente resulta em config ignorado."
- **dotfiles** — *dotfiles*. "arquivos de configuração do Unix (prefixados com `.`) versionados num repositório pra reproduzir o ambiente em qualquer máquina."

---

## Veja também

- [[01 - Lazygit — overview e operações essenciais]] — pré-req: painéis, layout e operações básicas
- [[06 - Lazygit — operações avançadas]] — customCommands em profundidade
- [[03-Dominios/Tecnologia/Terminal/Editor/index|Editor (Neovim)]] — `editPreset: nvim` e integração
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Editor preset|editor preset]], [[Dicionário do Terminal#Lazygit|lazygit]]

---

## Referências

- Lazygit Config: https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md
- Lazygit Custom Commands: https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Command_Keybindings.md
