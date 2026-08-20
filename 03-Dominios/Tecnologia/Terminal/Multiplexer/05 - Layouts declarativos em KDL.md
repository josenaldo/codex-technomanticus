---
title: "Layouts declarativos em KDL"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - multiplexer
  - zellij
  - adepto
  - layouts
  - kdl
aliases:
  - Layouts Zellij
  - KDL Zellij
---

# Layouts declarativos em KDL

> [!abstract] TL;DR
> Layouts Zellij são arquivos KDL que descrevem tabs/panes/splits/cwd/comando. KDL é uma linguagem declarativa: nó propriedade=valor { child }. `default_layout "<nome>"` no config aplica auto; `zellij --layout <nome>` aplica ad-hoc. Layouts vivem em `~/.config/zellij/layouts/<nome>.kdl`. Versioná-los nos dotfiles = setup repetível.

---

## O que é / Como funciona

### KDL — sintaxe mínima

KDL (KDL Document Language, pronunciado "cuddle") é uma linguagem de configuração declarativa com sintaxe humana. Nó = nome + propriedades opcionais + children opcionais entre `{}`.

```kdl
// Comentário de linha
/* Comentário de bloco */

// Nó simples sem filhos
pane

// Nó com propriedade
pane size=10

// Nó com children (entre {})
tab name="dev" {
    pane split_direction="vertical" {
        pane
        pane
    }
}

// String com aspas — obrigatória quando contém espaços
pane command="nvim"
pane cwd="~/repos/myproj"
```

Destaques de sintaxe:
- Sem aspas obrigatórias em valores simples (`size=10`, `borderless=true`).
- Comentários de linha (`//`) e bloco (`/* */`) são nativos — ausentes em JSON.
- Booleans são `true`/`false` (KDL v1, que o Zellij usa). KDL v2 introduziu `#true`/`#false`, mas o Zellij ainda segue v1.
- Sem vírgulas entre propriedades — separação por espaço.

### Estrutura de layout Zellij

O nó raiz é sempre `layout {}`. Dentro dele, `tab {}` define abas; dentro de tab, `pane {}` define divisões.

```kdl
layout {
    tab name="editor" {
        pane split_direction="vertical" {
            pane size="80%"
            pane size="20%" {
                pane
                pane
            }
        }
    }
    tab name="logs" {
        pane command="tail" {
            args "-f" "/var/log/syslog"
        }
    }
}
```

### Propriedades de pane mais usadas

| Propriedade | Tipo | Exemplo | Quando usar |
|---|---|---|---|
| `command` | string | `command="nvim"` | Executar comando ao abrir o pane |
| `args` | nó filho | `args "-f" "log"` | Argumentos do comando |
| `cwd` | path | `cwd="~/myproj"` | Working directory do pane |
| `size` | string/int | `size="50%"` ou `size=10` | Tamanho relativo ou fixo em linhas/colunas |
| `split_direction` | string | `split_direction="vertical"` | Como splittar panes filhos |
| `borderless` | bool | `borderless=true` | Remove borda visível do pane |
| `focus` | bool | `focus=true` | Pane que começa em foco ao abrir |
| `name` | string | `name="editor"` | Nome exibido do pane |
| `edit` | path | `edit="src/main.rs"` | Abrir arquivo em editor embutido |

### Floating panes em layout

Floating panes ficam sobrepostos ao grid, definidos fora dos `tab {}` no nó `floating_panes {}`.

```kdl
layout {
    tab {
        pane
    }
    floating_panes {
        pane {
            x "20%"
            y "20%"
            width "60%"
            height "60%"
            command "btop"
        }
    }
}
```

### Stacked panes

Stacked panes empilham múltiplos panes num mesmo espaço — um expandido, os demais reduzidos a barra de título.

```kdl
layout {
    pane stacked=true {
        pane name="server"
        pane name="db"
        pane name="cache"
    }
}
```

### default_layout

Configurado em `~/.config/zellij/config.kdl`:

```kdl
// Aplicar layout built-in
default_layout "compact"

// Ou aplicar layout customizado (arquivo em ~/.config/zellij/layouts/)
default_layout "dev"
```

