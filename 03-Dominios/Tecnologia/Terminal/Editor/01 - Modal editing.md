---
title: "Modal editing"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - modal-editing
  - neovim
aliases:
  - Modal editing
  - Modos do Vim
---

# Modal editing

> [!abstract] TL;DR
> Vim/Neovim separa edição em modos. No modo normal você não digita texto — você comanda. No modo insert você digita. Essa separação transforma edição em uma linguagem de operadores + alvos, e é o que multiplica velocidade. Entender modos é o pré-requisito para tudo no Neovim.

## O que é / Como funciona

Editores como VS Code e IntelliJ são **não-modais**: cada tecla que você pressiona ou insere um caractere ou aciona um atalho modificado (`Ctrl+`, `Alt+`). O teclado tem um único papel de cada vez.

Vim/Neovim são **modais**: o editor opera em **modos distintos**, e o significado de cada tecla depende do modo ativo. No **modo normal**, `d` não insere a letra "d" — ela é o operador *delete*. No **modo insert**, `d` insere a letra "d". A mesma tecla, semântica radicalmente diferente.

### Os 7 modos principais

| Modo | Como entrar | Indicador no statusline (LazyVim) |
|---|---|---|
| **Normal** | `<Esc>` de qualquer modo | `NORMAL` |
| **Insert** | `i`, `a`, `o`, `O`, `I`, `A` | `-- INSERT --` |
| **Visual (char)** | `v` | `-- VISUAL --` |
| **Visual-line** | `V` | `-- VISUAL LINE --` |
| **Visual-block** | `<C-v>` | `-- VISUAL BLOCK --` |
| **Command-line** | `:` (do normal) | prompt `:` na statusline |
| **Terminal** | `:terminal` ou `<leader>ft` no LazyVim | `-- TERMINAL --` |

> [!note] Há outros modos especializados (replace, select, ex, etc.), mas os 7 acima cobrem 99% do uso diário.

### Filosofia: Vim como linguagem

A frase canônica da comunidade é: **"Vim is a language."** Editores não-modais exigem que você memorize atalhos avulsos. No Vim/Neovim, você aprende:

- **Verbos (operadores):** `d` (delete), `c` (change), `y` (yank/copy), `>` (indent), `=` (format)…
- **Substantivos (motions/text objects):** `w` (word), `b` (word back), `e` (end of word), `$` (fim de linha), `iw` (inner word), `ap` (around paragraph), `i"` (dentro de aspas duplas)…

Compõe-se: `dw` = delete word, `ci"` = change inner quotes, `yap` = yank around paragraph. Aprender 10 operadores e 20 motions dá acesso combinatório a centenas de operações — sem memorizar atalhos específicos.

O modo normal é o **espaço de composição**: você articula operações. Modo insert é a exceção — usado apenas enquanto digita texto novo.

### Identificação visual no LazyVim

O tema padrão do LazyVim (Tokyonight) exibe o modo atual no canto esquerdo da statusline com cores distintas:

- **Normal:** texto `NORMAL`, cor azul/roxa
- **Insert:** texto `INSERT`, cor verde
- **Visual:** texto `VISUAL` / `V-LINE` / `V-BLOCK`, cor laranja
- **Command:** o prompt `:` aparece na command-line (linha inferior)
- **Terminal:** texto `TERMINAL`, cor cinza

Se o statusline não estiver visível, `:set showmode` exibe o indicador de modo na linha de comando. LazyVim já habilita isso por padrão.

## Na prática

### Entrar em modo insert

A partir do modo normal:

```
i     → insert antes do cursor
a     → insert após o cursor (append)
I     → insert no início da linha (primeiro caractere não-branco)
A     → insert no fim da linha
o     → abre linha abaixo e entra em insert
O     → abre linha acima e entra em insert
```

Casos de uso típicos: `i` para editar no ponto exato, `A` para completar o fim de uma linha, `o` para adicionar linha abaixo sem mover o cursor manualmente.

### Sair de qualquer modo

```
<Esc>     → volta ao modo normal (universal)
<C-[>     → equivalente exato a <Esc>, frequentemente mais rápido em layouts ANSI
<C-c>     → aborta a operação atual e volta ao normal (cuidado: não dispara autocomandos de InsertLeave)
```

> [!tip] A maioria dos usuários experientes mapeia `<C-[>` ou cria um mapa custom (`jk`, `jj`) para sair do insert sem mover a mão até o `<Esc>`. LazyVim **não** define esses mapas por padrão — evite copiar dotfiles alheios sem verificar isso.

### Modo visual

```
v        → visual char: seleciona caractere a caractere
V        → visual line: seleciona linhas inteiras
<C-v>    → visual block: seleciona colunas (útil para editar múltiplas linhas em paralelo)
```

No visual block, `I` insere texto no início de todas as linhas selecionadas; `A` insere no fim. Padrão observado em LazyVim para adicionar comentários em bloco ou prefixos de coluna.

### Modo command-line

```
:        → abre o prompt de command-line (do normal)
<Esc>    → cancela e fecha o prompt
<CR>     → executa o comando
```

