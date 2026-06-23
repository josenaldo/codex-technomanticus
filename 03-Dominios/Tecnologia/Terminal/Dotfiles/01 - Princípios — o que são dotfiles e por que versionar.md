---
title: "Princípios — o que são dotfiles e por que versionar"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - dotfiles
  - iniciado
  - principios
aliases:
  - Princípios dotfiles
---

# Princípios — o que são dotfiles e por que versionar

> [!abstract] TL;DR
> **Dotfile** = arquivo de configuração cujo nome começa com `.` (oculto no `ls` por convenção Unix). Exemplos: `~/.zshrc`, `~/.gitconfig`, `~/.config/nvim/init.lua`. Por que versionar: setup repetível em máquina nova, sync entre máquinas, histórico de mudanças, backup automático no remoto e portfólio demonstrável no GitHub. O que **não** versionar: secrets sem encryption (tokens, private keys), configs geradas por wizard (`.p10k.zsh`), paths absolutos hardcoded e cache/state descartável.

## O que é / Como funciona

### Definição e origem do nome

Um **dotfile** é qualquer arquivo cujo nome começa com `.` (ponto). Em sistemas Unix/Linux, essa convenção faz o arquivo ficar **oculto** no listador de arquivos padrão:

```bash
ls ~          # NÃO mostra arquivos que começam com "."
ls -a ~       # mostra TODOS, incluindo os dotfiles
ls -la ~      # versão longa: permissões, tamanho, data
```

A origem é histórica: nos anos 1970, o comando `ls` foi escrito para ignorar `.` (diretório atual) e `..` (diretório pai) — e acabou ignorando qualquer coisa que começa com ponto. Virou convenção para "metadados e configurações ocultas" e persiste até hoje.

O resultado prático no sistema moderno: as configurações de quase todas as ferramentas de linha de comando — shell, editor, git, SSH — vivem em arquivos `.algo` no seu `$HOME` ou dentro de `~/.config/`.

> [!info] XDG Base Directory
> O padrão moderno (XDG) recomenda que configs fiquem em `~/.config/<app>/` em vez de soltar arquivos direto em `$HOME`. Muitas ferramentas novas (Zellij, Lazygit, Neovim) seguem esse padrão. As mais antigas (Zsh, Git, SSH) ainda usam arquivos direto em `$HOME`. A nota 02 cobre a anatomia completa.

### Exemplos comuns no home

Abaixo uma seleção dos dotfiles mais comuns em um setup Linux/macOS moderno:

| Caminho | Ferramenta | O que configura |
|---|---|---|
| `~/.zshrc` | Zsh | Shell interativo: aliases, plugins, PATH, prompt |
| `~/.bashrc` | Bash | Equivalente do `.zshrc` para Bash |
| `~/.gitconfig` | Git | Nome, e-mail, aliases, editor default |
| `~/.ssh/config` | SSH | Blocos `Host` com alias, usuário, porta, chave |
| `~/.config/nvim/init.lua` | Neovim | Ponto de entrada da config do editor |
| `~/.config/zellij/config.kdl` | Zellij | Multiplexer: keybindings, tema, layout default |
| `~/.config/lazygit/config.yml` | Lazygit | TUI git: editor, temas, custom commands |
| `~/.config/lazydocker/config.yml` | Lazydocker | TUI Docker: custom commands, cores |

> [!warning] O que NÃO está nessa tabela propositalmente
> `~/.gnupg/` (chaves GPG), `~/.ssh/id_rsa` (chave privada SSH) e qualquer arquivo com tokens ou senhas. Esses são **secrets** — veja a seção "O que NÃO versionar" abaixo.

### Por que versionar dotfiles

Versionar dotfiles com git oferece vantagens concretas:

**1. Setup repetível**
Máquina nova (novo emprego, reinstalação, container de dev) fica idêntica em minutos. Sem versionar, o processo leva horas e fica incompleto — "não lembro o que configurei há 2 anos".

**2. Sync entre máquinas**
Edita o `.zshrc` no laptop, commita, dá pull no desktop. Ambos ficam idênticos sem copiar arquivo manualmente.

