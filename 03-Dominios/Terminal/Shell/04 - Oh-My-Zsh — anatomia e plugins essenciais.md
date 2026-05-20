---
title: "Oh-My-Zsh — anatomia e plugins essenciais"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - oh-my-zsh
  - plugins
aliases:
  - Oh-My-Zsh
  - OMZ
---

# Oh-My-Zsh — anatomia e plugins essenciais

> [!abstract] TL;DR
> Oh-My-Zsh é um framework de config pra Zsh: você clona em `~/.oh-my-zsh/`, source no `.zshrc`, e ganha um loader que ativa plugins via array `plugins=(...)`. Plugins essenciais (`git`, `zsh-autosuggestions`, `zsh-syntax-highlighting`, `direnv`) cobrem 90% das necessidades. Ordem importa: `zsh-syntax-highlighting` DEVE ser o último no array.

## O que é / Como funciona

### OMZ não é Zsh

Oh-My-Zsh é um **overlay de configuração** para o Zsh — não um shell diferente. Sem OMZ, Zsh funciona normalmente com suas configurações em `~/.zshrc`. Com OMZ instalado, esse mesmo `.zshrc` passa a conter um `source "$ZSH/oh-my-zsh.sh"` que ativa o framework: plugin loader, temas, funções helper e aliases automáticos.

A distinção importa porque confundir OMZ com Zsh leva a erros de diagnóstico. Se o Zsh travar, verifique primeiro se é o shell ou um plugin OMZ.

**O que OMZ agrega sobre o Zsh puro:**
- Plugin loader (ativa plugins via array `plugins=(...)`)
- 300+ plugins embarcados
- 150+ temas embarcados
- Funções helper reutilizáveis (ex: `current_branch`, `take`)
- Update automático periódico

### Layout de `~/.oh-my-zsh/`

```
~/.oh-my-zsh/
├── oh-my-zsh.sh          # entrypoint: source este arquivo no .zshrc
├── lib/                  # funções helper carregadas automaticamente
│   ├── completion.zsh    # configura compinit
│   ├── history.zsh       # defaults de history
│   ├── git.zsh           # funções de Git usadas pelo tema
│   └── ...
├── plugins/              # plugins embarcados (não edite)
│   ├── git/
│   │   └── git.plugin.zsh
│   ├── direnv/
│   │   └── direnv.plugin.zsh
│   └── ...
├── themes/               # temas embarcados (não edite)
│   ├── robbyrussell.zsh-theme
│   └── ...
├── custom/               # SEU terreno — sobrevive a updates
│   ├── plugins/          # plugins externos (zsh-autosuggestions, etc.)
│   ├── themes/           # temas externos (Powerlevel10k, etc.)
│   └── example.zsh       # aliases e overrides pessoais
└── cache/                # completion cache e controle de update
```

A pasta `custom/` nunca é sobrescrita pelo `omz update`. Tudo que você cria ou clona aqui persiste entre atualizações do framework.

### Sequência de inicialização de `oh-my-zsh.sh`

Quando o `.zshrc` executa `source "$ZSH/oh-my-zsh.sh"`, a ordem interna simplificada é:

1. **Verifica update** — consulta `cache/` pra ver se está na frequência configurada
2. **Source `lib/*`** — carrega helpers, defaults de history, completion, etc.
3. **`compinit`** — inicializa o sistema de completion do Zsh
4. **Loop sobre `plugins=(...)`** — para cada nome:
   - Procura `$ZSH/plugins/<nome>/<nome>.plugin.zsh` (embarcado)
   - Fallback: `$ZSH_CUSTOM/plugins/<nome>/<nome>.plugin.zsh` (custom)
   - Source o arquivo encontrado
5. **Source do tema** — carrega o `.zsh-theme` configurado em `ZSH_THEME`
6. **Customizações do usuário** — o que vier depois do `source` no `.zshrc`

Esse fluxo explica por que `zsh-syntax-highlighting` deve ser o **último plugin** — ele precisa encontrar todos os widgets ZLE já registrados pelos plugins anteriores.

### Array de plugins

```zsh
# ~/.zshrc
plugins=(
  git
  direnv
  zsh-autosuggestions
  zsh-syntax-highlighting   # SEMPRE último entre os syntax-related
)
```

Regras do array:
- Elementos separados por espaços (ou newlines) — **nunca vírgulas**
- OMZ resolve o caminho em dois lugares: `$ZSH/plugins/<nome>/` (embarcado) e `$ZSH_CUSTOM/plugins/<nome>/` (custom)
- Plugins externos precisam ser clonados manualmente antes de funcionar

### Plugins essenciais

#### `git` (embarcado)

O plugin mais usado do OMZ. Fornece dezenas de aliases curtos para Git e algumas funções utilitárias usadas pelos temas:

| Alias | Comando completo |
|---|---|
| `gst` | `git status` |
| `gco` | `git checkout` |
| `gp` | `git push` |
| `gl` | `git pull` |
| `glog` | `git log --oneline --decorate --graph` |
| `ga` | `git add` |
| `gcmsg` | `git commit -m` |

A função `current_branch` retorna a branch atual e é usada pelos temas pra montar o prompt.

