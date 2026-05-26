---
title: "eza — ls moderno"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - cli-utils
  - iniciado
  - eza
  - listing
aliases:
  - eza
  - ls moderno
---

# eza — ls moderno

> [!abstract] TL;DR
> eza é ls moderno em Rust — fork ativo do exa (arquivado em agosto 2023). Cores por tipo, ícones (com Nerd Font), modo árvore (`--tree`), status git inline (`--git`), color-scale por tamanho/idade. Configurável via `EZA_COLORS` (sintaxe diferente de `LS_COLORS`). Substitui `ls` pra inspeção visual rápida; mantém compat com ls(1) só parcialmente.

## O que é / Como funciona

### Filosofia e história

exa foi criado em 2014 por Benjamin Sago como alternativa moderna ao `ls`. Em agosto de 2023, o projeto foi oficialmente arquivado — sem novos releases ou correções de segurança. eza nasceu como fork comunitário ativo pouco depois, mantendo compatibilidade de flags e adicionando features novas: suporte a cores bright, theming via `theme.yml`, mais opções de sorting, e correções de segurança ausentes no exa.

eza NÃO é drop-in replacement de `ls` — algumas flags diferem e há features sem equivalente no ls(1) clássico. Em compensação, o output visual é muito mais rico: cores por tipo de arquivo, ícones de Nerd Font, integração git, color-scale por tamanho ou idade, e header de colunas em modo long. O princípio guia é inspeção visual rápida — não portabilidade POSIX.

### Modos principais

- **`eza`** — listagem simples com cores por tipo; diretórios em azul, executáveis em verde, links em ciano.
- **`eza -l`** — long format: permissões (rwxr-xr-x), owner, tamanho humano, data de modificação, nome.
- **`eza -a`** — inclui hidden files (nome começando com `.`, inclusive `.` e `..`).
- **`eza -A` / `--almost-all`** — hidden, mas pula `.` e `..`; compat com `ls -A`.
- **`eza --tree` / `-T`** — modo árvore recursiva; `-L 2` (ou `--level=2`) limita profundidade.
- **`eza --git`** — coluna de status git (M modified, A added, D deleted, I ignored, N new, T type-changed).
- **`eza -lah`** — combinação comum: long + all + human-readable (tamanho em KB/MB/GB).

### Ícones e Nerd Font

`--icons` ativa ícones por tipo de arquivo e diretório. Requer dois fatores simultâneos: (1) Nerd Font instalada no sistema, (2) Nerd Font configurada no emulador de terminal. Sem Nerd Font corretamente configurada, os glyphs Unicode do Private Use Area (PUA) aparecem como quadrados `□` ou `?`. Fontes recomendadas: MesloLGS NF, FiraCode Nerd Font, JetBrainsMono NF.

Para ativar automaticamente sem flag manual: `export EZA_ICONS_AUTO=1` no `.zshrc`.

### Color-scale

`--color-scale=size` ou `--color-scale=age` aplica gradiente de cor ao campo correspondente — tamanho ou data de modificação. Arquivos maiores ou mais antigos recebem cor mais intensa. Visual rápido para "quem é grande aqui" ou "o que foi modificado recentemente" sem precisar ordenar.

### Sorting

`--sort=CAMPO` — campos válidos: `name`, `size`, `modified`, `created`, `extension`, `inode`. `-r` / `--reverse` reverte a ordem. `--group-directories-first` coloca diretórios antes dos arquivos, independente do sort escolhido.

### EZA_COLORS vs LS_COLORS

eza usa a env var `EZA_COLORS` com sintaxe própria — **não compatível com `LS_COLORS`** do GNU dircolors. O formato é `chave=código_ansi` separado por `:` (ex: `di=34;01:fi=32`). As chaves disponíveis são específicas do eza — consultar `eza --color-help` ou a documentação oficial. As duas variáveis coexistem: `LS_COLORS` serve ao `ls` e outros; `EZA_COLORS` só ao eza.

## Na prática

### Setup básico