Layouts built-in disponíveis:

| Nome | Descrição |
|---|---|
| `default` | Layout padrão com status bar completa |
| `compact` | Layout compacto com barra menor |
| `strider` | Inclui file explorer lateral (plugin strider) |
| `disable-status-bar` | Sem status bar |

Layouts customizados ficam em `~/.config/zellij/layouts/<nome>.kdl` e são acessados pelo nome (sem extensão).

---

## Na prática

### Template "dev" — editor + shell + watcher

Arquivo `~/.config/zellij/layouts/dev.kdl`:

```kdl
layout {
    tab name="code" {
        pane split_direction="vertical" {
            pane size="70%" {
                pane command="nvim" focus=true
            }
            pane size="30%" {
                pane name="shell"
                pane name="watch" command="npm" {
                    args "run" "dev"
                }
            }
        }
    }
    tab name="git" {
        pane command="lazygit"
    }
}
```

Carregar:

```bash
zellij --layout dev
```

Resultado: 2 tabs — `code` com split 70/30 (nvim + shell/watcher) e `git` com lazygit.

### Template "monitor" — observabilidade

Arquivo `~/.config/zellij/layouts/monitor.kdl`:

```kdl
layout {
    tab name="monitor" {
        pane split_direction="horizontal" {
            pane command="btop"
            pane command="journalctl" {
                args "-f" "-n" "50"
            }
        }
    }
}
```

Dividido horizontalmente: recursos do sistema em cima, logs em baixo.

### Versionar layouts

Layouts são arquivos de texto — candidatos naturais a versionamento em dotfiles.

Estratégia recomendada: symlink da pasta de layouts para o repo de dotfiles.

```bash
# Estrutura no repo de dotfiles:
# dotfiles/
#   zellij/
#     layouts/
#       dev.kdl
#       monitor.kdl

# Symlink:
ln -s ~/repos/dotfiles/zellij/layouts ~/.config/zellij/layouts
```

Cada mudança nos layouts entra num commit nos dotfiles. Novo ambiente = clone + symlink = setup idêntico em segundos.

> [!note]
> O galho 5 desta trilha (Dotfiles, planejado) cobre estratégias completas de symlink e GNU Stow para gerenciar dotfiles como repositório. Por enquanto, o symlink manual acima é suficiente.

---

## Armadilhas

### (1) Esquecer aspas em comandos com espaço

**Causa:** KDL tolera valores sem aspas para strings simples, mas espaço inicia um novo token. `command=npm run dev` faz o parser ler `npm` como valor e `run`/`dev` como argumentos posicionais do nó — não do comando.

**Sintoma:** pane abre mas comando falha com erro de argumento inesperado, ou o shell recebe o comando errado.

**Como detectar:** `zellij --layout dev` e observar o pane — shell abre em vez do processo esperado, ou processo morre imediatamente com erro.

**Solução:** `command="npm"` + nó filho `args "run" "dev"` separados. Cada argumento é um valor posicional no nó `args`.

---

### (2) `cwd` sem expansão de `~`

**Causa:** algumas versões do Zellij não expandem `~` em `cwd`. O til é tratado como caractere literal no path.

**Sintoma:** pane abre no diretório atual do processo Zellij em vez do caminho configurado; ou erro "no such file or directory".

**Como detectar:** dentro do pane, `pwd` retorna um path diferente do esperado.

**Solução:** usar path absoluto (`cwd="/home/user/myproj"`) ou variável de ambiente (`cwd="$HOME/myproj"`) — mas confirme que a versão suporta a expansão. Path absoluto é o mais seguro.

---

### (3) Percentuais de `size` não somam 100

**Causa:** Zellij não normaliza automaticamente percentuais de panes filhos. Se dois panes têm `size="60%"` e `size="60%"`, a soma é 120% — comportamento é indefinido ou o layout quebra.

**Sintoma:** layout abre com sobreposição visual, panes muito pequenos ou erro de renderização.

**Como detectar:** somar manualmente os `size` dos panes irmãos — devem totalizar 100%. Ou comparar a aparência com o esperado.

