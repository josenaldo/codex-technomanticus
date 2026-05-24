---
title: "Setup matinal e tear-down"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - workflow
  - adepto
  - sessao
  - playbook
aliases:
  - Setup matinal
  - Tear-down
---

# Setup matinal e tear-down

> [!abstract] TL;DR
> Playbook: abrir o dia (setup matinal) e fechar o dia (tear-down) com sessões nomeadas Zellij. Setup: `zellij a -c projeto` com layout KDL → atuin import → lazygit em tab dedicada. Tear-down: `zellij d` (preserva estado) vs `zellij k` (descarte intencional). Hábito de ritual reduz fricção e perda de contexto entre dias.

## O que é / Como funciona

### Por que ritualizar

Ritualizar início e fim do dia de trabalho reduz decisões repetitivas ("por onde começo?") e preserva contexto entre dias sem depender de memória. O setup matinal é o sinal psicológico de que o trabalho começa; o tear-down, de que terminou. Sem ritual, o estado mental permanece aberto — dificulta descanso e reentrada.

Benefícios concretos:
- Menos decisões no começo do dia (layout, diretório, processos já definidos)
- Sessão nomeada preserva tabs, panes e processos entre dias
- Tear-down intencional evita acúmulo de sessões zombies consumindo RAM
- Limite claro entre trabalho e não-trabalho (higiene cognitiva)

### Setup matinal: passos

1. **Iniciar (ou reanexar) sessão nomeada** — `zellij a -c <projeto>` cria se não existe, anexa se já existe
2. **Restaurar layout** — se layout KDL foi persistido, ele abre automaticamente; senão, abrir tabs manualmente
3. **Sync atuin entre máquinas** — `atuin sync` propaga history do outro dispositivo (laptop/desktop)
4. **Abrir lazygit em tab dedicada** — tab `git` com `lazygit` já rodando dá visão imediata do estado do repo
5. **Foco em tab principal** — navegar para tab `code` e abrir o arquivo em que parou ontem

### Tear-down: passos

1. **Salvar tudo** — commitar WIP, ou pelo menos salvar buffers abertos no editor
2. **Decidir intenção** — continuar amanhã (detach) ou encerrar projeto/feature (kill)
3. **Detach** — `Ctrl-Q` dentro do Zellij (ou `zellij d` de fora); preserva estado completo
4. **Kill** — `zellij k <nome>` de fora; mata todos os processos da sessão
5. **Sync atuin final** — `atuin sync` para o outro dispositivo ter o history atualizado

### Detach vs kill

| Ação | Comando | Processos | Sessão sobrevive logout | Quando usar |
|------|---------|-----------|------------------------|-------------|
| Detach | `zellij d` (ou `Ctrl-Q`) | Continuam rodando | Sim | 90% do tempo — vai continuar amanhã |
| Kill | `zellij k <nome>` | Morrem | Não | Feature merged, projeto pausado, limpeza semanal |

Regra prática: **default é detach**. Kill exige intenção explícita.

## Na prática

### Layout KDL mínimo

Arquivo em `~/.config/zellij/layouts/projeto.kdl`:

```kdl
layout {
    default_tab_template {
        pane size=1 borderless=true {
            plugin location="zellij:tab-bar"
        }
        children
        pane size=2 borderless=true {
            plugin location="zellij:status-bar"
        }
    }

    tab name="code" focus=true {
        pane
    }

    tab name="git" {
        pane command="lazygit"
    }

    tab name="server" {
        pane
    }
}
```

Panes de `server` e `code` ficam **vazios** intencionalmente — comandos pesados são iniciados manualmente para evitar spike de CPU no boot da sessão.

### Setup matinal — receita

```bash
# Função no ~/.zshrc
work() {
    local proj="$1"
    cd "$(zoxide query "$proj")" || return 1
    zellij a -c "$proj" options --default-layout projeto
}

# Uso
work myproj
# Sessão "myproj" abre com 3 tabs (code/git/server)
# lazygit já roda em tab "git"
```

A função `work` combina três ações em um comando idempotente: navega para o diretório, cria a sessão se não existe, e aplica o layout. Chamar `work myproj` quando a sessão já existe simplesmente reanexar.

### Tear-down — receita

```bash
# Encerrar fluindo (preserva estado — default)
# Dentro do Zellij: Ctrl-Q

# Listar sessões antes de qualquer kill
zellij ls

# Kill intencional (descarta sessão e processos)
zellij k myproj
```

