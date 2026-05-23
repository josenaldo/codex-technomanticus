---
title: "atuin — history shell com SQLite e sync"
created: 2026-05-22
updated: 2026-05-22
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - cli-utils
  - adepto
  - atuin
  - history
aliases:
  - atuin
  - history sync
---

# atuin — history shell com SQLite e sync

> [!tldr] TL;DR
> atuin reescreve o history do shell em SQLite local, com fuzzy search interativa via Ctrl-R, stats (top comandos, dias mais ativos), e sync opcional E2E-encrypted (self-host ou atuin.sh). Cada comando registra cwd, exit code, duração, hostname — context muito mais rico que `~/.zsh_history`. Init script substitui o binding do Ctrl-R.

## O que é / Como funciona

### Filosofia: history como dataset estruturado

`~/.zsh_history` é texto plano: um comando por linha, sem contexto. atuin substitui isso por um banco SQLite com schema rico: cada entrada registra o comando, diretório de trabalho (`cwd`), hostname, exit code, duração, timestamp e session ID. O Ctrl-R padrão é substituído por uma TUI fuzzy/full-text com filtros — você pode buscar só comandos que rodaram na pasta atual, num host específico, ou que falharam com exit code != 0.

### Search modes

atuin suporta três modos de busca, configuráveis em `config.toml`:

- **`prefix`** — match começa com a query (`query*`). Mais estrito; útil para quem sabe o começo do comando.
- **`fulltext`** — substring match (`*query*`). Acha a query em qualquer posição.
- **`fuzzy`** (default) — estilo fzf; caracteres não-contíguos em ordem. Máxima flexibilidade de digitação.

```toml
search_mode = "fuzzy"
```

### Stats

`atuin stats` exibe agregados: top comandos, dias mais ativos, taxa de sucesso. `atuin history list` lista entradas filtráveis. `atuin history list --cwd ~/work` filtra por pasta; combina com `| grep` pra refinar.

### Sync E2E-encrypted (opcional)

Por default, o SQLite é apenas local. O sync é opt-in:

1. **atuin.sh hosted** — cria conta (`atuin register`), sincroniza com o servidor managed. Conveniente, mas implica confiar na atuin.sh.
2. **Self-host** — rodar o servidor atuin num Docker próprio e apontar `sync_address` pra ele. Elimina a dependência de third-party.

Em ambos os casos, a **chave de encryption é gerada localmente** no setup — o servidor só vê bytes encriptados. O modelo E2E assume que o cliente (binário da atuin.sh) é honesto. Quem quer eliminar também esse trust, compila do código-fonte ou usa self-host com cliente auditado.

### Config (`~/.config/atuin/config.toml`)

Opções principais:

| Chave | Default | Descrição |
|---|---|---|
| `search_mode` | `fuzzy` | Modo de busca: `prefix`, `fulltext`, `fuzzy` |
| `filter_mode` | `global` | Scope: `global`, `host`, `session`, `directory` |
| `auto_sync` | `true` | Sincroniza automaticamente (requer conta) |
| `sync_address` | `https://api.atuin.sh` | Endpoint do servidor (trocar pra self-host) |
| `sync_frequency` | `1h` | Frequência de sync automático |
| `style` | `compact` | Layout da TUI: `auto`, `compact`, `full` |
| `inline_height` | `40` | Linhas máximas da TUI; `0` = fullscreen |
| `secrets_filter` | `true` | Bloqueia comandos com tokens comuns |
| `store_failed` | `true` | Armazena comandos com exit code != 0 |

## Na prática

### Setup

```bash
# Instalar (Linux/macOS — instala via shell script oficial)
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh

# Importar history existente (detecta o shell automaticamente)
atuin import auto
# Ou explícito:
atuin import zsh    # ~/.zsh_history
atuin import bash   # ~/.bash_history

# Ativar no shell (adicionar ao final do ~/.zshrc)
eval "$(atuin init zsh)"

# Opcional: criar conta para sync
atuin register -u alice -e alice@example.com
atuin sync
```

### Config segura (não armazenar secrets)

`secrets_filter = true` (default) bloqueia padrões comuns (tokens AWS, GitHub, Stripe, npm, etc.). Para regras custom, use `history_filter` com regex:

```toml
# ~/.config/atuin/config.toml
search_mode = "fuzzy"
auto_sync = false
inline_height = 25
style = "compact"

# Regex para NÃO armazenar esses comandos
history_filter = [
    "AKIA[0-9A-Z]{16}",
    "ghp_[A-Za-z0-9]{36}",
    "sk-[A-Za-z0-9]{48}",
    ".*--password[= ]",
    ".*-p [^ ]*",
]
```

> [!warning] `history_filter` vs `secrets_filter`
> `secrets_filter = true` filtra baseado em padrões embutidos conhecidos. `history_filter` aceita regex customizados. Para máxima proteção, use ambos.

### Receitas

