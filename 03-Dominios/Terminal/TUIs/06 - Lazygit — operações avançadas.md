---
title: "Lazygit — operações avançadas"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - tuis
  - lazygit
  - magus
  - custom-commands
  - hooks
aliases:
  - Lazygit bisect
  - Lazygit customCommands
---

# Lazygit — operações avançadas

> [!abstract] TL;DR
> Magus em Lazygit: bisect via UI (painel Commits, `b` abre menu de bisect), customCommands em YAML (`key`, `command`, `context`, `prompts`), git hooks nativos respeitados (pre-commit framework é o padrão moderno), worktrees (`w` no painel Branches abre opções de worktree). Custom commands viabilizam force-push with lease, conventional commits prompt, fast PR creation — atalhos próprios versionados nos dotfiles que viram parte do workflow.

## O que é / Como funciona

### Bisect

`git bisect` encontra o commit que introduziu uma regressão por busca binária — em ~log₂(N) iterações, identifica o culpado em centenas de commits.

O Lazygit expõe bisect via UI no painel Commits:

- **`b`** — "View bisect options": abre menu com ações de bisect no commit selecionado
  - **Mark as good** — declara que o commit selecionado não tinha a regressão
  - **Mark as bad** — declara que o commit selecionado tem (ou introduziu) a regressão
  - **Mark as skipped** — pula o commit (útil pra commits com testes não-determinísticos ou que não compilam)
  - **Reset bisect** — aborta a sessão de bisect e retorna ao HEAD original

**Fluxo padrão:**

1. Painel Commits → selecionar um commit antigo sabidamente funcional
2. `b` → "Mark as good"
3. `b` no commit atual (HEAD) → "Mark as bad"
4. Lazygit faz checkout do commit do meio automaticamente
5. Testar (rodar testes, iniciar app, verificar comportamento)
6. `b` → "Mark as good" ou "Mark as bad" conforme o resultado
7. Repetir até Lazygit identificar o commit culpado (~7 iterações pra 100 commits suspeitos)
8. "Reset bisect" ao terminar para voltar ao HEAD

> A opção `B` (uppercase) que abortaria bisect direto foi verificada como ausente — o abort usa "Reset bisect" dentro do menu `b`.

### customCommands — schema completo

Cada entrada em `customCommands:` no `~/.config/lazygit/config.yml` define um atalho shell mapeado a uma tecla num contexto específico do Lazygit.

**Campos top-level:**

| Campo | Tipo | Req | Descrição |
|---|---|---|---|
| `key` | string | não | Tecla que dispara o comando (letra, `<C-x>`, `<enter>`, `<space>`, etc.) |
| `command` | string | sim | Comando shell (aceita Go template com placeholders) |
| `context` | string | sim | Painel em que o keybinding é ativo |
| `description` | string | não | Label exibido no menu `?` do keybindings |
| `output` | string | não | Destino do output do comando |
| `outputTitle` | string | não | Título do popup de output |
| `loadingText` | string | não | Texto exibido enquanto o comando roda |
| `prompts` | array | não | Lista de prompts pra coletar input do usuário |
| `after` | objeto | não | Ações pós-execução (`checkForConflicts: true`) |

**Valores válidos de `output`:**

| Valor | Comportamento |
|---|---|
| `none` | Descarta output |
| `terminal` | Suspende Lazygit; roda no terminal em foreground |
| `log` | Streama pro painel Command Log |
| `logWithPty` | Como `log`, mas roda em pseudo-terminal (compat com programas interativos) |
| `popup` | Exibe em popup dentro do Lazygit |

**Contexts válidos:**

`global`, `status`, `files`, `worktrees`, `submodules`, `localBranches`, `remotes`, `remoteBranches`, `tags`, `commits`, `reflogCommits`, `subCommits`, `commitFiles`, `stash`

Múltiplos contexts separados por vírgula: `context: "commits, subCommits"`.

**Placeholders Go template (campo `command`):**

| Placeholder | Disponível em |
|---|---|
| `{{ .SelectedLocalBranch.Name }}` | `localBranches` |
| `{{ .CheckedOutBranch.Name }}` | qualquer |
| `{{ .SelectedFile.Name }}` | `files` |
| `{{ .SelectedLocalCommit.Sha }}` | `commits` |
| `{{ .SelectedLocalCommit.Name }}` | `commits` |
| `{{ .SelectedWorktree.Path }}` | `worktrees` |
| `{{ .SelectedCommitRange.From }}` | `commits` |
| `{{ .SelectedCommitRange.To }}` | `commits` |
| `{{ .Form.<campo> }}` | qualquer (output de `prompts`) |

Template function utilitária: `{{ quote .SelectedFile.Name }}` — wrap com escape correto pra segurança no shell.