Aliases sugeridos no shell init (`.zshrc` ou equivalente):

```bash
alias ls='eza --group-directories-first'
alias ll='eza -l --git --group-directories-first'
alias la='eza -lah --git --group-directories-first'
alias lt='eza --tree -L 2'
```

Para ativar ícones automaticamente:

```bash
export EZA_ICONS_AUTO=1
```

### Receitas

```bash
# Long format com status git inline
eza -l --git

# Árvore até profundidade 3, respeitando .gitignore
eza --tree -L 3 --git-ignore

# Ordenar por tamanho decrescente (maior primeiro)
eza -l --sort=size -r

# Color-scale por idade (mais antigo = mais colorido)
eza -l --color-scale=age

# Pipeline com ripgrep: listar só .rs
eza -l | rg '\.rs$'

# Listar com header de colunas (útil pra entender o output)
eza -lh --header
```

### Quando eza vence ls

- Inspeção visual rápida em pastas com muitos arquivos de tipos diferentes.
- Ver git status sem rodar `git status` — coluna inline por arquivo.
- Árvore de diretório sem precisar instalar `tree`.
- Comparar tamanhos ou idades visualmente com `--color-scale`.
- Distinguir tipos de arquivo instantaneamente com ícones (Nerd Font presente).

### Quando ls clássico vence

- Scripts portáveis POSIX — `ls` está disponível em qualquer Unix.
- CI e ambientes minimalistas — eza pode não estar instalado.
- Compatibilidade exata de flags com ls(1) em scripts legados — eza difere.
- Performance em pastas com dezenas de milhares de arquivos — eza tem overhead por file (git status, metadados extras).

Versão hedged: eza 0.18+; verifique `eza --version` localmente.

## Armadilhas

### (1) Ícones aparecendo como `?` ou quadrados

**Causa:** ativar `--icons` sem Nerd Font configurada no emulador de terminal resulta em glyphs do Unicode Private Use Area (PUA) que o terminal não sabe renderizar.

**Sintoma:** `eza --icons` mostra `□` ou `?` onde deveriam estar os ícones.

**Como detectar:** trocar temporariamente a fonte do terminal para DejaVu Sans Mono (sem Nerd Font) — se os ícones quebram, confirma que eram Nerd Font.

