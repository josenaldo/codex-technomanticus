---
title: "tldr e cheat — docs práticas em fluxo"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - cli-utils
  - magus
  - tldr
  - cheat
  - docs
aliases:
  - tldr
  - cheat
  - tldr-pages
---

> [!abstract] TL;DR
> tldr-pages é coleção comunitária de pages curtas (1 tela, comandos de exemplo); `cheat` é cheatsheet local + customizável (você cria/edita pra workflows próprios). Complementam man — man tem invariantes e edge cases; tldr/cheat respondem "como uso isso AGORA". Múltiplos clientes tldr (tealdeer em Rust é rápido); cheat tem versão Go ativa (Python é legado descontinuado).

## O que é / Como funciona

### Por que duas ferramentas (não escolha)

Não é cheat _ou_ tldr — são complementares, cada uma com nicho:

- **tldr-pages**: doc comunitária padronizada, útil pra ferramentas conhecidas e comuns (git, tar, docker, kubectl). Você consulta o que a comunidade documentou.
- **cheat**: cheatsheet local pra workflows seus (comandos kubectl de produção, queries SQL repetidas, flags de deploys). Você cria e edita — é seu segundo cérebro em texto.
- **man**: invariantes e edge cases — documentação completa, oficial, com todas as flags, valores de saída, variáveis de ambiente. Não substituível.

Os três se complementam: tldr pra start rápido, cheat pra repetição pessoal, man pra profundidade.

### tldr-pages

Repositório central em `github.com/tldr-pages/tldr` com milhares de pages em Markdown simples. Estrutura de cada page:

- Nome do comando + descrição curta (2-3 linhas)
- 5-10 exemplos típicos, um por bloco, com placeholder em `{{}}` indicando o que substituir

O cliente baixa as pages de um CDN e cacheia localmente. `tldr --update` atualiza o cache. Em regime offline funciona enquanto o cache local existir.

### Clientes tldr (escolher um)

| Cliente | Linguagem | Instalar |
|---|---|---|
| tealdeer | Rust | `cargo install tealdeer` / `brew install tealdeer` / pacote binário |
| tldr-rust | Rust | `cargo install tldr` |
| tldr (Node) | Node.js | `npm install -g tldr` |
| tldr-py | Python | `pip install tldr` |

**Recomendação hedged**: tealdeer (1.6+) é o mais mantido e rápido em 2026; o cliente Node é a referência oficial mas lento. Verifique o que está disponível no seu repo de pacotes antes de decidir.

### cheat — workflow local

O cheat Go (`cheat/cheat`) mantém cheatsheets em diretórios configurados ("cheatpaths"):

- `~/.config/cheat/cheatsheets/personal/` — seus sheets (editáveis, versionáveis no dotfiles)
- `~/.config/cheat/cheatsheets/community/` — clone do repositório oficial comunitário

Cada cheatsheet é arquivo de texto plano (convencionalmente com frontmatter de tags). Comandos essenciais:

```bash
cheat -e mycheat          # abre $EDITOR pra criar/editar sheet "mycheat"
cheat mycheat             # exibe sheet
cheat -l                  # lista todos os sheets disponíveis
cheat -s rebase           # busca pattern em todos os sheets
cheat -r -s rebase        # busca com regex
cheat -l -t networking    # lista sheets com tag "networking"
```

### Versão histórica do cheat — Go vs Python

Há duas implementações com nomes iguais e histórico diferente:

| Aspecto | cheat Go (`cheat/cheat`) | cheat Python (`chrisallenlane/cheat`) |
|---|---|---|
| Status | Ativo (versão 5.x+) | **Descontinuado** |
| Install | binário no release / `brew install cheat` | `pip install cheat` |
| Config path | `~/.config/cheat/conf.yml` | `~/.cheat/` |
| Detectar versão | `cheat --version` → `cheat 5.x.x` | `cheat --version` → `2.x` / antiga |

`pip install cheat` pode instalar a versão Python descontinuada. Instalar a Go é o caminho certo.

### Quando cada uma vence

| Pergunta | Resposta |
|---|---|
| Operação genérica em comando Y conhecido? | tldr |
| Comando completo do seu workflow específico? | cheat (próprio) |
| Detalhes de TODAS as flags, edge cases? | man |
| Offline sem cache do tldr? | cheat local OU man |

## Na prática

### Setup tldr (assumindo tealdeer)

```bash
# Atualizar cache de pages
tldr --update

# Consultar comandos comuns
tldr tar
tldr docker run
tldr git rebase

# Idioma específico (se tradução disponível)
tldr -L pt_BR tar
tldr -L en tar          # inglês como source-of-truth

# Listar plataformas disponíveis
tldr --list-platforms
```

### Setup cheat

```bash
# Gerar config inicial
cheat --init > ~/.config/cheat/conf.yml

# Criar/editar sheet pessoal
cheat -e mycheat

# Exemplo de conteúdo de um sheet
# ---
# tags: [ git, daily ]
# ---
# Rebase interativo nos últimos N commits
# git rebase -i HEAD~N

# Buscar, ver, listar
cheat -s rebase         # busca pattern
cheat mycheat           # ver sheet
cheat -l                # listar tudo
```

### Receitas com fzf