**Tipos de prompt (`prompts`):**

Campos comuns: `type`, `title`, `key` (nome da variável em `{{ .Form.<key> }}`), `condition` (expressão Go template — pula prompt se falsa).

| Tipo | Campos adicionais |
|---|---|
| `input` | `initialValue`, `suggestions.preset` (authors/branches/files/refs/remotes/remoteBranches/tags), `suggestions.command` |
| `confirm` | `body` (texto explicativo) |
| `menu` | `options` (array com `name`, `value`, `description`, `key`) |
| `menuFromCommand` | `command`, `filter` (regex), `valueFormat`, `labelFormat` |

### Exemplos verificáveis

#### Force-push with lease (segurança no rebase)

```yaml
customCommands:
  - key: "F"
    command: "git push --force-with-lease origin {{ .CheckedOutBranch.Name }}"
    context: "global"
    description: "Force-push with lease"
    output: "log"
    prompts:
      - type: "confirm"
        key: "Confirm"
        title: "Force-push with lease em {{ .CheckedOutBranch.Name }}?"
```

#### Conventional commit com menu de tipo

```yaml
customCommands:
  - key: "<C-v>"
    command: "git commit -m \"{{ .Form.Type }}: {{ .Form.Subject }}\""
    context: "files"
    description: "Conventional commit"
    output: "log"
    prompts:
      - type: "menu"
        key: "Type"
        title: "Tipo"
        options:
          - { name: "feat",     value: "feat",     description: "Nova feature" }
          - { name: "fix",      value: "fix",      description: "Bug fix" }
          - { name: "docs",     value: "docs",     description: "Docs" }
          - { name: "refactor", value: "refactor", description: "Refactor" }
          - { name: "test",     value: "test",     description: "Test" }
          - { name: "chore",    value: "chore",    description: "Chore" }
      - type: "input"
        key: "Subject"
        title: "Subject"
```

#### Fast PR creation com gh CLI

```yaml
customCommands:
  - key: "<C-p>"
    command: "gh pr create --base main --head {{ .CheckedOutBranch.Name }} --fill"
    context: "global"
    description: "Create PR pra main"
    output: "log"
```

#### Branch creation com prefixo tipado

```yaml
customCommands:
  - key: "<C-n>"
    command: "git checkout -b {{ .Form.Type }}/{{ .Form.Name }}"
    context: "localBranches"
    description: "New typed branch"
    prompts:
      - type: "menu"
        key: "Type"
        title: "Tipo"
        options:
          - { name: "feat", value: "feat" }
          - { name: "fix",  value: "fix" }
          - { name: "exp",  value: "exp" }
      - type: "input"
        key: "Name"
        title: "Nome (kebab-case)"
```

### Git hooks nativos

O Lazygit **não tem sistema de hooks próprio extensível** — ele respeita exclusivamente os git hooks nativos em `.git/hooks/` (ou o `hooksPath` configurado no git). Isso significa:

- `c` (commit) no Lazygit dispara `pre-commit` e `commit-msg` como o git CLI faria
- Hook que falha bloqueia o commit; Lazygit exibe o output do hook como erro
- `post-commit`, `pre-push` etc. também são respeitados conforme o caso de uso

**Atenção:** `git.skipHookPrefix: "WIP"` no `config.yml` pula hooks pra commits com esse prefixo na mensagem — útil pra commits temporários, mas fácil de abusar.