Exemplos: `:w` (salvar), `:q` (fechar), `:s/foo/bar/g` (substituir).

### Verificar o modo atual

Quando em dúvida sobre em qual modo você está:

```
:set showmode    → exibe o modo na command-line (já habilitado no LazyVim)
```

Olhe a statusline (canto inferior esquerdo). O LazyVim usa cores diferentes por modo — normal é azul/roxo, insert é verde, visual é laranja. Se a statusline não aparecer, `:messages` mostra o histórico de mensagens recentes.

### Ciclo de edição mais comum

```
[Normal] → ciw → [Insert] digita novo conteúdo → <Esc> → [Normal]
```

`ciw` = *change inner word*: apaga a palavra sob o cursor e entra em insert. Você digita o substituto e volta ao normal. Esse padrão (normal → operador → insert → `<Esc>`) é o loop fundamental do Vim.

Outro ciclo frequente com navegação:

```
[Normal] → w (avança palavra) → cw → [Insert] digita → <Esc> → . (repete)
```

O `.` (dot) repete a última operação de change — multiplicador silencioso de produtividade.

## Armadilhas

### 1. "Por que minhas letras viraram comandos?"

**Sintoma:** você digita `dd` e a linha desaparece; digita `w` e o cursor pula uma palavra. O buffer parece enlouquecido.

**Causa:** você está em modo normal e esqueceu de entrar em insert.

**Diagnóstico:** olhe o statusline. Se mostrar `NORMAL` (ou nada), você não está em insert.

**Solução:** pressione `i` ou `a` para entrar em insert, ou `u` para desfazer as mudanças acidentais antes de continuar.

> [!warning] Esse é o erro mais comum de quem abre o Neovim pela primeira vez. A transição mental de "teclado sempre digita" para "teclado comanda por padrão" leva alguns dias.

### 2. Mapeamento `jk`/`jj` copiado de dotfiles alheios

**Cenário:** você copiou a config de alguém que mapeou `jj` ou `jk` para `<Esc>`. No terminal, isso introduz um *delay* perceptível de 100-1000ms toda vez que você digita `j` (o editor espera para ver se vem outro `j`/`k`).

**LazyVim default:** não define esses mapas. `<Esc>` e `<C-[>` funcionam sem delay.

**Solução:** se quiser o mapa, ajuste `timeoutlen` para um valor baixo (e.g., `vim.o.timeoutlen = 300`) e avalie o trade-off. Não copie dotfiles inteiros sem ler.

### 3. Modo terminal: `<Esc>` não sai do modo

**Cenário:** você abre `:terminal` dentro do Neovim (ou usa `<leader>ft`). Pressiona `<Esc>` esperando voltar ao normal. O `<Esc>` é enviado ao processo terminal (e.g., fecha o prompt do shell), não ao Neovim.

**Causa:** no modo terminal do Neovim, as teclas são repassadas ao processo filho. `<Esc>` tem significado para o shell/programa, não para o Neovim.

**Solução:** para voltar ao modo normal do Neovim a partir do terminal embutido, use:

```
<C-\><C-n>    → sai do modo terminal e vai para normal
```

LazyVim mapeia isso por padrão. Confirme com `:nmap <C-\>` se necessário.

## Em inglês

- **modo** — *mode*. "Press `Esc` to return to **normal mode** before issuing any motion or operator."
- **modo normal** — *normal mode*. "In **normal mode**, every keystroke is a command — nothing is inserted into the buffer."
- **modo de inserção** — *insert mode*. "You enter **insert mode** to type text; exit it as soon as you're done."
- **modo visual** — *visual mode*. "Select a block of code in **visual mode** before applying an operator like `d` or `>`."
- **modo de comando** — *command-line mode*. "Open **command-line mode** with `:` to run Ex commands like `:w` or `:s`."
- **entrar em** — *enter*. "Use `i` to **enter** insert mode at the cursor position."
- **sair de** — *exit / leave*. "Press `<Esc>` to **exit** insert mode and return to normal."
- **edição modal** — *modal editing*. "**Modal editing** separates navigation and text manipulation from text insertion."
- **digitar** — *type*. "**Type** your changes in insert mode, then press `Esc` to return to normal."
- **comandar** — *command*. "In normal mode, you **command** the editor — moves, deletions, and transformations are all keystrokes."

## Veja também

- [[02 - Motions, operadores e text objects]]
- [[03 - Edição e navegação]]
- [[04 - LazyVim tour]]
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Modal editing|modal editing]]
- [[Dicionário do Terminal#Modo|modo]]

## Referências

- [Neovim user intro](https://neovim.io/doc/user/intro.html)
- `:Tutor` (vimtutor embutido no Neovim)
- [Learn Vim — irian.to](https://learnvim.irian.to/)
- [Practical Vim — Drew Neil](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
- [Boost your fu (Barbarian Meets Coding)](https://www.barbarianmeetscoding.com/boost-your-coding-fu-with-vscode-and-vim)