```bash
# Navegar pages do tldr interativamente
tldr --list | fzf --preview 'tldr {}'

# Navegar cheatsheets pessoais
ls ~/.config/cheat/cheatsheets/personal/ | fzf --preview 'cheat {}'

# Alias conveniente no .zshrc
function ? { tldr "$@"; }
```

Versões hedged: tealdeer 1.6+; cheat 5.1+ (Go version). Verifique localmente com `tldr --version` e `cheat --version`.

## Armadilhas

### (1) tldr-pages desatualizada ou incompleta

**Causa:** tldr é comunidade; pages podem refletir versão antiga ou ter flags faltando — depende de quem mantém aquela page.

**Sintoma:** receita do tldr não funciona; flag mudou; exemplo não roda.

**Como detectar:** comparar com `<comando> --help` da versão instalada localmente.

**Solução:** tldr é ponto de partida, não verdade absoluta. Contribuir fix via PR é aceito com facilidade pelo projeto (PRs simples são merged em dias).

### (2) cheat Go vs cheat Python (legado)

**Causa:** `pip install cheat` ainda instala versão Python descontinuada em ambientes sem Go instalado.

**Sintoma:** comandos diferem (`cheat -l` vs sintaxe antiga); paths de config diferem (`~/.cheat/` vs `~/.config/cheat/`).

**Como detectar:** `cheat --version` — Go imprime `cheat 5.x.x`; Python é numeração antiga (anos atrás) com layout de config diferente.

**Solução:** instalar binário Go direto do repo `cheat/cheat` (release page) ou `brew install cheat`. Documentar em dotfiles qual versão está em uso.

### (3) Cache local do tldr quebrado/antigo

**Causa:** `--update` não foi rodado faz semanas; cache obsoleto.

**Sintoma:** pages aparecem antigas; novos comandos adicionados recentemente não constam.

**Como detectar:** olhar timestamp em `~/.cache/tldr/` (ou `~/.local/share/tealdeer/`).

**Solução:** rodar `tldr --update` periodicamente. Tealdeer tem `auto_update_interval_hours` no config (`~/.config/tealdeer/config.toml`) pra atualizar sozinho.

### (4) Traduções tldr inconsistentes com inglês

**Causa:** pages PT/ES são traduzidas por voluntários; podem estar defasadas em relação ao en.

**Sintoma:** flag mencionada na tradução PT-BR não existe mais; exemplo está desatualizado.

**Como detectar:** comparar `tldr -L pt_BR tar` com `tldr -L en tar`.

**Solução:** preferir `-L en` como source-of-truth; usar traduções apenas como contexto rápido.

### (5) Achar que tldr substitui man

**Causa:** tldr é resumo de 5-10 exemplos; man é referência completa.

**Sintoma:** receita básica funciona; edge case ou flag específica não documentada no tldr.

**Como detectar:** procurar flag avançada (ex: `tldr find` não tem `-printf`; `man find` tem).

**Solução:** tldr pra start rápido; man pra detalhes (semântica de flags, exit codes, env vars). Usar `MANPAGER` com bat torna man menos doloroso.

### (6) Cheatsheets pessoais não versionados — perda em troca de máquina

**Causa:** `~/.config/cheat/cheatsheets/personal/` não foi adicionado ao repo de dotfiles.

**Sintoma:** ao mudar de máquina ou reformatar, cheatsheets pessoais somem.

**Como detectar:** clonar dotfiles em VM e verificar se `cheat -l` retorna seus sheets.

**Solução:** incluir `~/.config/cheat/cheatsheets/personal/` no manager de dotfiles (stow/chezmoi/bare repo). Community sheets chegam via `git clone` separado e não precisam ser versionados junto.

## Em inglês

- **Documentação** — *documentation*. "tldr-pages é documentação community-driven pra comandos CLI."
- **Folha de consulta** — *cheatsheet*. "Cheatsheets locais cobrem workflows que tldr não tem."
- **Página de manual** — *manpage*. "Manpages têm a referência completa; tldr é o resumo prático."
- **Conduzida pela comunidade** — *community-driven*. "tldr-pages é mantido pela comunidade, sem owner central único."
- **Cache** — *cache*. "O cache local do tldr permite uso offline depois do primeiro `--update`."
- **Offline** — *offline*. "Tealdeer funciona offline usando o cache local de pages baixadas."
- **Referência de comandos** — *command reference*. "man é a referência de comandos completa; tldr e cheat focam no uso prático."
- **Orientada a exemplos** — *example-driven*. "tldr é documentação example-driven, não descrição formal de flags."
- **Descontinuado** — *deprecated*. "cheat Python está deprecated; cheat Go é a versão ativa."
- **Fork** — *fork*. "tealdeer é fork do conceito de tldr com implementação própria em Rust."

## Veja também

- [[03 - bat — cat moderno com syntax highlight]] — `MANPAGER` com bat pra manpages bonitas
- [[03-Dominios/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#tldr-pages|tldr-pages]]
- [[Dicionário do Terminal#cheatsheet|cheatsheet]]
- [[Dicionário do Terminal#MANPAGER|MANPAGER]]

## Referências

- tldr-pages: https://tldr.sh/
- tldr-pages repo: https://github.com/tldr-pages/tldr
- cheat repo: https://github.com/cheat/cheat
