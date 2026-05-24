---
title: "Code review no terminal"
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
  - code-review
  - playbook
aliases:
  - Code review terminal
  - PR review
---

# Code review no terminal

> [!abstract] TL;DR
> Playbook: review de PR sem sair do terminal. `gh pr list` + `gh pr checkout <num>` → lazygit pra ver diff por arquivo → delta como pager pra cores ricas → nvim com anotações inline. Quando voltar pra UI web: threads longas, discussions, approvals coletivos. Vantagem do terminal: edita/testa enquanto revisa.

## O que é / Como funciona

### Por que review no terminal

A diferença fundamental entre revisar no browser e no terminal é que no terminal você **edita e testa o código durante a review** — não só lê. Isso muda a qualidade do feedback.

Outras vantagens:

- **Diff colorido superior**: delta renderiza syntax highlighting real, não só verde/vermelho.
- **Sem context-switch pro browser**: editor, terminal, diff, tudo no mesmo ambiente.
- **Funciona offline**: depois de `gh pr checkout`, o diff é local. Útil em viagens ou conexão ruim.
- **Integração com ferramentas locais**: roda os testes, abre o arquivo no editor, busca referências — tudo sem sair do workflow.

### Por que voltar pra web

O terminal não é superior em tudo. Prefira o browser quando:

- **Threads de discussão longas** (>3 níveis aninhados): a UI do GitHub renderiza threading com muito mais clareza.
- **Approvals coletivos**: a interface mostra o estado de N revisores em um painel; no terminal você precisa parsear texto.
- **Discussions (não-código)**: comentários gerais, decisões de design, links externos com preview — tudo mais legível na web.
- **Side-by-side rendering visual**: alguns devs preferem o layout split do GitHub pra certas mudanças de formatação.

### Fluxo macro

| Fase | Ação | Ferramenta |
|------|------|------------|
| 1 — Descobrir | Listar PRs abertas | `gh pr list` |
| 2 — Checkout | Criar branch local do PR | `gh pr checkout <num>` |
| 3 — Ler diff | Navegar mudanças por arquivo | lazygit ou `git diff` |
| 4 — Anotar | Rascunhar comentários | nvim em pane paralelo |
| 5 — Submeter | Aprovar / pedir mudanças | `gh pr review` |

## Na prática

### Setup uma vez

Configura delta como pager padrão do git:

```bash
# Configurar delta como pager git
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.light false  # ou true pra terminal claro
```

Feito isso, todos os `git diff`, `git log -p` e `git show` passam pelo delta automaticamente.

### Fluxo completo

```bash
# Fase 1 — Descobrir
gh pr list                              # PRs abertas no repo atual
gh pr list --search "review-requested:@me"

# Fase 2 — Checkout
gh pr checkout 1234

# Fase 3 — Ler diff
lazygit                                 # diff por arquivo
# OU
git diff main...                        # com delta

# Fase 4 — Anotar (em pane paralelo)
nvim review-notes.md

# Fase 5 — Submeter
gh pr review --approve --body "LGTM"
# OU
gh pr review --request-changes --body "$(cat review-notes.md)"
gh pr comment <num> --body "Falta cobrir caso X"
```

### Atalhos úteis no lazygit durante review

| Tecla | Ação |
|-------|------|
| `<space>` em arquivo | Stage/unstage (não necessário na review, mas útil pra teste rápido) |
| `d` em arquivo | Ver diff completo do arquivo |
| `s` em hunk | Split em chunks menores — ajuda a analisar mudança isolada |
| `enter` em arquivo | Navegar hunks com j/k |
| `←` / `→` | Mudar entre arquivos modificados |

### Quando voltar pro browser

- PR com 10+ comentários aninhados: threading fica ilegível no terminal.
- Approval coletivo: UI mostra quem aprovou, quem pediu changes, quem está pendente.
- Discussions sobre design: links, images, PRs cruzados — tudo mais navegável na web.
- Compartilhar diff visual com não-dev: QA, PM, designer — manda o link do GitHub.