#### `zsh-autosuggestions` (externo — `zsh-users/zsh-autosuggestions`)

Sugere comandos enquanto você digita, exibindo uma sugestão em cinza inline logo após o cursor. A sugestão é baseada no history do Zsh (e opcionalmente em completions).

**Aceitar sugestão:**
- `→` (right-arrow) ou `End` — aceita a sugestão inteira
- `Ctrl-F` — aceita a sugestão inteira (alternativa)
- `Ctrl-→` (forward-word) — aceita parcialmente até a próxima palavra

**Configuração útil:**

```zsh
# Personaliza estilo visual (fg=8 é cinza, default)
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=8,underline"

# Estratégia de sugestão: history (default), completion, ou ambas
ZSH_AUTOSUGGEST_STRATEGY=(history completion)

# Desativa sugestões pra comandos muito longos (performance)
ZSH_AUTOSUGGEST_BUFFER_MAX_SIZE=20
```

#### `zsh-syntax-highlighting` (externo — `zsh-users/zsh-syntax-highlighting`)

Colore comandos enquanto você digita, antes de pressionar Enter:
- **Verde** — comando válido (existe no `$PATH` ou é builtin)
- **Vermelho** — comando inválido (não encontrado)
- **Amarelo** — alias
- **Azul** — path existente

O efeito imediato é capturar typos antes de executar. Se o comando ficou vermelho, tem erro de digitação.

**Por que deve ser o último plugin:** o plugin funciona envolvendo (wrapping) widgets ZLE. Se sourced antes de outros plugins que registram widgets com `zle -N`, ele não captura esses widgets e perde o highlight em comandos adicionados por eles. Em Zsh 5.8+, usa `add-zle-hook-widget`, então os hooks rodam na ordem de registro — zsh-syntax-highlighting deve registrar por último.

#### `direnv` (embarcado)

Integra o utilitário `direnv` ao Zsh. Cria o hook que `direnv` precisa para carregar/descarregar variáveis de ambiente automaticamente ao entrar e sair de diretórios com `.envrc`.

Exemplo: entrar em `~/projetos/api/` que tem `.envrc` com `export DATABASE_URL=...` — o `direnv` carrega a variável automaticamente. Sair do diretório a descarrega.

Requer `direnv` instalado (`brew install direnv` ou via package manager). O plugin só cria o hook — o utilitário em si é externo.

### Plugins debatíveis (com tradeoff)

#### `fast-syntax-highlighting`

Alternativa mais rápida ao `zsh-syntax-highlighting`, com mais tipos de highlight (paths, globbing, expressões). O nome é enganoso — não é compatível com `zsh-syntax-highlighting`.

> [!warning] Conflito
> **NUNCA** use `fast-syntax-highlighting` e `zsh-syntax-highlighting` juntos. Os dois envolvem os mesmos widgets ZLE e o resultado é cores quebradas ou degradação de performance. Escolha um.

#### `fzf-tab`

Substitui o menu de completion padrão do Zsh por uma interface fuzzy (`fzf`). Muito popular em setups avançados — permite navegar completions com preview interativo.

**Posição no array:** deve vir **antes** de `zsh-syntax-highlighting`, mas **depois** de outros plugins de completion. A ordem recomendada: `zsh-autosuggestions` → `fzf-tab` → `zsh-syntax-highlighting`.

Requer `fzf` instalado.

#### `zsh-autocomplete`

Plugin de `marlonrichert` que sobrepõe completamente o sistema de completion do Zsh: exibe opções em tempo real enquanto você digita, sem pressionar Tab. É uma mudança significativa de comportamento.

**Caveats importantes:**
- Altera o fluxo de Tab — o comportamento default do OMZ muda radicalmente
- Conflita com `fzf-tab` (os dois competem pelo controle de completions)
- Requer Zsh 5.8+
- A ordem de source importa: deve ser sourced **antes** de plugins que sobrescrevem bindings, o que conflita com a regra do `zsh-syntax-highlighting`
- Usuários que migram de `zsh-autocomplete` para `fzf-tab` frequentemente precisam limpar a config de completion

Use com cautela em setups OMZ. Avalie antes de adotar em ambiente de produção.

### Modo de update

```zsh
# ~/.zshrc — antes do source do OMZ
zstyle ':omz:update' mode reminder    # avisa quando tem update (default)
zstyle ':omz:update' mode auto        # atualiza silenciosamente
zstyle ':omz:update' mode disabled    # nunca atualiza automaticamente
zstyle ':omz:update' frequency 7      # frequência em dias (default: 13)
```

## Na prática

### Instalar OMZ

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

O script faz backup do `.zshrc` existente (renomeia para `.zshrc.pre-oh-my-zsh`), clona o repo em `~/.oh-my-zsh/` e cria um novo `.zshrc` com configuração básica.

### Instalar plugin externo (zsh-autosuggestions)

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

Depois adicionar `zsh-autosuggestions` ao array `plugins=(...)` no `.zshrc` e recarregar:

```bash
source ~/.zshrc
```

### Instalar zsh-syntax-highlighting

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### Ordem recomendada no array