**Solução:** somar exatamente 100% (`size="70%"` + `size="30%"`), ou usar tamanhos fixos (`size=20`) para panes de tamanho definido e deixar os outros sem `size` (ocupam o restante).

---

### (4) `focus=true` em mais de um pane por tab

**Causa:** cada tab deve ter no máximo 1 pane com `focus=true`. Com múltiplos panes marcados, Zellij escolhe qual recebe foco — e a escolha pode não ser determinística.

**Sintoma:** o pane que abre em foco não é o esperado; comportamento inconsistente entre carregamentos do layout.

**Como detectar:** buscar `focus=true` no arquivo KDL — deve aparecer no máximo 1 vez por `tab {}`.

**Solução:** garantir exatamente 1 `focus=true` por tab no layout. Se nenhum pane tiver `focus=true`, o Zellij escolhe o primeiro.

---

### (5) Layout customizado não carrega

**Causa:** pode ter múltiplas origens: arquivo fora da pasta `layouts/`, nome com `.kdl` na config (deve ser sem extensão), ou erro de sintaxe KDL que impede o parse.

**Sintoma:** `zellij --layout mydev` falha com "layout not found" ou abre o layout default sem aviso.

**Como detectar:** 
```bash
# Verificar se o arquivo existe com o nome correto
ls ~/.config/zellij/layouts/

# Verificar paths de config dir, cache dir e versão do Zellij
zellij setup --check
```

> [!warning] `zellij setup --check` não valida sintaxe KDL
> O comando verifica apenas paths de config dir, cache dir e versão instalada — não parseia layouts. Para validar a sintaxe do arquivo KDL, abra-o num editor com syntax highlighting (LSP de KDL, se disponível, ou highlight básico no Vim/VS Code) e/ou rode `zellij --layout <nome>` e observe o erro no stderr.

**Solução:** confirmar que o arquivo está em `~/.config/zellij/layouts/<nome>.kdl`; usar `default_layout "<nome>"` (sem `.kdl`) no config; abrir o arquivo KDL num editor com syntax highlighting (LSP de KDL, se disponível, ou highlight básico no Vim/VS Code) e/ou rodar `zellij --layout <nome>` e observar o erro no stderr.

---

## Em inglês

- **layout** — *layout*. "definição declarativa de tabs e panes em KDL, descrevendo toda a estrutura de uma workspace."
- **declarativo** — *declarative*. "estilo de config que descreve *o quê* deve existir, não *como* criar — contrário de imperativo."
- **imperativo** — *imperative*. "estilo de automação baseado em comandos sequenciais; ex: scripts shell que criam panes via CLI."
- **pane** — *pane*. "divisão interna de uma tab que roda um shell ou comando; unidade básica do layout."
- **split direction** — *split direction*. "eixo de divisão dos panes filhos: `vertical` (lado a lado) ou `horizontal` (um acima do outro)."
- **floating** — *floating*. "pane sobreposto ao grid, posicionado livremente por coordenadas x/y."
- **stacked** — *stacked*. "modo de empilhamento onde panes irmãos dividem o mesmo espaço; só um fica expandido."
- **cwd** — *cwd (current working directory)*. "diretório de trabalho inicial do pane; equivalente ao diretório no qual o shell abre."
- **template** — *template*. "layout pré-configurado para um caso de uso recorrente (dev, monitor, etc.), carregado por nome."
- **workspace** — *workspace*. "ambiente de trabalho completo — conjunto de tabs e panes para um contexto ou projeto."

---

## Veja também

- [[02 - Modelo mental — sessions, tabs, panes]]
- [[04 - Sessões persistentes — detach, attach, gerenciamento]]
- [[07 - Integração com Neovim e shell]]
- [[03-Dominios/Tecnologia/Terminal/Multiplexer/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#KDL|KDL]], [[Dicionário do Terminal#Layout (Zellij)|layout]]

---

## Referências

- [Zellij — Layouts](https://zellij.dev/documentation/layouts)
- [KDL spec](https://kdl.dev/)