## Armadilhas

1. **`gh pr checkout` em working tree sujo**
   - **Causa:** ter mudanças não-comitadas e esquecer de limpar antes do checkout.
   - **Sintoma:** `gh pr checkout` falha com erro de conflito; ou em casos mais graves, merge inesperado de mudanças dependendo do estado.
   - **Como detectar:** rodar `git status` antes de qualquer checkout. Se houver arquivos modificados, o comando vai reclamar.
   - **Solução:** stash (`git stash`) ou worktree (ver nota 07) antes de checkout. Hábito recomendado: `gs && gh pr checkout N` — ver status antes de agir.

2. **Delta config sem `light`/`dark` correto**
   - **Causa:** terminal com fundo claro com delta configurado pra dark (ou vice-versa).
   - **Sintoma:** diff ilegível, contraste péssimo, texto quase invisível sobre o fundo.
   - **Como detectar:** abrir qualquer diff e perguntar "consigo ler isso fluente?". Se tiver que forçar a vista, está errado.
   - **Solução:** `git config --global delta.light true` (terminal claro) ou `delta.light false` (terminal escuro). Themes específicos no galho 6.

3. **Aprovar sem rodar testes localmente**
   - **Causa:** confiança excessiva em "GitHub Actions já testou". CI cobre o happy path; integração sutil pode escapar.
   - **Sintoma:** PR merged e depois aparece bug em produção em fluxo que test suite não cobria.
   - **Como detectar:** seu review tem mudança não-trivial (infra, build, lógica central) e você só leu, não rodou.
   - **Solução:** `gh pr checkout N && <run tests>` antes de approve. O terminal facilita exatamente isso — você já está no código, basta rodar.

4. **Review longa em uma sentada vs. múltiplas sessões**
   - **Causa:** pressão pra "fechar review hoje" mesmo com fadiga acumulada.
   - **Sintoma:** miss de bug óbvio na 30ª linha por exaustão cognitiva; aprovações apressadas.
   - **Como detectar:** se a review passou de 30min sem pausa, a qualidade do olho já caiu.
   - **Solução:** time-box 30min/sessão. PR de 500 linhas vira 2-3 sessões com pausa entre elas. Detach Zellij entre sessões (`zellij d`) — o estado fica preservado, você volta exatamente onde estava.

## Em inglês

- **Code review** — *code review*. "Fiz o code review do PR do bob ontem."
- **Pull request (PR)** — *pull request*. "Abre um PR quando terminar a feature."
- **Checkout** — *checkout*. "Faz o checkout do branch pra rodar localmente."
- **Diff** — *diff*. "O diff mostra exatamente o que mudou entre os commits."
- **Hunk** — *hunk*. "Esse hunk pode ser separado em dois commits distintos."
- **Approve** — *approve*. "Vou aprovar o PR, está tudo ok."
- **Request changes** — *request changes*. "Pedi request changes porque falta tratamento de erro."
- **Reviewer** — *reviewer*. "Você está listado como reviewer nesse PR."
- **Syntax highlighting** — *syntax highlighting*. "O delta faz syntax highlighting real no diff."
- **Pager** — *pager*. "O delta age como pager do git, exibindo o output com cores."

## Veja também

- [[03 - Onboarding em projeto novo]]
- [[07 - Worktrees + Zellij paralelos]]
- [[08 - Refactoring multi-arquivo]]
- [[03-Dominios/Terminal/TUIs/01 - Lazygit — overview|Lazygit overview (galho 4)]]
- [[03-Dominios/Terminal/TUIs/03 - Lazygit — operações intermediárias|Lazygit intermediário (galho 4)]]
- [[03-Dominios/Terminal/CLI Utils/10 - delta — pager moderno pra git diff|delta (galho 6)]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#gh CLI|gh CLI]]
- [[Dicionário do Terminal#PR checkout|PR checkout]]

## Referências

- [gh pr checkout](https://cli.github.com/manual/gh_pr_checkout)
- [gh pr review](https://cli.github.com/manual/gh_pr_review)
