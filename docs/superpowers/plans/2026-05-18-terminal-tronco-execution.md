# Trilha Terminal — Tronco Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Materializar o tronco da trilha Terminal — criar `03-Dominios/Tecnologia/Terminal/index.md` como MOC umbrella, listando os 7 galhos planejados (Editor, Shell, Multiplexer, TUIs de Dev, Dotfiles, CLI Utils, Workflow) com bullets de texto puro até nascerem.

**Architecture:** Conteúdo único de markdown (Obsidian Flavored), seguindo o padrão MOC do vault (frontmatter `type: moc`, callout TL;DR, seção Conteúdo com bullets, Veja também). Galhos pendentes ficam como bullets de texto puro marcados `(planejado)` — sem wikilink — pra evitar red links no graph view. Nenhuma pasta de galho é criada nesta sessão.

**Tech Stack:** Markdown (Obsidian Flavored), git.

**Referências:**
- Spec: `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`
- Padrão MOC de referência: `03-Dominios/Tecnologia/Node/index.md` (estilo do tronco da trilha Node)

---

## File Structure

- **Create:** `03-Dominios/Tecnologia/Terminal/index.md` — MOC tronco da trilha Terminal
- Nenhum arquivo modificado.
- Nenhum galho/subpasta criado.

---

## Pré-requisitos

- Estar na working tree do repo `codex-technomanticus` (branch `main`).
- Wikilink externo `[[03-Dominios/Tecnologia/Ferramentas/Ferramentas|Ferramentas]]` aponta pra folder note existente (`03-Dominios/Tecnologia/Ferramentas/Ferramentas.md`). Verificado.
- Linux ainda não tem `index.md` próprio → não incluímos wikilink pra Linux nesta versão (ativar em sessão futura quando Linux ganhar tronco).

---

## Task 1: Criar o tronco MOC da trilha Terminal

**Files:**
- Create: `03-Dominios/Tecnologia/Terminal/index.md`

- [ ] **Step 1: Verificar que o destino ainda não existe e o parent existe**

Run:
```bash
ls -d "03-Dominios/Tecnologia/Terminal" 2>/dev/null && echo "ALREADY EXISTS — abort" || echo "ok: dir does not exist yet"
ls -d "03-Dominios" && echo "ok: parent exists"
```

Expected: `ok: dir does not exist yet` + `03-Dominios` listed.

Se `03-Dominios/Terminal` já existir, **parar** e investigar — pode ter sido criado por sessão anterior.

- [ ] **Step 2: Criar a pasta e escrever o arquivo `index.md`**

Crie o arquivo `03-Dominios/Tecnologia/Terminal/index.md` com **exatamente** o conteúdo abaixo:

````markdown
---
title: "Terminal"
type: moc
publish: true
created: 2026-05-18
updated: 2026-05-18
status: growing
progresso: andamento
tags:
  - terminal
  - moc
  - dev-environment
aliases:
  - Terminal
---
# Terminal

> [!abstract] TL;DR
> Trilha do ambiente de trabalho no terminal: editor (Neovim/LazyVim), shell (Zsh/p10k), multiplexer (Zellij), TUIs (Lazygit/Lazydocker), dotfiles, CLI utils e playbooks de workflow. 7 galhos, ~57 notas distribuídas em 3 fases (Iniciado → Adepto → Magus) por galho. Cada galho é implementado em sessão própria — esta nota é o roadmap interativo da trilha.

Esta trilha cobre o ecossistema TUI/keyboard-first pra trabalho de desenvolvimento no terminal. Cada galho é fechado em si mesmo (Iniciado + Adepto + Magus na mesma execução) e nasce em uma sessão dedicada com spec e plano próprios.

## Conteúdo

### Galhos

- Editor — galho 1 (planejado): Neovim + LazyVim (modal editing, plugins, LSP)
- Shell — galho 2 (planejado): Zsh + Oh-My-Zsh + Powerlevel10k
- Multiplexer — galho 3 (planejado): Zellij
- TUIs de Dev — galho 4 (planejado): Lazygit, Lazydocker
- Dotfiles — galho 5 (planejado): gerenciamento de configs e sync
- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…
- Workflow — galho 7 (planejado): playbooks cross-tool

### Fases de aprendizado

Cada galho organiza suas notas em 3 fases progressivas:

- **Iniciado** — visão geral, nível júnior. Vocabulário básico, modelo mental, comandos suficientes pra começar a usar a ferramenta.
- **Adepto** — domínio operacional, nível pleno. Configurar, customizar, usar com confiança em projetos reais.
- **Magus** — maestria, nível senior. Técnicas avançadas, otimização, casos de uso obscuros.

## Veja também

- [[03-Dominios/Tecnologia/Ferramentas/Ferramentas|Ferramentas]]
````

