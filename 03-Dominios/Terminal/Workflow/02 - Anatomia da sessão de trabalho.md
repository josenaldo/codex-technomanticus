---
title: "Anatomia da sessão de trabalho"
created: 2026-05-24
updated: 2026-05-24
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - workflow
  - iniciado
  - sessao
aliases:
  - Anatomia da sessão
  - Sessão de trabalho
---

# Anatomia da sessão de trabalho

> [!abstract] TL;DR
> Sessão de trabalho = container persistente de tabs/panes/processos. Vocabulário: session (root), tab (área visível), pane (split dentro de tab), layout (config declarativa). Zellij/tmux atuam como window manager do terminal. Dois modelos principais: sessão = projeto (uma sessão por repo) ou sessão = task (uma sessão por feature). Sessions efêmeras (descartáveis, sem nome) vs persistentes (nomeadas, sobrevivem reboot e desconexão SSH).

## O que é / Como funciona

### Sessão, tab, pane, layout — vocabulário

A hierarquia canônica:

- **session** — raiz do container. Tem nome humano (`projeto`) ou ID anônimo. Persiste após detach. Pode ser listada, reattachada, destruída.
- **tab** — área visível única dentro da sessão. Navegável via `leader+número`. Cada tab ocupa 100% da tela.
- **pane** — split dentro de uma tab. Divide o espaço horizontal ou vertical. Cada pane roda um processo independente.
- **layout** — declaração KDL (Zellij) ou conf (tmux) que reproduz a estrutura de tabs+panes ao abrir uma sessão. Torna o setup reproduzível.

Regra mnemônica: `session > tab > pane`. Confundir os níveis é a armadilha mais comum em docs e forums.

### Window manager mental model

Zellij e tmux atuam como window managers para o terminal — o mesmo papel que i3, Sway ou Openbox exercem pra GUIs.

Implicações práticas:

- Um único terminal hospedeiro pode rodar N sessões simultâneas.
- Múltiplas máquinas (SSH) podem compartilhar a mesma sessão remota.
- O processo supervisor sobrevive ao fechamento do emulator (iTerm, Alacritty, Kitty…).
- Fechar a janela do emulator ≠ matar a sessão — ela continua rodando em background.

Em `myproj`, alice roda `zellij -s myproj` no servidor. Bob faz SSH e `zellij a myproj`. Ambos veem o mesmo estado.

### Sessions efêmeras vs persistentes

**Efêmera** (sem nome):

```bash
zellij          # nova sessão com ID anônimo (ex: "teal-lion")
```

- Some ao detach final ou kill explícito.
- Use pra one-shot tasks: checar um log remoto, rodar um script rápido.
- Nenhum investimento em nome/organização.

**Persistente** (named):

```bash
zellij -s projeto
```

- Sobrevive desconexão SSH, sleep da máquina, exit do emulator.
- Pode ser reattachada dias depois no mesmo estado.
- Use pra qualquer trabalho que vai continuar amanhã.

Regra simples: se vai voltar a essa sessão, dê um nome.

### Modelos de organização

**Sessão = projeto** (recomendado pra monorepo / trabalho contínuo):

- Uma sessão por repositório.
- Tabs por contexto: `code`, `server`, `tests`, `db`, `logs`.
- Estado persiste entre dias; acorda direto onde parou.
- Risco: sessão acumula entropia ao longo de semanas.

**Sessão = task** (recomendado pra multi-feature / worktrees):

- Uma sessão por feature ou branch.
- Mapeia 1:1 com git worktrees.
- Fácil de destruir ao terminar a task.
- Veja [[07 - Worktrees + Zellij paralelos]] pra detalhes.

**Sessão = papel** (menos comum):

- Uma sessão `dev`, uma `ops`, uma `review`.
- Útil quando os contextos têm ferramentas muito diferentes.

### Modo focus

Esconde a UI auxiliar (status bar, tabs bar) pra maximizar área de código.

| Multiplexer | Comando         | Atalho default |
|-------------|-----------------|----------------|
| Zellij      | sem comando CLI | `Alt-f`        |
| tmux        | `set status off` | — (bind custom) |

Útil em: deep work, pair-programming, screencasts, apresentações. Não muda o estado da sessão — só o rendering.

## Na prática

### Comandos básicos — Zellij

```bash
# Criar sessão
zellij                      # nova efêmera (ID anônimo)
zellij -s myproj            # nova nomeada

# Listar e conectar
zellij ls                   # listar sessões ativas
zellij a myproj             # attach à sessão existente
zellij a -c myproj          # attach ou cria se não existir

# Sair e destruir
zellij d                    # detach (sessão continua rodando)
zellij k myproj             # kill sessão pelo nome
```

Para tmux a nomenclatura muda (`new-session`, `attach-session`, `kill-session`) mas o modelo mental é o mesmo.

### Quantos tabs e panes são saudáveis

**Tabs**: 3-5 por sessão. Acima de 5 a navegação por número começa a falhar (ninguém lembra o que tem no tab 7).

**Panes**: 2-4 por tab. Acima de 4 panes visíveis ao mesmo tempo vira poluição visual — use tabs extras em vez de mais splits.

**Regra do processo persistente**: cada pane deve ter um processo que justifica ficar aberto (`dev server`, `watch tests`, shell interativo). Panes com comandos já finalizados devem ser fechados.