```bash
# Buscar comandos no diretório atual
atuin search --cwd ~/work git

# Ver estatísticas de uso
atuin stats

# Listar comandos que falharam (exit code != 0)
atuin history list --exit 1 | head -50

# Forçar sync manual
atuin sync

# Abrir TUI interativa com Ctrl-R
# (após eval "$(atuin init zsh)")

# Ver versão instalada
atuin --version
```

> [!note] Versão hedged
> Exemplos testados com atuin 18.x (latest: 18.16.1 em maio/2026). Verifique `atuin --version` localmente — flags podem variar entre versões.

## Armadilhas

**`atuin import` no shell errado** — rodar `atuin import bash` quando o history é do Zsh (ou vice-versa) resulta em "no history found" ou zero entradas importadas. Como detectar: `echo $SHELL` e `echo $HISTFILE`. Solução: usar o subcomando correspondente ao shell real, ou `atuin import auto` que detecta automaticamente. Re-importar não gera duplicatas (deduplicação por hash).

**Sync com atuin.sh = confiar em third-party** — mesmo com E2E encryption, o modelo de trust assume que o cliente binário (baixado da atuin.sh) é honesto. Sintoma: preocupação de privacidade mesmo "E2E encrypted". Como detectar: leia o threat model na documentação. Solução: **self-host** o servidor atuin (Docker; setup simples) se confiança de third-party é problema. E2E continua valendo mesmo no self-host.

**Secrets viajando no sync** — `secrets_filter` e `history_filter` não configurados: tokens de API e senhas presentes em comandos viram parte do history e sincronizam para o servidor. Sintoma: `aws s3 cp ... AKIA...` aparece no `atuin history list`. Como detectar: `atuin history list | grep -iE 'token|key|secret|password'`. Solução: configurar `history_filter` com regex para os formatos de chave da sua stack. Para deletar entradas já existentes: `atuin history list | grep AKIA | xargs -I{} atuin history delete "{}"`

**SQLite lock em uso concorrente intenso** — muitos shells abertos escrevendo no banco simultaneamente. Sintoma: erros esporádicos "database is locked" no terminal. Como detectar: logs em `~/.local/share/atuin/` com lock errors. Solução: versões recentes do atuin lidam bem com concorrência; se persistir, verifique atualizações. Em casos extremos, reduza shells concorrentes ou use `daemon.enabled = true` (atuin daemon serializa as escritas).

**Reset acidental (`atuin history delete`) sem backup** — comando destrutivo executado sem entender o escopo; apaga entradas do history local; se não houver sync ativo, perda permanente. Como detectar antes: `atuin stats` zerado após a operação. Solução: SEMPRE fazer backup de `~/.local/share/atuin/history.db` antes de operações destrutivas. Se sync estava ativo, `atuin sync` baixa o history do servidor.

**Binding Ctrl-R conflita com plugins Zsh** — plugins como `zsh-autosuggestions`, `fzf`, ou `oh-my-zsh` podem redefinir Ctrl-R; se o `eval "$(atuin init zsh)"` vem antes deles no `.zshrc`, o binding do atuin é sobrescrito. Sintoma: Ctrl-R abre o history clássico (não a TUI do atuin). Como detectar: `bindkey | grep '\\^R'` — mostra o widget atual. Solução: mover `eval "$(atuin init zsh)"` para o **fim** do `.zshrc`, depois de todos os plugins que mexem em bindkey.

## Em inglês

- shell history / shell history — registro de comandos executados no shell
- search mode / search mode — modo de busca configurável (prefix, fulltext, fuzzy)
- end-to-end encryption / end-to-end encryption — criptografia fim-a-fim; dados encriptados antes de sair do cliente
- self-host / self-host — hospedar o próprio servidor em infra controlada
- stats / stats — estatísticas de uso (top comandos, frequência, dias ativos)
- exit code / exit code — código de saída de um processo; `0` = sucesso, outros = erro
- working directory (cwd) / working directory — diretório de trabalho no momento do comando
- sync / sync — sincronização de dados entre múltiplas máquinas
- filter / filter — regra de exclusão ou inclusão; aqui: comandos que NÃO devem ser armazenados
- regex / regex — expressão regular usada para casamento de padrões em strings

## Veja também

- [[05 - zoxide — cd inteligente com frecency]] — par natural (atuin pra history; zoxide pra pasta)
- [[12 - Stack interativo — fzf zoxide atuin]] — composição capstone
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#atuin|atuin]]
- [[Dicionário do Terminal#history sync|history sync]]
- [[Dicionário do Terminal#E2E encryption (history sync)|E2E encryption (history sync)]]
- [[Dicionário do Terminal#frecency|frecency]]
- [[Dicionário do Terminal#init script (shell)|init script (shell)]]

## Referências

- atuin docs: https://docs.atuin.sh/
- atuin repo: https://github.com/atuinsh/atuin