```zsh
plugins=(
  git
  direnv
  zsh-autosuggestions
  fzf-tab                       # se usar — antes do syntax-highlight
  zsh-syntax-highlighting       # ÚLTIMO
)
```

### Inspecionar o setup atual

```bash
omz plugin list                 # lista todos os plugins disponíveis
omz plugin info git             # mostra README do plugin git
omz update                      # roda update manual imediato
```

### Recarregar sem fechar terminal

```bash
source ~/.zshrc
```

Em inglês: **source the file** (executar/recarregar o arquivo de config no shell atual). Diferente de abrir um novo terminal, que também sourceia o `.zshrc`, mas perde o estado da sessão atual.

## Armadilhas

### (1) Double-load: `fast-syntax-highlighting` + `zsh-syntax-highlighting`

Os dois plugins envolvem os mesmos widgets ZLE. Usar ambos no array `plugins=(...)` resulta em conflito: cores quebradas, highlight incorreto, ou lentidão. **Solução:** escolha apenas um.

```zsh
# ERRADO — conflito garantido
plugins=(
  zsh-autosuggestions
  fast-syntax-highlighting
  zsh-syntax-highlighting
)

# CORRETO — escolha um
plugins=(
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

### (2) `zsh-syntax-highlighting` não é o último plugin

Se `zsh-syntax-highlighting` não for o último no array, plugins carregados depois dele que registram novos widgets ZLE não terão seus comandos coloridos corretamente. O highlight deixa de funcionar para tudo adicionado por esses plugins posteriores.

```zsh
# ERRADO
plugins=(
  zsh-syntax-highlighting   # sourced antes dos outros
  zsh-autosuggestions
  git
)

# CORRETO
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting   # SEMPRE último
)
```

### (3) `zsh-autocomplete` conflita com o fluxo de completion padrão

O plugin `zsh-autocomplete` sobrepõe `_omz_completion` e redefine o comportamento de Tab. Rodar simultaneamente com `fzf-tab` resulta em comportamento imprevisível — os dois competem pelo controle do mesmo mecanismo. Além disso, ao migrar para `fzf-tab` depois de ter usado `zsh-autocomplete`, pode ser necessário rodar `compinit` manualmente ou remover o cache em `~/.zcompdump`.

### (4) Bracketed-paste quebra com URLs e aspas

Em alguns terminais, o `bracketed-paste-magic` (ativo por default no OMZ) transforma colagem de texto com aspas ou URLs em sequências de escape inesperadas. Sintoma: colar `https://example.com?foo=bar&baz=1` vira lixo no prompt.

**Solução:** adicionar antes do `source` do OMZ no `.zshrc`:

```zsh
DISABLE_MAGIC_FUNCTIONS="true"
```

### (5) NVM/SDKMan tornam o shell lento

`nvm` e ferramentas similares carregam scripts pesados no `.zshrc`, aumentando o tempo de abertura de um novo terminal de ~100ms para vários segundos. Isso não é culpa do OMZ, mas aparece como "OMZ lento".

**Mitigação:** lazy-load — só carrega o NVM quando `node` é chamado pela primeira vez:

```zsh
# Lazy-load NVM — não carrega no startup
node() {
  unfunction node
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
  node "$@"
}
```

## Em inglês

| Português | Inglês |
|---|---|
| framework de shell | shell framework |
| recarregar (o arquivo) | source (the file) — `source ~/.zshrc` |
| atalho | shortcut |
| atualizar | update |
| conflito de plugins | plugin conflict |
| tema | theme |
| personalização | customization |
| carregador de plugins | plugin loader / plugin manager |
| sugestão inline | inline suggestion |
| realce de sintaxe | syntax highlighting |

## Veja também

- `[[02 - Zsh essencial]]`
- `[[03 - History do Zsh]]` — plugin `history-substring-search`
- `[[05 - Powerlevel10k]]` — theme primário
- `[[08 - Completion system (compsys)]]` — conflito `zsh-autocomplete` aprofundado
- `[[10 - Plugins, themes e custom no OMZ]]` — escrever seu plugin
- `[[03-Dominios/Terminal/Shell/index|MOC do galho]]`
- `[[Dicionário do Terminal#Oh-My-Zsh|Oh-My-Zsh]]`, `[[Dicionário do Terminal#Plugin (OMZ)|plugin]]`, `[[Dicionário do Terminal#Zsh-autosuggestions|zsh-autosuggestions]]`, `[[Dicionário do Terminal#Zsh-syntax-highlighting|zsh-syntax-highlighting]]`

## Referências

- [Oh-My-Zsh — repositório oficial](https://github.com/ohmyzsh/ohmyzsh)
- [Oh-My-Zsh wiki — lista de plugins](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins)
- [zsh-autosuggestions — zsh-users](https://github.com/zsh-users/zsh-autosuggestions)
- [zsh-syntax-highlighting — zsh-users](https://github.com/zsh-users/zsh-syntax-highlighting)
- [zsh-autocomplete — marlonrichert](https://github.com/marlonrichert/zsh-autocomplete)
- [awesome-zsh-plugins](https://github.com/unixorn/awesome-zsh-plugins)