Use a ferramenta `Write` com `file_path: <repo>/03-Dominios/Tecnologia/Terminal/index.md` e o conteúdo acima exatamente como está (incluindo a linha em branco final). A ferramenta `Write` cria a pasta `Terminal/` automaticamente.

- [ ] **Step 3: Verificar que o arquivo foi criado e o conteúdo está correto**

Run:
```bash
test -f "03-Dominios/Tecnologia/Terminal/index.md" && echo "ok: file exists"
wc -l "03-Dominios/Tecnologia/Terminal/index.md"
head -16 "03-Dominios/Tecnologia/Terminal/index.md"
```

Expected:
- `ok: file exists`
- Contagem ≥ 30 linhas
- Frontmatter visível nas 16 primeiras linhas (title, type, publish, created, updated, status, progresso, tags, aliases)

- [ ] **Step 4: Validar YAML do frontmatter**

Run (qualquer um dos dois):
```bash
# Opção A — Python (sempre disponível)
python3 -c "
import yaml, sys
content = open('03-Dominios/Tecnologia/Terminal/index.md').read()
# extrai frontmatter entre os dois '---'
parts = content.split('---', 2)
if len(parts) < 3:
    print('FAIL: no frontmatter delimiters'); sys.exit(1)
fm = yaml.safe_load(parts[1])
assert fm.get('type') == 'moc', f'type expected moc, got {fm.get(\"type\")}'
assert fm.get('title') == 'Terminal', f'title expected Terminal, got {fm.get(\"title\")}'
assert 'terminal' in fm.get('tags', []), 'missing tag terminal'
assert 'moc' in fm.get('tags', []), 'missing tag moc'
print('ok: frontmatter valid')
"
```

Expected: `ok: frontmatter valid`. Qualquer outra saída = falha; corrigir o frontmatter no `index.md`.

- [ ] **Step 5: Confirmar que o wikilink externo aponta pra nota existente**

Run:
```bash
test -f "03-Dominios/Tecnologia/Ferramentas/Ferramentas.md" && echo "ok: wikilink target exists"
```

Expected: `ok: wikilink target exists`. Se falhar, o folder note do Ferramentas foi renomeado/removido — investigar antes de prosseguir.

- [ ] **Step 6: Commit**

Run:
```bash
git add "03-Dominios/Tecnologia/Terminal/index.md"
git status
```

Expected: status mostra apenas `new file: 03-Dominios/Tecnologia/Terminal/index.md` em "Changes to be committed". Se outros arquivos aparecerem em staging, abortar e investigar.

Then:
```bash
git commit -m "$(cat <<'EOF'
feat(terminal): scaffold tronco da trilha Terminal

Cria 03-Dominios/Tecnologia/Terminal/index.md como MOC umbrella da trilha
Terminal. Lista os 7 galhos planejados (Editor, Shell, Multiplexer,
TUIs de Dev, Dotfiles, CLI Utils, Workflow) como bullets de texto
puro (sem wikilink) até cada galho nascer em sua própria sessão.
Documenta o padrão de 3 fases (Iniciado/Adepto/Magus) na seção
"Fases de aprendizado".

Roadmap: docs/superpowers/specs/2026-05-18-trilha-terminal-design.md
EOF
)"
```

**Nota importante:** o commit NÃO inclui `Co-Authored-By: Claude` (preferência do usuário). NÃO usar `--no-verify` nem `--no-gpg-sign`.

- [ ] **Step 7: Verificar o commit final**

Run:
```bash
git log --oneline -1
git show --stat HEAD
```

Expected:
- Última linha do log: `<hash> feat(terminal): scaffold tronco da trilha Terminal`
- `git show --stat` mostra exatamente 1 file changed (`03-Dominios/Tecnologia/Terminal/index.md`), com `30+ insertions(+)`.

---

## Critério de pronto

- `03-Dominios/Tecnologia/Terminal/index.md` existe e tem o conteúdo exato da Step 2.
- Frontmatter YAML válido (Step 4 passa).
- Commit `feat(terminal): scaffold tronco...` está no `git log`, sem `Co-Authored-By: Claude`.
- Nenhuma pasta de galho foi criada nesta sessão.
- Nenhum outro arquivo modificado/commitado.

## Não faz parte deste plano

- Criar qualquer pasta `Editor/`, `Shell/`, etc. — cada galho tem sessão própria com spec dedicado.
- Escrever qualquer nota atômica. Esta sessão é puro scaffold do tronco.
- Atualizar índices/MOCs de outros domínios (Linux, Ferramentas) pra apontar pro Terminal — fazer quando relevante em sessão futura.
- Atualizar wikilinks reciprocamente (`Ferramentas.md` apontar de volta pro Terminal) — opcional, fora de escopo agora.