**Solução:** instalar Nerd Font (MesloLGS NF, FiraCode NF, JetBrainsMono NF) e configurar no emulador de terminal (kitty, WezTerm, Alacritty, etc.). Ver verbete [[Dicionário do Terminal#Nerdfont|Nerd Font]].

### (2) `alias ls=eza` quebra scripts que esperam flags ls(1) clássicos

**Causa:** scripts de CI, Makefiles ou automações podem usar `ls -la` esperando o formato exato do GNU ls — parsing de output fixo, flags específicas, separadores de coluna. eza tem layout de output diferente.

**Sintoma:** script funciona em CI (sem alias) e falha localmente (com alias ativo).

**Como detectar:** testar o script com `\ls -la` (backslash bypassa alias) — se funciona, o alias é o culpado.

**Solução:** limitar alias ao contexto interativo:

```bash
if [[ -t 1 ]]; then
  alias ls='eza --group-directories-first'
fi
```

Ou preservar `ls` puro e usar nome diferente (`alias l=eza`) para o eza.

### (3) `--git` lento em repos grandes

**Causa:** a flag `--git` busca o status git de cada arquivo individualmente. Em monorepos com milhares de arquivos, isso custa tempo perceptível.

**Sintoma:** `eza -l --git` claramente mais lento que `eza -l` no mesmo diretório.

**Como detectar:** `time eza -l --git` vs `time eza -l` — diferença >1s é sinal.

**Solução:** remover `--git` do alias `ll` default e criar alias específico pra quando precisar:

```bash
alias ll='eza -l --group-directories-first'
alias llg='eza -l --git --group-directories-first'
```

### (4) Ordenação default ≠ ls com group-dirs-first

**Causa:** aliases que ativam `--group-directories-first` por padrão produzem ordem visual diferente do `ls` clássico (diretórios primeiro, depois arquivos, cada grupo em ordem alfabética). Quem alterna entre os dois pode se perder.

**Sintoma:** ordem de listagem confusa ao comparar `eza` e `ls` lado a lado.

**Como detectar:** `eza` vs `ls` no mesmo diretório — diretórios em posição diferente.

**Solução:** decidir convenção (group-dirs-first é a mais comum) e documentar nos dotfiles para consistência.

### (5) `EZA_COLORS` ≠ `LS_COLORS` (sintaxe diferente)

**Causa:** copiar o valor de `LS_COLORS` (gerado pelo `dircolors`) para `EZA_COLORS` não funciona — as chaves são distintas. eza usa chaves próprias (`di`, `fi`, `ex`, `ur`, `gm`, etc.); ls usa chaves do GNU dircolors com superposição parcial mas sem compat total.

**Sintoma:** cores não aplicam ou aplicam errado após copiar `LS_COLORS`.

**Como detectar:** `echo $LS_COLORS` vs `echo $EZA_COLORS` — formatos parecem iguais mas chaves divergem em campos específicos.

**Solução:** ler `eza --color-help` para as chaves válidas do eza e montar `EZA_COLORS` separadamente.

### (6) eza vs exa — confundir documentação antiga

**Causa:** muitos tutoriais publicados antes de agosto de 2023 referenciam `exa` — instalação via `brew install exa`, `apt install exa`, etc. O projeto exa está arquivado; o pacote pode estar desatualizado ou ausente.

**Sintoma:** `brew install exa` falha ou instala versão antiga de 2022; binário não tem features novas.

**Como detectar:** `exa --version` mostrando data de 2022 ou anterior confirma que é o projeto arquivado.

**Solução:** instalar sempre eza (`brew install eza`, `cargo install eza`, `apt install eza` em Ubuntu 24.04+). As flags são quase 100% compatíveis — migração trivial.

## Em inglês

Termos técnicos que aparecem ao ler docs e fóruns sobre eza:

- **listagem** — *listing*. "eza produz uma listing colorida por tipo de arquivo, com metadados opcionais."
- **formato longo** — *long format*. "O long format (`eza -l`) exibe permissões, owner, tamanho e data de modificação."
- **arquivo oculto** — *hidden file*. "Hidden files têm nome começando com `.`; visíveis com `eza -a`."
- **visualização em árvore** — *tree view*. "A tree view (`eza --tree`) exibe o diretório de forma hierárquica recursiva."
- **status git** — *git status*. "A flag `--git` adiciona uma coluna de git status inline por arquivo."
- **ícones** — *icons*. "eza suporta icons por tipo de arquivo quando uma Nerd Font está configurada no terminal."
- **escala de cores** — *color scale*. "O color scale aplica gradiente de cor proporcional ao tamanho ou idade do arquivo."
- **derivação** — *fork*. "eza é um fork ativo do exa, que foi arquivado em agosto de 2023."
- **arquivado** — *archived*. "O projeto exa está archived — sem novos releases ou correções de segurança."
- **lexicográfico** — *lexicographic*. "Lexicographic sort ordena por valor de caractere Unicode, como em dicionário."

## Veja também

- [[02 - ripgrep e fd — buscar conteúdo e nomes]] — `fd -t d` lista pastas com semântica própria
- [[03 - bat — cat moderno com syntax highlight]] — par natural na "stack moderna"
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#eza|eza]]
- [[Dicionário do Terminal#exa (legado)|exa (legado)]]
- [[Dicionário do Terminal#EZA_COLORS|EZA_COLORS]]
- [[Dicionário do Terminal#Nerdfont|Nerd Font]]
- [[Dicionário do Terminal#gitignore-aware|gitignore-aware]] — `--git-ignore` em eza

## Referências

- eza repo: https://github.com/eza-community/eza
- eza manpage: https://github.com/eza-community/eza/blob/main/man/eza.1.md
- exa (arquivado): https://the.exa.website/