**Pre-commit framework** (https://pre-commit.com/) é o padrão moderno pra gerenciar hooks:

```bash
# Instalar (recomendado via pipx pra isolamento)
pipx install pre-commit
# Alternativa
pip install pre-commit
```

Criar `.pre-commit-config.yaml` na raiz do repo:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

Instalar os hooks no `.git`:

```bash
pre-commit install
```

A partir daí, `c` no Lazygit aciona o pre-commit framework antes de cada commit. Falha = Lazygit mostra erro e o commit não ocorre.

### Worktrees

Worktrees permitem ter múltiplos working directories do mesmo repositório, cada um em uma branch diferente, sem `stash` nem troca de context.

**Keybindings verificados (Keybindings_en.md):**

- Painel **Local branches**: `w` → "View worktree options" (criar worktree a partir da branch selecionada, etc.)
- Painel **Worktrees**: painel dedicado com operações:
  - `n` — criar novo worktree
  - `<space>` — switch para o worktree selecionado (Lazygit recarrega naquele worktree)
  - `o` — abrir em editor
  - `d` — remover o worktree selecionado
  - `/` — filtrar por texto

O painel Worktrees também pode ser acessado via `w` em Commits, Tags, Stash e Remote branches — todos abrem "View worktree options".

**Equivalente CLI:**

```bash
# Listar worktrees
git worktree list

# Criar worktree em path irmão (recomendado)
git worktree add ../myproj-hotfix hotfix/security

# Remover
git worktree remove ../myproj-hotfix
```

---

## Na prática

### Workflow bisect — encontrar regressão

Cenário: `main` quebrou em produção; commit funcional existe 3 meses atrás.

```text
1. Painel Commits → rolar até commit antigo sabidamente funcional (antes da regressão)
2. `b` → "Mark as good"
3. HEAD (commit atual) → já marcado como bad implicitamente; ou `b` → "Mark as bad" explicitamente
4. Lazygit faz checkout do commit do meio (~N/2)
5. Testar: rodar suite de testes, levantar app, reproduzir o bug
6. `b` → "Mark as good" (se não reproduz) ou "Mark as bad" (se reproduz)
7. Lazygit avança para o próximo ponto médio
8. Repetir ~7x para 100 commits suspeitos
9. Lazygit exibe o commit culpado
10. `b` → "Reset bisect" — retorna ao HEAD original
```

### Workflow custom commands no dia-a-dia

Custom commands são YAML versionado nos dotfiles — uma vez configurados, viram parte natural do workflow:

```text
- `F` (force-push with lease) → substitui digitar git push --force-with-lease + branch name
- `<C-v>` (conventional commit) → elimina hesitação sobre tipo; menu guia o prefixo
- `<C-p>` (PR creation) → abre PR sem sair do Lazygit, sem abrir browser
- `<C-n>` (typed branch) → branch com prefixo consistente feat/fix/exp sem digitar formato
```

**Estratégia de organização:**

1. `context: "global"` pra comandos de qualquer painel (push, PR, fetch especial)
2. `context: "files"` pra commits com templates
3. `context: "localBranches"` pra operações de branch (criação, delete remoto)
4. `context: "commits"` pra operações sobre commit selecionado (revert, copy SHA, tag)

Todos os custom commands vão no mesmo arquivo de config que já vai nos dotfiles — zero overhead de manutenção extra.

### Workflow worktree pra hotfix

Cenário: feature em andamento com dev server rodando; bug crítico em produção precisa de fix urgente.

```text
1. Situação: em feature/auth, dev server rodando no pane ao lado, stash seria inconveniente
2. Lazygit → painel Local branches → selecionar main → `w` → "Create worktree"
3. Path: ../myproj-hotfix | Branch: hotfix/security (nova) → confirmar
4. Lazygit switch pro novo worktree (hotfix/security em ../myproj-hotfix)
5. Implementar o fix no mesmo Lazygit
6. Commitar, push, abrir PR (`<C-p>` se configurado)
7. Voltar ao worktree original: painel Worktrees → selecionar worktree da feature → `<space>`
8. feature/auth intacta: dev server ainda rodando, nenhum stash, nenhum checkout
9. Após merge do hotfix: `d` no worktree de hotfix pra remover
```

---

## Armadilhas

**1. Bisect com testes não-determinísticos (flaky tests)**

- **Causa:** testes flaky passam e falham aleatoriamente, independente do commit; sinal de bisect vira ruído.
- **Sintoma:** bisect converge em commit que não introduziu a regressão; rodando o teste manualmente no commit "culpado" mostra resultados inconsistentes.
- **Detecção:** rerun do bisect em sessão separada aponta commit diferente; rodar o teste 3-5x no mesmo commit mostra resultados misturados.
- **Solução:** usar "Mark as skipped" (`git bisect skip`) no Lazygit pra commits ambíguos; bisect contorna os skipped e converge mesmo assim, com range de culpados ligeiramente maior.

**2. `output` ausente deixa resultado invisível em popup oculto**

- **Causa:** o valor default de `output` pode variar por versão; sem especificar, o output pode ser descartado ou aparecer brevemente num popup que fecha sozinho.
- **Sintoma:** custom command roda (o efeito ocorre — commit foi feito, push foi executado) mas não há feedback visual; difícil saber se teve sucesso ou erro.
- **Detecção:** adicionar `output: "popup"` temporariamente — se o conteúdo aparecer, o output estava sendo perdido antes.
- **Solução:** sempre especificar `output` explicitamente. Preferir `output: "log"` pra streaming de comandos longos; `output: "popup"` pra resultados curtos; `output: "terminal"` pra comandos interativos.

**3. `{{ .Form.Subject }}` com aspas duplas quebra o shell command**

- **Causa:** Go template injeta o valor do input diretamente na string do `command`; se o usuário digitar `"` no input, a aspas interna fecha as aspas do shell, quebrando o comando.
- **Sintoma:** mensagem de commit truncada na primeira aspas; ou erro de shell `unexpected token`; ou commit com mensagem corrompida.
- **Detecção:** testar o custom command com input contendo `"` ou `'`; verificar o Command Log para ver o comando exato gerado.
- **Solução:** usar `{{ quote .Form.Subject }}` (template function embutida do Lazygit) que faz wrap com escape correto. Ex: `command: "git commit -m {{ quote .Form.Subject }}"`.

**4. Worktree criado dentro do repo (path filho) gera confusão**

- **Causa:** `git worktree add ./hotfix` cria o worktree como subdiretório do repo principal; Lazygit e git ficam confusos sobre o que é tracked.
- **Sintoma:** painel Files do repo principal mostra arquivos do worktree filho como untracked; `git status` mostra o diretório `hotfix/` como untracked; operações de discard podem ser destrutivas.
- **Detecção:** `git worktree list` mostra o path; se está dentro do repo principal, é o problema.
- **Solução:** sempre criar worktrees em paths **irmãos** (`../myproj-hotfix`), nunca filhos. Adicionar o path de worktrees ao `.gitignore` se necessário como fallback.

**5. Pre-commit framework lento bloqueia `c` no Lazygit**

- **Causa:** hooks com linters pesados, type-checkers ou testes rodando em modo `pre-commit`; `c` dispara o hook; Lazygit aguarda a conclusão, parecendo congelado.
- **Sintoma:** Lazygit trava na tela de commit por vários segundos; ou, em hooks muito lentos, parece não responder.
- **Detecção:** `pre-commit run --all-files` direto no terminal mostra o tempo total; identificar o hook lento.
- **Solução:** (a) hooks pesados devem rodar em CI, não em `pre-commit` — remover do `.pre-commit-config.yaml`; (b) usar `stages: [pre-push]` pra hooks que só precisam rodar antes do push; (c) `pre-commit run --files <arquivo>` em vez de `--all-files` pra checagens manuais; (d) `SKIP=<hook-id> git commit` pra bypass pontual (mas não default).

**6. `context` errado — custom command não dispara**

- **Causa:** `context: "commits"` quando o painel ativo é `files`; o keybinding só é ativo no context declarado.
- **Sintoma:** pressionar a `key` configurada não faz nada; a tecla pode ter outra ação no context errado.
- **Detecção:** trocar `context` para `"global"` temporariamente — se o comando disparar, o context original estava incorreto. Verificar a lista exata de contexts em Custom_Command_Keybindings.md.
- **Solução:** usar `context: "global"` pra comandos que devem funcionar em qualquer painel; usar context específico apenas quando o placeholder depende do painel (`{{ .SelectedFile.Name }}` exige `files`, etc.).

---

## Em inglês

- **bisect** — *bisect*. "busca binária em histórico de commits para identificar qual commit introduziu uma regressão; `git bisect good/bad/skip`."
- **regressão** — *regression*. "comportamento que funcionava antes e deixou de funcionar após uma mudança no código; o que bisect encontra."
- **custom command** — *custom command*. "atalho shell definido pelo usuário em YAML, mapeado a uma tecla num context específico do Lazygit."
- **prompt** — *prompt*. "diálogo que o Lazygit exibe antes de executar um custom command para coletar input do usuário; tipos: `input`, `menu`, `confirm`, `menuFromCommand`."
- **placeholder** — *placeholder / template variable*. "variável Go template no campo `command` que é substituída pelo valor do context atual; ex: `{{ .CheckedOutBranch.Name }}`."
- **hook** — *hook*. "script executado automaticamente pelo git em eventos específicos (pre-commit, commit-msg, pre-push); Lazygit os respeita como o git CLI faria."
- **worktree** — *worktree*. "diretório de trabalho adicional do mesmo repositório git, em branch própria; múltiplos worktrees coexistem sem interferir."
- **force-push** — *force-push*. "push que sobrescreve histórico remoto; necessário após rebase; prefira `--force-with-lease` para não sobrescrever trabalho de outros."
- **lease** — *lease*. "no contexto de `--force-with-lease`: verificação que o remoto não foi atualizado por outros desde o último fetch; evita sobrescrever commits de colegas."
- **framework** — *framework*. "no contexto de pre-commit: ferramenta que gerencia e executa múltiplos hooks de múltiplas linguagens a partir de um único `.pre-commit-config.yaml`."

---

## Veja também

- [[03 - Lazygit — operações intermediárias]] — pré-req: rebase interativo, cherry-pick
- [[04 - Lazygit — config e customização]] — onde `customCommands` vivem no `config.yml`
- [[03-Dominios/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Bisect (Lazygit)|bisect]], [[Dicionário do Terminal#Custom command (Lazygit)|custom command]], [[Dicionário do Terminal#Worktree|worktree]]

---

## Referências

- Custom Command Keybindings: https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Command_Keybindings.md
- Pre-commit framework: https://pre-commit.com/
- git-worktree: https://git-scm.com/docs/git-worktree