**3. Histórico de mudanças**
"Por que está quebrando agora?" → dentro do repo de dotfiles, `git log -- zsh/.zshrc` (ou path relativo ao arquivo) mostra exatamente o que mudou e quando. Reverter uma mudança ruim vira `git revert` ou `git checkout`.

**4. Backup natural**
O repo remoto (GitHub, GitLab, Codeberg) é backup automático. Disco falhou? Clone o repo e rode o bootstrap.

**5. Portfólio demonstrável**
`github.com/<usuario>/dotfiles` é CV em forma de código. Recrutadores e colegas veem seu nível de proficiência com ferramentas pela qualidade dos dotfiles — comentários, organização, plugins escolhidos.

**6. Aprendizado comunitário**
Ler dotfiles de outros desenvolvedores experientes é uma das formas mais eficientes de descobrir ferramentas novas, aliases úteis e configurações não óbvias. Sites como [dotfiles.github.io](https://dotfiles.github.io/) agregam exemplos da comunidade.

### O que NÃO versionar

Versionar tudo cegamente causa problemas sérios. Os critérios de exclusão são:

| Categoria | Exemplos | Motivo |
|---|---|---|
| **Secrets sem encryption** | API tokens, senhas em plaintext, `.env` | Vazamento irreversível se o repo for público (ou mesmo privado com acesso indevido) |
| **Chaves privadas SSH/GPG** | `~/.ssh/id_rsa`, `~/.gnupg/private-keys-v1.d/` | Comprometem toda autenticação associada |
| **Configs geradas por wizard** | `~/.p10k.zsh` (gerado por `p10k configure`) | O wizard sobrescreve sua edição manual; gera conflito de "quem manda" |
| **Paths hardcoded** | `/home/alice/projetos/meu-app` | Funciona em `alice`; quebra em `bob` ou em nova máquina |
| **Cache e state descartável** | `~/.cache/`, `~/.local/state/` | Regenerado automaticamente; enche o repo de noise |
| **OAuth tokens e tokens rotativos** | tokens de refresh de CLIs | Rotacionam; versionar não ajuda e pode vazar |

A regra prática: se você editou manualmente e é configuração (não gerado, não cache, não secret) → versionar. Dúvida sobre secret → encriptar primeiro (nota 07) ou deixar fora.

### Cultura dotfiles no GitHub

Existe uma convenção forte na comunidade de desenvolvimento:

- Repo chamado `dotfiles` (ou `<usuario>/dotfiles`) é a convenção universal
- O README explica o que é necessário para usar: clone, dependências, como rodar o bootstrap
- Sites como [dotfiles.github.io](https://dotfiles.github.io/) listam repos notáveis e tutoriais
- O próprio GitHub reconhece o padrão — perfis exibem o repo `dotfiles` de forma destacada

O site dotfiles.github.io resume bem a filosofia: backup, restore e sync das preferências e configurações da sua caixa de ferramentas — além de aprender com a comunidade e compartilhar o que você aprendeu.

## Na prática

### Ver seus dotfiles atuais

Antes de versionar qualquer coisa, faça um inventário do que você já tem:

```bash
# Dotfiles direto em $HOME (estilo legado)
ls -la ~ | grep '^\.'

# Limitando os primeiros 20 resultados
ls -la ~ | grep '^\.' | head -20

# Configs no padrão XDG (~/.config/)
ls -la ~/.config/ 2>/dev/null

# Ver um dotfile específico
ls -la ~/.gitconfig
cat ~/.gitconfig
```

Você vai perceber que já tem vários dotfiles mesmo sem ter feito nada especial — o git cria `~/.gitconfig` na primeira configuração, o Zsh usa `~/.zshrc`, etc.

### Inventário rápido — decisão "o que vale versionar"

Para cada arquivo que você encontrar, passe pelo checklist mental:

1. **Você editou manualmente?**
   - Sim → candidato a versionar
   - Não (gerado por ferramenta) → provavelmente não versionar

2. **É configuração ou cache/state?**
   - Configuração (muda comportamento) → versionar
   - Cache/state (descartável) → não versionar

3. **Contém secret?**
   - Sim (token, senha, private key) → encriptar primeiro (nota 07) ou não versionar agora
   - Não → próxima pergunta

4. **Funciona em outra máquina?**
   - Sim → versionar
   - Não (path hardcoded, config específica de hardware) → refatorar antes de versionar

**Começando por onde?**
A sequência natural para quem está adotando dotfiles pela primeira vez:

1. `~/.gitconfig` — curto, seguro (sem secrets), universal
2. `~/.zshrc` (ou `~/.bashrc`) — o arquivo que você mais edita
3. `~/.ssh/config` — só os blocos `Host`, nunca as chaves privadas
4. `~/.config/nvim/` (ou editor preferido) — quando a config ficar não-trivial
5. Outras configs conforme você começar a customizá-las

### Roadmap pra adoção

```text
Passo 1 — Escolher ferramenta de gerenciamento
  Opções: GNU stow (symlinks simples), chezmoi (templates + secrets), bare repo
  Notas 04, 05 e 06 cobrem cada uma em detalhe

Passo 2 — Criar repo
  Público (portfólio visível) ou privado (se tiver dúvidas sobre o que vai versionar)
  git init ~/dotfiles && cd ~/dotfiles && git remote add origin <url>

Passo 3 — Adicionar configs gradualmente
  Comece com gitconfig e zshrc — os mais seguros e úteis
  Adicione uma ferramenta por vez; não tente migrar tudo de uma vez

Passo 4 — Testar restore
  Clone em uma VM ou container com usuário diferente
  "Funciona em alice mas não em bob?" → há path hardcoded ou dependência implícita

Passo 5 — Lidar com secrets quando aparecer necessidade
  Não force o problema; adicione encryption quando tiver um secret real pra versionar
  Nota 07 cobre git-crypt, age e sops
```

## Armadilhas

### (1) Commitar secret em plaintext

**Causa:** copiar um arquivo de configuração que, sem querer, contém uma API key, token de acesso ou senha — sem revisar o conteúdo antes de commitar.

**Sintoma:** o secret aparece no `git log -p` e, se o repo for público, no histórico do GitHub. Mudar apenas o arquivo e criar novo commit NÃO resolve — o secret ainda está no histórico.

**Como detectar:**
```bash
git log -p | grep -iE "(token|password|api[_-]?key|secret|passwd)"
```

**Solução:** se o secret já foi pusado para um repo público, **rotacione o secret imediatamente** — assuma que ele foi vazado, independente de alguém ter visto ou não. Depois, use `git filter-repo` ou BFG Repo Cleaner para purgar o histórico e force-push. Prevenção: antes de versionar um arquivo, revise o conteúdo com `cat` ou `grep` para secrets.

---

### (2) Versionar `~/.ssh/id_rsa` (private key SSH)

**Causa:** copiar o diretório `~/.ssh/` inteiro para o repo sem filtrar — inclui a chave privada junto com o `config` (que seria seguro versionar).

**Sintoma:** a chave privada fica no repositório. Com ela, qualquer pessoa com acesso ao repo pode se autenticar como você em qualquer servidor onde a chave pública correspondente está registrada.

**Como detectar:**
```bash
git ls-files | grep -E "id_(rsa|ed25519|ecdsa)"
```

**Solução:** versionar **apenas** `~/.ssh/config` (blocos `Host` com alias, usuario, porta — sem nenhuma chave). Chaves privadas: gere novas localmente em cada máquina, copie manualmente quando necessário, ou use encryption da nota 07.

---

### (3) Versionar configs com paths hardcoded

**Causa:** escrever um path absoluto como `/home/alice/projetos/meu-app` ou `/Users/alice/Documents/` diretamente em um arquivo de config — funciona na máquina de alice mas em nenhuma outra.

**Sintoma:** clonar o repo em outra máquina (ou mesmo com outro usuário) e a ferramenta falhar silenciosamente ou gerar erros de "path não encontrado".

**Como detectar:**
```bash
grep -rn "/home/alice\|/Users/alice" ~/dotfiles/
```
Troca `alice` pelo seu usuário.

**Solução:** usar `$HOME` ou `~` em vez de paths absolutos com username. Para casos mais complexos (configs que variam entre máquinas), chezmoi tem sistema de templates que resolvem isso — nota 05.

---

### (4) Sem `.gitignore` adequado — repo polui com cache/state

**Causa:** inicializar o repo sem definir o que ignorar. `~/.cache/`, `~/.local/state/`, arquivos temporários e logs acabam aparecendo como untracked ou, pior, sendo commitados.

**Sintoma:** `git status` cheio de ruído; repo cresce para centenas de MB; commits contêm lixo que não deveria estar lá.

**Como detectar:**
```bash
du -sh .git/         # repo grande demais é sinal
git status           # muitos untracked irrelevantes
```

**Solução:** ferramentas de gerenciamento resolvem isso por design:
- **bare repo**: usa whitelist (lista o que incluir, ignora o resto)
- **GNU stow**: só vê arquivos dentro da pasta `dotfiles/`
- **chezmoi**: trabalha com source directory explícita

Se estiver usando abordagem manual, crie um `.gitignore` robusto desde o início.

---

### (5) Atualizar em uma máquina, esquecer sync — divergência silenciosa

**Causa:** editar o `.zshrc` no laptop, commitar, mas esquecer de fazer pull no desktop antes de editar o mesmo arquivo lá. Duas semanas depois, as versões divergiram silenciosamente.

**Sintoma:** merge conflict com histórico confuso; ou perda de uma das mudanças ao forçar overwrite.

**Como detectar:**
```bash
git status    # antes de editar qualquer dotfile
git log --oneline origin/main..HEAD  # mudanças locais não pusadas
```

**Solução:** cultivar o hábito: `git pull && editar && git commit && git push` em cada máquina. É a disciplina básica de qualquer workflow git — só precisa ser aplicada também aos dotfiles.

---

### (6) Versionar config gerada por wizard e depois editar à mão

**Causa:** ferramentas como Powerlevel10k geram `~/.p10k.zsh` via `p10k configure`. Se você versionar esse arquivo e depois editar à mão, rodar o wizard novamente **sobrescreve suas edições**.

**Sintoma:** customizações manuais desaparecem após rodar `p10k configure` ou o equivalente de outra ferramenta.

**Como detectar:**
```bash
git diff    # antes de rodar qualquer wizard
```

**Solução:** escolha uma das abordagens e mantenha:
1. **Apenas wizard**: sempre re-rodar o wizard pra mudar; nunca editar à mão
2. **Apenas manual**: editar o arquivo diretamente; nunca re-rodar o wizard
3. **Template** (chezmoi): o template gera o arquivo; wizard fica desativado

## Em inglês

- **dotfile** — *dotfile*. "arquivo de configuração com nome começando com ponto."
- **versionar** — *version control*. "controlar mudanças de arquivo via git."
- **sincronizar** — *sync*. "propagar mudanças do repo entre máquinas com pull e push."
- **diretório home** — *home directory*. "pasta pessoal do usuário, acessível via `~` ou `$HOME`."
- **arquivo oculto** — *hidden file*. "arquivo com nome iniciado por `.`, não listado por `ls` sem `-a`."
- **configuração** — *config* (ou *configuration*). "conjunto de preferências de uma ferramenta persistido em arquivo."
- **portfólio** — *portfolio*. "repositório público de dotfiles como evidência de skill técnico."
- **idempotente** — *idempotent*. "script de bootstrap que pode ser rodado N vezes sem efeitos colaterais."
- **bootstrap** — *bootstrap*. "script inicial que clona o repo e aplica os dotfiles em uma máquina nova."
- **restaurar** — *restore*. "recriar o ambiente a partir do repo de dotfiles em uma máquina nova."

## Veja também

- [[02 - Anatomia — estrutura típica e XDG Base Directory]] — anatomia detalhada dos dotfiles e o padrão XDG
- [[03 - Cross-OS — Linux vs macOS vs WSL]] — diferenças entre sistemas operacionais
- [[04 - GNU stow — symlinks declarativos]] — a ferramenta mais simples pra começar
- [[07 - Secrets em dotfiles — git-crypt, age, sops]] — encryption pra dados sensíveis
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Dotfile|dotfile]]

## Referências

- [Arch Wiki — Dotfiles](https://wiki.archlinux.org/title/Dotfiles)
- [Dotfiles community — dotfiles.github.io](https://dotfiles.github.io/)