Hábito sexta-feira: rodar `zellij ls` e fazer kill nas sessões que não serão retomadas na semana seguinte.

### Multi-máquina (laptop + desktop)

[[03-Dominios/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync|atuin sync]] propaga history de comandos entre máquinas automaticamente. Sessões Zellij **não sincronizam** — cada máquina tem suas próprias sessões.

Convenção de nomes para evitar confusão mental:

```
laptop-myproj
desktop-myproj
desktop-myproj-hotfix
```

Prefixo da máquina deixa claro onde a sessão vive ao ler `zellij ls` de qualquer dispositivo via SSH.

## Armadilhas

1. **`zellij k` com trabalho não salvo** — Causa: hábito de "limpar" sessões antigas sem verificar o estado atual. Sintoma: edits abertos no nvim somem; pane com processo importante é destruído. Como detectar: antes de qualquer kill, fazer `zellij a <nome>` e checar tabs visualmente. Solução: detach como default; kill somente após attach + confirmação visual de que nada está aberto.

2. **Layout KDL com auto-start de comandos pesados** — Causa: querer "tudo pronto em 1 comando" no layout. Sintoma: `npm run dev`, `docker compose up` e servidor de banco iniciando simultaneamente trava o laptop no boot da sessão. Como detectar: spike de CPU imediatamente ao rodar `work myproj`. Solução: layout define apenas nomes de tabs e panes vazios; comandos pesados são iniciados manualmente na tab correta.

3. **Nomes de sessão genéricos que conflitam** — Causa: sempre usar `zellij -s work` ou `zellij -s dev` sem considerar projetos paralelos. Sintoma: `zellij a work` abre estado de outro projeto da semana passada. Como detectar: `zellij ls` mostra `work` mas você não lembra o que estava nessa sessão. Solução: usar o slug do repo como nome (`myproj`, `alice-api`) ou `<projeto>-<feature>` quando trabalhando em branches paralelas.

4. **Sessões esquecidas acumulando RAM** — Causa: fechar o laptop direto sem detach explícito (ou com detach mas nunca fazendo kill depois). Sintoma: após meses, `zellij ls` lista dezenas de sessões; `top` mostra zellij consumindo 1 GB+ de RAM. Como detectar: `zellij ls | wc -l` acima de 10 é sinal de acúmulo. Solução: ritual de sexta-feira — listar sessões, retomar e fazer kill nas que não voltam na próxima semana.

## Em inglês

- **Setup** — *setup*. "O setup matinal inicia a sessão nomeada e restaura o layout do dia anterior."
- **Tear-down** — *tear-down*. "O tear-down encerra a sessão de forma intencional, com detach ou kill."
- **Ritual** — *ritual*. "Ritualizar o início e fim do dia reduz decisões repetitivas."
- **Attach** — *attach*. "Fazer attach em uma sessão existente evita criar duplicatas com estado diferente."
- **Detach** — *detach*. "Detach preserva todos os processos e permite retomar amanhã exatamente onde parou."
- **Kill** — *kill*. "Kill descarta a sessão e mata todos os processos — use com intenção, não como default."
- **Layout** — *layout*. "Um layout KDL declarativo garante que as tabs certas abram na ordem certa."
- **Auto-start** — *auto-start*. "Evite auto-start de comandos pesados no layout para não travar o boot da sessão."
- **Idempotent** — *idempotent*. "A função `work` é idempotente: chamar duas vezes não cria duas sessões."
- **Multi-machine** — *multi-machine*. "Em configuração multi-machine, use prefixo de máquina no nome da sessão para evitar confusão."

## Veja também

- [[02 - Anatomia da sessão de trabalho]]
- [[07 - Worktrees + Zellij paralelos]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes|Sessões persistentes (galho 3)]]
- [[03-Dominios/Terminal/Multiplexer/05 - Layouts declarativos em KDL|Layouts KDL (galho 3)]]
- [[03-Dominios/Terminal/CLI Utils/06 - atuin — history shell com SQLite e sync|atuin (galho 6)]]
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#tear-down|tear-down]]
- [[Dicionário do Terminal#named session|named session]]

## Referências

- Zellij layouts: https://zellij.dev/documentation/layouts
- Zellij commands: https://zellij.dev/documentation/commands