### Escolher o modelo certo

| Situação | Modelo recomendado |
|---|---|
| Trabalho longo em monorepo | sessão = projeto |
| Múltiplas features paralelas | sessão = task + worktrees |
| Job exploratória / one-shot | efêmera |
| Ambientes muito distintos | sessão = papel |

Para `myproj` com alice trabalhando em 3 features simultâneas: `zellij -s feat/auth`, `zellij -s feat/payments`, `zellij -s feat/notifications` — cada uma com seu worktree.

## Armadilhas

1. **Confundir sessão com tab/pane no vocabulário**

**Causa:** Zellij e tmux usam terminologia parecida mas não idêntica; iniciante frequentemente chama tab de "janela" ou "window".

**Sintoma:** Comandos não funcionam como esperado; leitura de docs e forums fica confusa porque os termos se misturam.

**Como detectar:** Testar `zellij --help` e observar a saída; ler a seção de nomenclatura da doc oficial. Se você chama tab de "window" você está usando terminologia tmux em contexto Zellij.

**Solução:** Memorizar a hierarquia `session > tab > pane` e usar esses termos consistentemente. Session é raiz; tab é área visível; pane é split dentro de tab. Só tmux usa o termo "window" (equivalente a tab no Zellij).

---

2. **Acumular sessões persistentes "esquecidas"**

**Causa:** Hábito de detach sem nunca destruir; nunca rodar `zellij ls` pra auditar o que está ativo.

**Sintoma:** `zellij ls` mostra 10-15 sessões com nomes que você não reconhece; RAM consumida por processos zumbi; confusion ao fazer `a -c` e attachar em sessão errada.

**Como detectar:** Rodar `zellij ls` e contar. Se há sessões com mais de 7 dias sem uso, você tem acúmulo.

**Solução:** Higiene semanal: `zellij ls` + kill sessões inativas há mais de 7 dias com `zellij k <nome>`. Alternativa: convenção de nomenclatura com data (`zellij -s feat-auth-0524`) facilita identificação.

---

3. **Sessão efêmera para trabalho que vai durar dias**

**Causa:** Começar com `zellij` sem `-s` por hábito; não perceber que a sessão não tem nome.

**Sintoma:** Na segunda-feira de manhã o estado da sexta-feira sumiu. Precisa reabrir todos os tabs, reiniciar todos os servidores, reconfigurar o ambiente.

**Como detectar:** Notar que toda segunda você refaz os mesmos passos de setup. Verificar com `zellij ls` — se a sessão aparece como nome aleatório (ex: `teal-lion`) é efêmera.

**Solução:** Se vai voltar amanhã, use `-s nome` desde o início. Custo: 5 caracteres extras. Benefício: estado persiste indefinidamente.

---

4. **Layout KDL gigante tentando reproduzir tudo automaticamente**

**Causa:** Vontade de ter "setup completo num único comando"; tentar colocar `command` em cada pane dentro do layout.

**Sintoma:** Layout com 50+ linhas; qualquer mudança de projeto quebra o layout; tempo gasto mantendo o arquivo supera o tempo economizado; comandos auto-start falham silenciosamente.

**Como detectar:** Abrir o layout e contar linhas. Se tem mais de 20 linhas ou blocos `command {}` em cada pane, está complexo demais.

**Solução:** Layout mínimo — declara 3-4 tabs com nomes, sem comandos auto-start. Abertura manual dos processos é aceitável e mais robusta. Layout serve pra estrutura, não pra automação completa.

## Em inglês

- **session** — *session*. "Criar uma nova sessão nomeada: `zellij -s myproj`."
- **tab** — *tab*. "Cada tab ocupa 100% da área visível da sessão."
- **pane** — *pane*. "Divida o pane horizontalmente com `Alt-n`."
- **layout** — *layout*. "O layout KDL declara a estrutura inicial de tabs e panes."
- **attach** — *attach*. "Fazer attach em uma sessão existente retoma exatamente onde você parou."
- **detach** — *detach*. "Fazer detach desconecta sem destruir a sessão."
- **focus mode** — *focus mode*. "O focus mode esconde a status bar pra maximizar o espaço de código."
- **window manager** — *window manager*. "Zellij atua como window manager do terminal."
- **ephemeral** — *ephemeral*. "Uma sessão efêmera é descartada ao fazer o detach final."
- **persistent** — *persistent*. "Sessões persistentes sobrevivem a reboots e desconexões SSH."

## Veja também

- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[04 - Setup matinal e tear-down]]
- [[07 - Worktrees + Zellij paralelos]]
- [[03-Dominios/Terminal/Multiplexer/02 - Modelo mental — sessions, tabs, panes|Modelo mental Multiplexer]]
- [[03-Dominios/Terminal/Multiplexer/04 - Sessões persistentes — detach, attach, gerenciamento|Sessões persistentes (galho 3)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#named session|named session]]
- [[Dicionário do Terminal#ephemeral session|ephemeral session]]
- [[Dicionário do Terminal#focus mode|focus mode]]
- [[Dicionário do Terminal#sessão de trabalho|sessão de trabalho]]

## Referências

- Zellij sessions: https://zellij.dev/documentation/sessions
- Zellij layouts: https://zellij.dev/documentation/layouts
