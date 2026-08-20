---
title: "bat — cat moderno com syntax highlight"
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
  - bat
aliases:
  - bat
---

# bat — cat moderno com syntax highlight

> [!abstract] TL;DR
> bat é cat moderno com syntax highlight, line numbers, integração git (changes inline). Detecta TTY: em pipe vira cat puro (preserva scripts); em terminal mostra highlight + paginação. Configurável via `BAT_THEME`, `BAT_PAGER`, `BAT_STYLE`. Usado como preview do fzf e como `MANPAGER`. Em Debian/Ubuntu o binário se chama `batcat`.

## O que é / Como funciona

### Filosofia: cat com superpoderes, mas compatível

bat é um substituto moderno ao `cat`, escrito em Rust, que mantém compatibilidade com scripts enquanto adiciona qualidade de vida no terminal interativo. O princípio guia é simples: em terminal interativo, mostra tudo (highlight, números, paginação); em pipe ou redirecionamento, comporta-se como `cat` puro, sem decoração alguma.

Isso significa que ao adotar bat, scripts que usam `cat arquivo | grep padrão` continuam funcionando sem modificação — a TTY detection garante que `bat` não injete escape sequences em pipelines.

### Features principais

- **Syntax highlighting** via `syntect` (~150 linguagens; mesma engine de gramáticas do Sublime Text `.sublime-syntax`).
- **Line numbers** em modo terminal (suprimidos em pipe automaticamente).
- **Git diff inline**: margem lateral com `+` (adição), `-` (remoção), `~` (modificação) para mudanças não commitadas.
- **Paginação automática** via `less -R` por padrão.
- **Themes customizáveis**: compatível com `.tmTheme` do TextMate/Sublime; ~30 themes embutidos.

### Env vars relevantes

| Variável | Função | Default |
|---|---|---|
| `BAT_THEME` | Tema de syntax highlight | `Monokai Extended` (escuro) / `Monokai Extended Light` (claro) |
| `BAT_PAGER` | Pager usado pelo bat | `less -R` |
| `BAT_STYLE` | Componentes exibidos | `changes,grid,header-filename,numbers,snip` |
| `BAT_PAGING` | Modo de paginação | `auto` |

Ver temas disponíveis: `bat --list-themes`. Ver linguagens: `bat --list-languages`.

### TTY detection

bat verifica se `stdout` é um terminal interativo (`isatty(1)`). O resultado define os defaults:

- **Em terminal:** `--color=auto` → colorido; `--paging=auto` → pagina se output > tela.
- **Em pipe/arquivo:** plain text, sem escape sequences, sem pager — equivale a `cat`.

Para forçar cores em pipe (ex.: passar para outro programa que entende ANSI): `--color=always`. Para desabilitar pager mantendo cores: `--paging=never`.

### Integração com MANPAGER

Receita oficial para usar bat como renderizador de manpages:

```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
```

O `col -bx` remove backspaces antigos usados pela formatação clássica de man (bold = `letra BS letra`). Sem ele, bat recebe `_b_o_l_d` literal e o output fica corrompido. Com ele, `man find` exibe a manpage com syntax highlight e busca interativa via less.

### Integração com fzf

bat é o preview padrão de arquivos com fzf:

```bash
fzf --preview 'bat --color=always --style=numbers --line-range=:500 {}'
```

O `--color=always` força cores mesmo no pipe para o preview do fzf. `--line-range=:500` limita a 500 linhas para performance.

## Na prática

### Setup básico

```bash
# Escolher tema interativamente
bat --list-themes | fzf --preview "bat --theme={} README.md"

# Configurar tema via env var (adicionar ao .zshrc)
export BAT_THEME="Dracula"

# Configurar estilo padrão
export BAT_STYLE="numbers,changes,grid"

# Configurar MANPAGER
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
```

### Receitas comuns

```bash
# Exibir arquivo com highlight
bat src/main.rs

# Comparar dois arquivos (git diff inline)
bat --diff file_a file_b

# Forçar linguagem (útil pra arquivos sem extensão reconhecida)
bat -l json config.txt

# Modo plain: sem números, sem grid, sem pager
bat -p arquivo.txt

# Forçar cores em pipe (para outro programa que entende ANSI)
echo '{"a": 1}' | bat -l json --color=always

# Manpage com highlight (após configurar MANPAGER)
man find

# Mostrar caracteres não-imprimíveis
bat -A arquivo.bin
```

### Aliases sugeridos

NÃO aliasing `cat=bat` global — a TTY detection já cuida da maioria dos casos, e o alias pode quebrar scripts em contextos inesperados. Prefira funções wrapper pontuais:

```bash
# Debian/Ubuntu: alias necessário pelo nome do binário
alias bat=batcat

# Wrapper pra leitura com paginação sempre ativa, sem decoração
alias batp='bat --paging=always --style=plain'
```

Versão hedged: bat 0.24+; verifique `bat --version` localmente.

## Armadilhas

### (1) Aliasing `cat=bat` quebra scripts que dependem de cat-strict

**Causa:** a TTY detection do bat, embora boa, não é idêntica ao cat POSIX em todos os edge cases; alias global expõe scripts a comportamento inesperado.

**Sintoma:** script funciona localmente, falha em container/CI (ou produz saída inesperada).

**Como detectar:** `[ -t 1 ] && echo "é TTY" || echo "é pipe"` no script revela o contexto; bat em CI sem TTY pode detectar errado dependendo da versão.

**Solução:** evitar `alias cat=bat` global. Usar `alias bat=batcat` (Debian) ou função wrapper `bcat()`. Reservar `cat` puro para scripts.

### (2) `BAT_PAGER=less` sem `-R` perde cores

**Causa:** qualquer customização manual de `BAT_PAGER` que omita `-R` faz o less exibir escape sequences literalmente em vez de interpretá-las.

**Sintoma:** paginação exibe `^[[31m...` literal em vez de cores — lixo visual no terminal.

**Como detectar:** `echo $BAT_PAGER` mostra `less` sem flags.

**Solução:** `export BAT_PAGER="less -R"`. O `-R` instrui o less a interpretar escape sequences ANSI em vez de exibi-las literalmente. O default do bat já define `less -R`.

### (3) Binários abrindo no pager e travando terminal

**Causa:** bat não bloqueia abertura de binários por padrão; `bat -A` em arquivo binário grande injeta sequências de controle não-renderizáveis no terminal.

**Sintoma:** terminal cheio de caracteres de controle; necessita `reset` para restaurar.

**Como detectar:** executar `bat arquivo.png` ou `bat executavel` — bat exibe warning mas `bat -A` em binário grande vira bagunça.

**Solução:** confiar no warning default do bat para binários; usar `xxd` ou `hexdump` para inspecionar conteúdo binário real. Nunca usar `bat -A` em arquivos cujo tipo é desconhecido.

### (4) `batcat` vs `bat` em Debian/Ubuntu

**Causa:** o pacote `bat` no apt Debian/Ubuntu instala o binário como `batcat` por colisão histórica com `bacula-console`.

**Sintoma:** `bat: command not found` mesmo após `apt install bat`; `batcat` funciona.

**Como detectar:** `which bat` falha; `which batcat` resolve.

**Solução:** `alias bat=batcat` no `.zshrc`, ou symlink `ln -s /usr/bin/batcat ~/.local/bin/bat`. Scripts portáveis devem detectar ambos: `command -v bat || command -v batcat`.

### (5) Tema escuro/claro descalibrado com o terminal

**Causa:** o tema do bat não foi combinado com o tema de fundo do emulador de terminal (escuro vs claro).

**Sintoma:** texto quase invisível — letras claras sobre fundo claro, ou escuras sobre escuro.

**Como detectar:** abrir qualquer arquivo conhecido e verificar legibilidade.

**Solução:** combinar o tema bat com o tema do terminal. Sugestões: `Monokai Extended` ou `Dracula` para fundo escuro; `GitHub` ou `OneHalfLight` para fundo claro. Escolher interativamente: `bat --list-themes | fzf --preview "bat --theme={} README.md"`.

### (6) `MANPAGER` configurado errado quebra `man`

**Causa:** receitas simplificadas omitem `col -bx`, deixando backspaces literais da formatação man antiga chegarem ao bat.

**Sintoma:** `man find` exibe `_b___b_o___o_l___l_d` com underscores excessivos em vez de texto bold.

**Como detectar:** abrir qualquer manpage após configurar `MANPAGER`.

**Solução:** usar a receita oficial completa:

```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
```

O `col -bx` processa e remove os backspaces antes do bat aplicar o highlight.

## Em inglês

Termos técnicos que aparecem ao ler docs e fóruns sobre bat:

- **realce de sintaxe** — *syntax highlighting*. "bat usa syntax highlighting via syntect para colorizar código por estrutura sintática."
- **paginador** — *pager*. "Um pager como `less` divide output longo em páginas navegáveis no terminal."
- **TTY (terminal)** — *TTY (terminal)*. "bat detecta se stdout é um TTY interativo para decidir se aplica cores e paginação."
- **variável de ambiente** — *environment variable*. "BAT_THEME e BAT_PAGER são environment variables que configuram o bat."
- **tema** — *theme*. "O theme define o conjunto de cores aplicado ao syntax highlight; escolha com `bat --list-themes`."
- **numeração de linhas** — *line numbers*. "bat exibe line numbers na margem esquerda em modo terminal; em pipe são suprimidas."
- **paginação** — *paging*. "bat aplica paging automático via less quando o output excede a altura do terminal."
- **conteúdo binário** — *binary content*. "bat exibe warning ao abrir binary content; use `xxd` ou `hexdump` para inspeção real."
- **sequência de escape** — *escape sequence*. "Escape sequences ANSI (`ESC[...m`) codificam cores; `less -R` é necessário para interpretá-las."
- **página de manual** — *manpage*. "bat pode ser configurado como MANPAGER para exibir manpages com syntax highlight."

## Veja também

- [[01 - fzf — fuzzy finder universal]] — bat como preview default
- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — pipeline com bat preview
- [[10 - delta — pager moderno pra git diff]] — delta usa engine similar (syntect)
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#bat|bat]]
- [[Dicionário do Terminal#BAT_THEME|BAT_THEME]]
- [[Dicionário do Terminal#batcat|batcat]]
- [[Dicionário do Terminal#MANPAGER|MANPAGER]]
- [[Dicionário do Terminal#TTY detection|TTY detection]]
- [[Dicionário do Terminal#syntax pager|syntax pager]]

## Referências

- bat repo: https://github.com/sharkdp/bat
- bat customization: https://github.com/sharkdp/bat#customization
