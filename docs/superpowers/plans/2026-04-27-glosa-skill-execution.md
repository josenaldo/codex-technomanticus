# Skill /glosa + Reestruturação do Vault — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganizar o vault Codex Technomanticus em 5 zonas (Meta/Pergaminhos/Glosas/Domínios/Sendas) e implementar a skill `/glosa` que cria fichamento de artigo a partir de URL e remove o link de Pergaminhos.

**Architecture:** Duas fases sequenciais. **Fase A** (Tasks A1-A13): auditoria de configs externas + 14 movimentos via `git mv` preservando histórico + criação de arquivos de meta-documentação + validação. Commit único ao final da fase. **Fase B** (Tasks B1-B5): criação da skill em `.claude/skills/glosa/SKILL.md`, validação com URL real (incluindo edge cases), commit único.

**Tech Stack:** Bash (`git mv`), Markdown (skill descriptions, templates, workflow), Obsidian Templater syntax, Claude Code skill framework, WebFetch tool (runtime).

**Spec:** [`docs/superpowers/specs/2026-04-27-glosa-skill-design.md`](../specs/2026-04-27-glosa-skill-design.md)

**Convenções de commit deste projeto:** sem `Co-Authored-By` (preferência registrada em memória).

---

## Fase A — Reestruturação do vault

### Task A1: Auditoria de configs externas e wikilinks com path

**Files:**

- Read: `quartz.config.ts` no repo Quartz separado (cross-repo, fora deste worktree)
- Read: `.obsidian/` (todos os arquivos `*.json`)
- Read: scripts de deploy mencionados em `~/.claude/projects/-home-josenaldo-repos-personal-codex-technomanticus/memory/project_codex.md`
- Read: `.gitignore`

**Output do task:** uma lista textual de paths antigos referenciados em configs (que precisarão ser atualizados no Task A11). Salve a lista em comentário inline no PR/sessão; não precisa criar arquivo.

- [ ] **Step 1: Auditar `.obsidian/` por paths hardcoded**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && grep -rn -E "_templates|_guia|00 - Inbox|Recursos|Aprendizado" .obsidian/ 2>/dev/null || echo "Nenhum match em .obsidian/"
```

Anote cada match (arquivo + linha) — serão atualizados em A11.

- [ ] **Step 2: Auditar `.gitignore`**

Run:

```bash
grep -nE "_templates|_guia|00 - Inbox|Recursos|Aprendizado" /home/josenaldo/repos/personal/codex-technomanticus/.gitignore || echo "Nenhum match em .gitignore"
```

- [ ] **Step 3: Auditar wikilinks com path absoluto**

Wikilinks `[[Nome]]` continuam funcionando após renames de pasta. Mas wikilinks com path (`[[Pasta/Nome]]`) quebram. Detectar:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && grep -rn -E "\[\[[^]|]*/[^]]*\]\]" --include="*.md" 2>/dev/null | grep -vE "(\.tmp|node_modules|\.git)" | head -50
```

Liste todos os matches. Ignore matches em `docs/` (specs internas). Para os demais (em `_guia/`, `_templates/`, `Aprendizado/`, `Recursos/`, ou pastas de domínio), anote — serão atualizados em A11.

- [ ] **Step 4: Auditar repo Quartz cross-repo**

O Quartz está num repo separado em `/home/josenaldo/repos/personal/josenaldo.github.io/` (referenciado pela memória `project_codex.md`). Verificar se existe e se contém referências aos paths antigos:

```bash
ls /home/josenaldo/repos/personal/josenaldo.github.io/quartz.config.ts 2>/dev/null && \
  grep -nE "_templates|_guia|00 - Inbox|Recursos|Aprendizado" /home/josenaldo/repos/personal/josenaldo.github.io/quartz.config.ts || \
  echo "Quartz config não encontrado ou sem matches"
```

- [ ] **Step 5: Anotar findings**

Resuma na resposta da execução:

```text
Auditoria findings:
- .obsidian/: <linhas a atualizar>
- .gitignore: <matches>
- Wikilinks com path: <quantidade> (lista em A11)
- Quartz config: <matches ou "n/a">
```

Não commit — só audit.

---

### Task A2: Criar pastas top-level vazias

**Files:**

- Create: `00-Meta/`, `01-Pergaminhos/`, `02-Glosas/`, `03-Dominios/`, `04-Sendas/` (diretórios)
- Create: `02-Glosas/.gitkeep`, `04-Sendas/senda-frontend/.gitkeep`

- [ ] **Step 1: Criar diretórios top-level**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && mkdir -p 00-Meta 01-Pergaminhos 02-Glosas 03-Dominios 04-Sendas/senda-frontend
```

- [ ] **Step 2: Criar gitkeeps para pastas vazias**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && touch 02-Glosas/.gitkeep 04-Sendas/senda-frontend/.gitkeep
```

- [ ] **Step 3: Verificar**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls -d 00-Meta 01-Pergaminhos 02-Glosas 03-Dominios 04-Sendas 04-Sendas/senda-frontend
```

Expected: 6 linhas, todas existindo.

Sem commit — vai junto com A13.

---

### Task A3: Migrar `_guia`, `_templates`, `Recursos` → `00-Meta/`

**Files:**

- Move: `_guia/` → `00-Meta/guia/`
- Move: `_templates/` → `00-Meta/templates/`
- Move: `Recursos/` → `00-Meta/recursos/`

- [ ] **Step 1: Mover `_guia` → `00-Meta/guia`**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv _guia 00-Meta/guia
```

- [ ] **Step 2: Mover `_templates` → `00-Meta/templates`**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv _templates 00-Meta/templates
```

- [ ] **Step 3: Mover `Recursos` → `00-Meta/recursos`**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Recursos 00-Meta/recursos
```

- [ ] **Step 4: Verificar**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 00-Meta/
```

Expected: `guia/`, `templates/`, `recursos/` (e mais coisas a serem adicionadas em tasks seguintes).

---

### Task A4: Migrar `Aprendizado/Mestres` → `00-Meta/mestres/`

**Files:**

- Move: `Aprendizado/Mestres/` → `00-Meta/mestres/`

- [ ] **Step 1: Mover Mestres**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Aprendizado/Mestres 00-Meta/mestres
```

- [ ] **Step 2: Verificar**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 00-Meta/mestres/
```

Expected: o conteúdo original de `Aprendizado/Mestres/`.

---

### Task A5: Migrar `Aprendizado/RPA` e `Trilha Entrevistas.md` → `04-Sendas/`

**Files:**

- Move: `Aprendizado/RPA/` → `04-Sendas/rpa/`
- Move: `Aprendizado/Trilha Entrevistas.md` → `04-Sendas/trilha-entrevistas/Trilha Entrevistas.md`
- Possível: `Aprendizado/Aprendizado.md` (MOC da pasta, se existir) → `04-Sendas/Sendas.md`

- [ ] **Step 1: Verificar conteúdo de `Aprendizado/`**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls -la Aprendizado/
```

Identifique todos os arquivos e subpastas restantes (após Mestres ter saído em A4).

- [ ] **Step 2: Mover RPA**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Aprendizado/RPA 04-Sendas/rpa
```

- [ ] **Step 3: Criar pasta destino e mover Trilha Entrevistas**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && mkdir -p 04-Sendas/trilha-entrevistas && git mv "Aprendizado/Trilha Entrevistas.md" "04-Sendas/trilha-entrevistas/Trilha Entrevistas.md"
```

- [ ] **Step 4: Mover MOC da Aprendizado se existir**

Se `Aprendizado/Aprendizado.md` existir:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && [ -f Aprendizado/Aprendizado.md ] && git mv Aprendizado/Aprendizado.md 04-Sendas/Sendas.md || echo "Aprendizado.md não existe — skip"
```

- [ ] **Step 5: Mover quaisquer outros arquivos restantes em Aprendizado**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls Aprendizado/ 2>/dev/null
```

Se houver arquivos restantes não previstos, decida caso a caso (provavelmente vão pra `04-Sendas/` no top level, ou pra `00-Meta/` se forem meta-conteúdo). Mova com `git mv`.

- [ ] **Step 6: Remover diretório vazio**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && rmdir Aprendizado
```

Expected: sucesso silencioso. Se falhar com "directory not empty", investigue antes de prosseguir.

---

### Task A6: Migrar `00 - Inbox/` → `01-Pergaminhos/`

**Files:**

- Move: `00 - Inbox/Entradas.md` → `01-Pergaminhos/entradas.md`
- Move: `00 - Inbox/Avaliar.md` → `01-Pergaminhos/avaliar.md`
- Move: `00 - Inbox/entradas/inglês.md` → `03-Dominios/Carreira/Inglês/Inglês — entradas.md` (decisão da spec §11.2, default)

- [ ] **Step 1: Mover Entradas.md (renomeando pra lowercase)**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv "00 - Inbox/Entradas.md" 01-Pergaminhos/entradas.md
```

- [ ] **Step 2: Mover Avaliar.md (renomeando pra lowercase)**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv "00 - Inbox/Avaliar.md" 01-Pergaminhos/avaliar.md
```

- [ ] **Step 3: Verificar conteúdo restante de `00 - Inbox/`**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls -la "00 - Inbox/" "00 - Inbox/entradas/" 2>/dev/null
```

Expected: só `00 - Inbox/entradas/inglês.md` (a ser movido em A7) e diretórios vazios.

NÃO remova `00 - Inbox/` ainda — fica para o Task A7.

---

### Task A7: Migrar 10 pastas de domínio → `03-Dominios/` + finalizar Inglês entradas

**Files:**

- Move: `Arquitetura/`, `Ferramentas/`, `Fundamentos/`, `Go/`, `IA/`, `Infraestrutura/`, `Inglês/`, `Java/`, `JavaScript/`, `Python/` → `03-Dominios/<nome>/`
- Move: `00 - Inbox/entradas/inglês.md` → `03-Dominios/Carreira/Inglês/Inglês — entradas.md`
- Cleanup: `00 - Inbox/`

- [ ] **Step 1: Mover as 10 pastas de domínio**

Run cada um sequencialmente:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Arquitetura 03-Dominios/Arquitetura
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Ferramentas 03-Dominios/Ferramentas
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Fundamentos 03-Dominios/Fundamentos
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Go 03-Dominios/Go
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv IA 03-Dominios/IA
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Infraestrutura 03-Dominios/Infraestrutura
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Inglês 03-Dominios/Inglês
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Java 03-Dominios/Java
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv JavaScript 03-Dominios/JavaScript
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv Python 03-Dominios/Python
```

- [ ] **Step 2: Mover `inglês.md` que estava em `00 - Inbox/entradas/`**

Agora que `03-Dominios/Carreira/Inglês/` existe:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git mv "00 - Inbox/entradas/inglês.md" "03-Dominios/Carreira/Inglês/Inglês — entradas.md"
```

- [ ] **Step 3: Cleanup `00 - Inbox/`**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && rmdir "00 - Inbox/entradas" "00 - Inbox"
```

Expected: silencioso. Se falhar, investigue (algum arquivo escondido tipo `.DS_Store`).

- [ ] **Step 4: Verificar**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 03-Dominios/ && echo "---" && ls -la "00 - Inbox" 2>&1 | head -2
```

Expected: 10 pastas de domínio em `03-Dominios/`; `ls 00 - Inbox` retorna "No such file or directory".

---

### Task A8: Criar `00-Meta/workflow.md`

**Files:**

- Create: `00-Meta/workflow.md`

- [ ] **Step 1: Criar workflow.md**

Conteúdo:

````markdown
---
title: "Workflow do Codex"
created: 2026-04-27
updated: 2026-04-27
type: how-to
status: seedling
tags:
  - guia
  - meta
publish: false
---

# Workflow do Codex Technomanticus

Este vault é organizado em **5 zonas** que refletem o pipeline cognitivo de um commonplace book pessoal.

## As 5 zonas

```text
00-Meta/         meta-linguagem do codex (templates, guia, recursos, mestres)
01-Pergaminhos/  links brutos coletados, ainda não processados
02-Glosas/       fichamentos de artigos lidos
03-Dominios/     conhecimento integrado e evergreen, organizado por área
04-Sendas/       caminhos curatoriais que sequenciam Domínios pra estudo
```

## Como o material flui

1. **Captura.** Você acha um link interessante → cola em `01-Pergaminhos/entradas.md`, sob uma seção temática (`# Tema`)
2. **Destilação.** Lê o artigo → invoca `/glosa <url>` → ficha aparece em `02-Glosas/<ano>-<slug>.md`
3. **Limpeza automática.** A skill `/glosa` remove o link de `01-Pergaminhos/entradas.md` se ele estava lá
4. **Integração** (opcional, sob demanda). Se um artigo merece estudo profundo, você o relê e extrai notas atômicas pra `03-Dominios/<área>/`
5. **Curadoria** (opcional). Pra preparar entrevista ou estudo focado, você sequencia notas de Domínios numa Senda em `04-Sendas/<nome-da-senda>/`

## Skill `/glosa`

Invocação:

- `/glosa <url>` (slash command, forma canônica)
- "Claude, fiche esse link: <url>" (linguagem natural)

Comportamento:

- Faz `WebFetch` da URL e extrai título, autor, site, data, idioma, body
- Gera draft com **TL;DR**, **Pontos-chave**, **Citações** (verbatim na língua original) e **Tags**
- Deixa **Meu comentário** vazio (é onde a ficha vira sua)
- Deixa **Ver também** vazio (você preenche os wikilinks)
- Escreve o arquivo em `02-Glosas/<ano>-<slug>.md`
- Remove a linha de `01-Pergaminhos/entradas.md` se o link estava lá

Limitações do MVP:

- Só artigos web (HTML)
- PDFs, vídeos do YouTube, podcasts: não suportados — a skill avisa e aborta

## Convenções

- **Filename de Glosas**: `<ano>-<slug-kebab-case>.md` (ex: `2026-ai-now-writes-97-of-my-code.md`). Em colisão de slug no mesmo ano: sufixo `-2`, `-3`, etc.
- **Frontmatter `publish: false`** em Glosas (não vão pro site público via Quartz)
- **Wikilinks sem path absoluto**: prefira `[[Nome da Nota]]` em vez de `[[Pasta/Nome da Nota]]`
- **Idioma das seções autorais** (TL;DR, Pontos-chave, Meu comentário, Ver também): PT-BR
- **Idioma das citações**: língua original do artigo

## Templates

Veja `00-Meta/templates/`. O `Template - Glosa.md` é usado tanto pela skill (gerando o arquivo) quanto manualmente via Templater no Obsidian (criação manual).
````

- [ ] **Step 2: Escrever o arquivo**

Use Write tool em `/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/workflow.md` com o conteúdo do Step 1.

- [ ] **Step 3: Verificar**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && head -20 00-Meta/workflow.md
```

Expected: frontmatter + título.

---

### Task A9: Criar `00-Meta/templates/Template - Glosa.md`

**Files:**

- Create: `00-Meta/templates/Template - Glosa.md` (template Templater do Obsidian)

- [ ] **Step 1: Criar o template**

Conteúdo:

```markdown
---
title: "<% tp.file.title %>"
aliases: []
source: 
author: 
site: 
published: 
read: <% tp.date.now("YYYY-MM-DD") %>
type: glosa
status: lido
tags:
  - 
lang: 
publish: false
---

# <% tp.file.title %>

## TL;DR

<!-- 1 a 3 frases em PT-BR sintetizando o argumento principal -->

## Pontos-chave

- 

## Citações

> 

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- 
```

- [ ] **Step 2: Escrever o arquivo**

Use Write tool em `/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Glosa.md` com o conteúdo do Step 1.

- [ ] **Step 3: Verificar**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls "00-Meta/templates/"
```

Expected: lista incluindo `Template - Glosa.md` (e os templates pré-existentes).

---

### Task A10: Atualizar `00-Meta/guia/Como usar este vault.md` refletindo nova estrutura

**Files:**

- Modify: `00-Meta/guia/Como usar este vault.md`

- [ ] **Step 1: Ler o arquivo atual**

Use Read tool em `/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/Como usar este vault.md`.

- [ ] **Step 2: Substituir a seção "Estrutura do vault"**

Use Edit tool. O arquivo atual tem seções "Conhecimento agnóstico", "Stacks", "Suporte". Substituir tudo isso pela nova estrutura de 5 zonas.

Substituir o bloco que vai de `## Estrutura do vault` até antes de `## Como navegar` por:

```markdown
## Estrutura do vault

O vault é organizado em **5 zonas numeradas**:

### `00-Meta/` — meta-linguagem do codex

Templates, guia, recursos meta-carreira (Brag Doc, Cursos), referências sobre mentores.

- `guia/` — como usar este vault e o workflow
- `templates/` — templates Templater
- `recursos/` — Brag Document, lista de cursos
- `mestres/` — referências sobre desenvolvedores/mentores
- `workflow.md` — fluxo completo (captura → destilação → integração)

### `01-Pergaminhos/` — links brutos

- `entradas.md` — todos os links coletados, organizados em seções por tema
- `avaliar.md` — wishlist de tópicos a estudar

Pergaminhos é zona de captura: links chegam aqui, são processados (viram Glosas) e removidos. Se o arquivo cresce, é sinal de que há leitura acumulada.

### `02-Glosas/` — fichamentos de artigos

Cada arquivo é uma ficha de leitura: TL;DR + Pontos-chave + Citações + Meu comentário + Ver também. Filename: `<ano>-<slug>.md`. Populado pela skill `/glosa` (ou manualmente via Templater).

### `03-Dominios/` — conhecimento evergreen

Notas atômicas, organizadas por área:

- **Agnósticas**: `Fundamentos/`, `Arquitetura/`, `Ferramentas/`
- **Stacks**: `Java/`, `JavaScript/`, `Python/`, `Go/`
- **Suporte**: `Infraestrutura/`, `Inglês/`

Cada pasta tem um arquivo MOC (ex: `Java/Java.md`) que serve de índice.

### `04-Sendas/` — caminhos curatoriais

Trilhas de estudo que sequenciam notas de Domínios:

- `trilha-entrevistas/` — preparação para entrevistas internacionais
- `rpa/` — Roadmap Pessoal de Aprendizado
- `senda-frontend/` — estudo focado em frontend (JS/TS/HTML/CSS/React)

Sendas não contêm conhecimento próprio — apontam pra Domínios via wikilinks.
```

- [ ] **Step 3: Atualizar a tabela de templates**

A tabela "Templates disponíveis" precisa incluir Template - Glosa. Localize a linha que termina com `Template - Mestre` e adicione, na linha seguinte:

```markdown
| Template - Glosa          | Fichamento de artigo lido (formato Glosa)   |
```

- [ ] **Step 4: Verificar**

Use Read tool no arquivo e confirme que a nova estrutura está consistente.

---

### Task A11: Aplicar correções de configs identificadas em A1

**Files:**

- Modify: arquivos identificados na auditoria do Task A1

- [ ] **Step 1: Atualizar `.obsidian/` se necessário**

Para cada match registrado em A1, abrir o arquivo e substituir o path antigo pelo novo. Mapeamentos:

```text
_templates       → 00-Meta/templates
_guia            → 00-Meta/guia
00 - Inbox       → 01-Pergaminhos
Recursos         → 00-Meta/recursos
Aprendizado      → 04-Sendas
Aprendizado/RPA  → 04-Sendas/rpa
Aprendizado/Mestres → 00-Meta/mestres
```

Use Edit tool em cada arquivo conforme necessário.

- [ ] **Step 2: Atualizar `.gitignore` se necessário**

Substituir paths antigos pelos novos (mesmo mapeamento do Step 1).

- [ ] **Step 3: Atualizar wikilinks com path absoluto identificados em A1**

Para cada wikilink `[[Pasta/Nome]]` listado em A1 que aponte pra uma pasta renomeada, atualizar usando Edit tool. Exemplo:

```text
[[Aprendizado/Trilha Entrevistas]] → [[Trilha Entrevistas]]   (preferível, sem path)
ou
[[Aprendizado/Trilha Entrevistas]] → [[04-Sendas/trilha-entrevistas/Trilha Entrevistas]]   (com path novo)
```

Recomendado: remover o path e deixar só `[[Nome]]` — Obsidian resolve por nome.

- [ ] **Step 4: Atualizar Quartz config cross-repo se necessário**

Se A1 identificou matches em `/home/josenaldo/repos/personal/josenaldo.github.io/quartz.config.ts`, atualizar lá também usando Edit tool. Se o repo não foi encontrado em A1, skip.

- [ ] **Step 5: Verificar configs intactas**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && grep -rn -E "_templates|_guia|00 - Inbox" .obsidian/ .gitignore 2>/dev/null || echo "Nenhuma referência antiga restante"
```

Expected: `Nenhuma referência antiga restante`. Se ainda houver matches, repita os steps 1-2.

---

### Task A12: Validação final da Fase A

**Files:**

- N/A (apenas validação)

- [ ] **Step 1: Verificar estrutura final no filesystem**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls -d 00-Meta 01-Pergaminhos 02-Glosas 03-Dominios 04-Sendas && \
  echo "---" && \
  ls 00-Meta/ && \
  echo "---" && \
  ls 01-Pergaminhos/ && \
  echo "---" && \
  ls 03-Dominios/ && \
  echo "---" && \
  ls 04-Sendas/
```

Expected:
- 5 diretórios top-level encontrados
- `00-Meta/`: `guia`, `mestres`, `recursos`, `templates`, `workflow.md`
- `01-Pergaminhos/`: `avaliar.md`, `entradas.md`
- `03-Dominios/`: 10 pastas (`Arquitetura`, `Ferramentas`, `Fundamentos`, `Go`, `IA`, `Infraestrutura`, `Inglês`, `Java`, `JavaScript`, `Python`)
- `04-Sendas/`: pelo menos `rpa`, `trilha-entrevistas`, `senda-frontend`

- [ ] **Step 2: Confirmar que pastas antigas sumiram**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls _guia _templates Recursos Aprendizado "00 - Inbox" Arquitetura IA Java 2>&1 | grep "No such file"
```

Expected: 8 linhas "No such file or directory" (uma por pasta antiga).

- [ ] **Step 3: Verificar git status (todas as renomeações registradas)**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git status --short | head -30 && echo "---" && git status --short | wc -l
```

Expected: muitas linhas `R  arquivo-antigo -> arquivo-novo` (renames detectados pelo git) + algumas linhas `??` para arquivos novos (`workflow.md`, `Template - Glosa.md`, `.gitkeep`s) + possíveis `M` para configs atualizadas.

- [ ] **Step 4: Verificar que index.md está intacto na raiz**

A spec memory diz "Nunca remover index.md Quartz". Confirmar:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls index.md README.md
```

Expected: ambos os arquivos existem na raiz.

- [ ] **Step 5: (Opcional) Validar Quartz cross-repo**

Se o repo Quartz existe localmente e tem build local:

```bash
cd /home/josenaldo/repos/personal/josenaldo.github.io && ls package.json 2>/dev/null && echo "Repo Quartz disponível para build manual"
```

Se sim, peça ao autor pra rodar o build manualmente e validar. Senão, skip — a auditoria de A1+A11 deveria ter coberto.

---

### Task A13: Commit da Fase A

**Files:**

- N/A (apenas commit)

- [ ] **Step 1: Revisar uma última vez o que vai ser commitado**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git status
```

Expected: muitos renames + alguns arquivos novos + possíveis modificações em configs. Nenhum arquivo deletado avulso.

- [ ] **Step 2: Adicionar tudo**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git add -A
```

- [ ] **Step 3: Confirmar staging**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git status --short | head -20
```

Expected: linhas começando com letras em verde (renames staged).

- [ ] **Step 4: Commit (sem Co-Authored-By, conforme preferência)**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git commit -m "$(cat <<'EOF'
feat(estrutura): reorganiza vault em 5 zonas (Meta/Pergaminhos/Glosas/Domínios/Sendas)

Reorganiza o codex em pipeline explícito de captura → destilação →
integração. As 14 pastas existentes são migradas via git mv (preservando
histórico). Adiciona workflow.md documentando as zonas e o fluxo /glosa,
e Template - Glosa.md (Templater) para fichamento manual no Obsidian.

Zonas:
- 00-Meta/ (guia, templates, recursos, mestres, workflow)
- 01-Pergaminhos/ (links brutos: entradas.md, avaliar.md)
- 02-Glosas/ (fichamentos — vazio, populado pela skill /glosa)
- 03-Dominios/ (10 pastas de conhecimento evergreen)
- 04-Sendas/ (trilha-entrevistas, rpa, senda-frontend)
EOF
)"
```

- [ ] **Step 5: Confirmar commit**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git log --oneline -1
```

Expected: linha com hash + mensagem do commit recém-criado.

**Fase A concluída.** Vault reestruturado e validado.

---

## Fase B — Implementação da skill `/glosa`

### Task B1: Criar `.claude/skills/glosa/SKILL.md`

**Files:**

- Create: `.claude/skills/glosa/SKILL.md`

- [ ] **Step 1: Criar diretório da skill**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && mkdir -p .claude/skills/glosa
```

- [ ] **Step 2: Escrever SKILL.md**

Use Write tool em `/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/glosa/SKILL.md` com o seguinte conteúdo:

````markdown
---
name: glosa
description: Cria fichamento (Glosa) de artigo web a partir de URL. Use quando o usuário pedir pra fichar/catalogar/registrar um artigo, falar em "ficha de leitura", "fichamento", "glosa", invocar /glosa, ou compartilhar uma URL de artigo pedindo registro. Não suporta PDFs, vídeos do YouTube, podcasts ou tweets — nesses casos, avise e aborte.
---

# Skill: glosa

Cria um fichamento estruturado ("Glosa") de um artigo web em `02-Glosas/<ano>-<slug>.md` e remove o link correspondente de `01-Pergaminhos/entradas.md` se ele estava lá.

## Quando usar

Ative quando o usuário:

- Invoca `/glosa <url>`
- Compartilha uma URL e pede ficha/glosa/fichamento/catálogo/registro
- Diz "fichar esse link", "fazer ficha de leitura", "registrar esse artigo", "catalogar isso"
- Menciona "Pergaminhos" e quer processar um link em ficha

## Quando NÃO usar (e o que fazer)

| Situação                          | Resposta                                                                 |
| --------------------------------- | ------------------------------------------------------------------------ |
| URL é YouTube/Vimeo               | Avise: vídeo não está no MVP. Sugira manter o link em Pergaminhos.       |
| URL termina em `.pdf`             | Avise: PDF não está no MVP. Sugira manter o link em Pergaminhos.         |
| URL é Spotify/podcast             | Avise: podcast não está no MVP. Sugira manter o link em Pergaminhos.     |
| URL é tweet/post de rede social   | Avise: rede social não está no MVP. Sugira manter o link em Pergaminhos. |
| URL é malformada (não HTTP/HTTPS) | Erro: peça uma URL válida.                                               |

## Fluxo de execução

1. **Validar URL.** Deve ser HTTP/HTTPS bem-formada. Se não, erro e abortar.
2. **Detectar tipo.** Domínios `youtube.com`, `youtu.be`, `vimeo.com`, `open.spotify.com`, `twitter.com`, `x.com` → tipo não suportado, avise e aborte. URL terminando em `.pdf` → não suportado, avise e aborte. Demais → assume HTML.
3. **WebFetch.** Use a tool WebFetch com prompt:

   > "Extraia do artigo as seguintes informações: título exato, autor (nome completo se disponível, senão handle/nome de pena), nome do site/publicação, data de publicação no formato YYYY-MM-DD, idioma do conteúdo (`pt` ou `en`), e o body do artigo em markdown limpo. Retorne em formato estruturado, claramente rotulado por campo."

4. **Tratar falhas de fetch.** Se WebFetch retorna erro (404, paywall, timeout, conteúdo < 500 chars sugerindo bloqueio), reporte ao usuário e aborte sem escrever arquivo.
5. **Gerar conteúdo da ficha:**
   - **TL;DR**: 1 a 3 frases em PT-BR sintetizando o argumento principal do artigo
   - **Pontos-chave**: 5 a 7 bullets em PT-BR fiéis ao texto (sem inferências do autor da skill)
   - **Citações**: 3 a 5 trechos verbatim **na língua original do artigo**, escolhidos pela carga semântica (definições, dados, frases de impacto)
   - **Tags**: 3 a 5 tags em kebab-case sem acento, baseadas no conteúdo
   - **Meu comentário**: SEMPRE deixe como placeholder literal `*Escreva aqui sua reação, surpresas, discordâncias.*`. Nunca preencha automaticamente.
   - **Ver também**: SEMPRE deixe vazio (apenas `-`)
6. **Calcular slug.** Normalize o título para ASCII kebab-case, max 60 chars. Remova acentos, pontuação, e palavras vazias do português ("de", "da", "do", "o", "a", "e", "em") se necessário pra caber em 60 chars.
7. **Calcular filename.** `<ano-de-leitura>-<slug>.md`. Ano de leitura = ano corrente.
8. **Resolver colisão.** Se `02-Glosas/<filename>.md` já existe, tente `<filename>-2.md`, `<filename>-3.md`, etc. Avise o usuário: "Atenção: pode ser duplicata semântica de uma Glosa existente."
9. **Escrever arquivo.** Use Write tool em `02-Glosas/<filename>.md` com o template (seção "Template do arquivo" abaixo) preenchido.
10. **Limpar Pergaminhos.** Leia `01-Pergaminhos/entradas.md` linha por linha. Para cada linha, verifique se contém a URL como substring (cobrindo os formatos `<url>`, `[texto](url)`, e URL crua). Se encontrar, remova a linha inteira. Use Edit tool com `old_string` = linha completa, `new_string` = "" (string vazia, mas note: Edit tool falha com new_string vazio em algumas versões — alternativa: ler todo o arquivo, filtrar linhas, reescrever com Write).
11. **Reportar ao usuário.** Uma destas duas mensagens conforme o caso:
    - `Glosa criada: 02-Glosas/<filename>.md. Link removido de Pergaminhos: ✓`
    - `Glosa criada: 02-Glosas/<filename>.md. Link não estava em Pergaminhos.`

## Template do arquivo

Estrutura completa que a skill escreve. Substitua `<placeholders>` pelos valores extraídos.

```markdown
---
title: "<título exato do artigo>"
aliases: ["<título exato do artigo>"]
source: <url>
author: <autor>
site: <nome do site>
published: <YYYY-MM-DD ou vazio se não detectado>
read: <hoje YYYY-MM-DD>
type: glosa
status: lido
tags: [<tag1>, <tag2>, <tag3>]
lang: <pt ou en>
publish: false
---

# <título> — <autor>

## TL;DR

<1 a 3 frases em PT-BR>

## Pontos-chave

- <bullet 1>
- <bullet 2>
- <bullet 3>
- <bullet 4>
- <bullet 5>

## Citações

> "<citação 1 na língua original>"

> "<citação 2 na língua original>"

> "<citação 3 na língua original>"

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
```

## Convenções rígidas

- **PT-BR** em TL;DR, Pontos-chave, Meu comentário, Ver também
- **Língua original** em Citações
- **Tags**: kebab-case ASCII, 3-5 por ficha
- **`publish: false`** sempre (Glosas não vão pro site público)
- **`status: lido`** no momento da criação
- **`Meu comentário`** sempre placeholder vazio — nunca preencher

## Edge cases (tabela)

| Caso                                  | Comportamento                                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------------------------- |
| URL malformada                        | Erro + abortar; não escreve arquivo                                                            |
| WebFetch retorna 404/paywall/timeout  | Reporte erro com mensagem clara; não escreve arquivo                                           |
| Conteúdo extraído < 500 chars         | Alerta sobre paywall ou extração parcial; pergunte se deve seguir mesmo assim                  |
| Tipo não suportado (PDF/YouTube/etc)  | Avise tipo; sugira manter em Pergaminhos; não escreve arquivo                                  |
| Idioma não detectado                  | Default `lang: en` (heurística para artigos técnicos)                                          |
| Data publicação não detectada         | `published:` vazio no frontmatter; mencione no relatório final                                 |
| Autor não detectado                   | `author: "(desconhecido)"`                                                                     |
| Slug colide no mesmo ano              | Sufixo `-2`, `-3`...; alerta de possível duplicata                                             |
| URL em Pergaminhos não bate exato     | Match por substring contendo a URL; remove linha inteira                                       |
| Remoção deixa header de seção vazio   | Mantenha o header; o autor remove na próxima revisão manual                                    |
````

- [ ] **Step 3: Verificar arquivo escrito**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && head -20 .claude/skills/glosa/SKILL.md
```

Expected: frontmatter com `name: glosa` e `description: ...`.

---

### Task B2: Validar a skill — fluxo principal (URL nova)

**Files:**

- N/A (validação live)

**Pré-requisito:** Fase A commitada e SKILL.md criado.

- [ ] **Step 1: Reload de skills no Claude Code**

A skill recém-criada precisa ser reconhecida. Em alguns ambientes basta reiniciar a sessão. Confirme com o usuário que a skill está visível antes de prosseguir.

- [ ] **Step 2: Invocar a skill com URL real**

Peça ao usuário pra invocar:

```text
/glosa https://swizec.com/blog/ai-now-writes-97-of-my-code-heres-what-i-learned/
```

- [ ] **Step 3: Verificar o arquivo gerado**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 02-Glosas/ && head -30 02-Glosas/2026-*.md 2>/dev/null
```

Expected:
- Um arquivo `02-Glosas/2026-<slug>.md`
- Frontmatter completo: `title`, `aliases`, `source`, `author` ("Swizec Teller"), `site` ("swizec.com"), `published` (alguma data), `read` (data de hoje), `type: glosa`, `status: lido`, `tags`, `lang: en`, `publish: false`
- Body com seções: `# Título — Autor`, `## TL;DR`, `## Pontos-chave`, `## Citações`, `## Meu comentário` (placeholder), `## Ver também` (`-`)

- [ ] **Step 4: Critérios de qualidade do conteúdo gerado**

Validar manualmente lendo o arquivo:

- TL;DR é fiel ao argumento do artigo (não inventa nada)
- Pontos-chave são 5-7 bullets em PT-BR
- Citações são verbatim em inglês (NÃO parafraseado, NÃO traduzido)
- "Meu comentário" é exatamente o placeholder
- "Ver também" é apenas `-`

Se algum critério falhou, ajuste o SKILL.md e refaça.

- [ ] **Step 5: Verificar que entradas.md NÃO foi alterado**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git diff 01-Pergaminhos/entradas.md
```

Expected: vazio (URL não estava em Pergaminhos, então nada removido).

E a mensagem da skill deveria ter dito "Link não estava em Pergaminhos."

---

### Task B3: Validar a skill — fluxo "link em Pergaminhos"

**Files:**

- N/A (validação live)

**Pré-requisito:** B2 OK.

- [ ] **Step 1: Adicionar uma URL de teste a Pergaminhos**

Use Edit tool em `01-Pergaminhos/entradas.md` para adicionar (no final do arquivo, ou em uma seção temática):

```markdown
[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
```

(Essa URL pode já existir no arquivo — se sim, use outra que ainda não tenha sido fichada.)

- [ ] **Step 2: Confirmar a inserção**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && grep -n "building-effective-agents" 01-Pergaminhos/entradas.md
```

Expected: pelo menos uma linha com o link.

- [ ] **Step 3: Invocar a skill com a URL adicionada**

Peça ao usuário pra invocar:

```text
/glosa https://www.anthropic.com/engineering/building-effective-agents
```

- [ ] **Step 4: Verificar a Glosa gerada**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 02-Glosas/ | grep building-effective-agents
```

Expected: `2026-building-effective-agents.md` (ou similar).

- [ ] **Step 5: Verificar que a linha foi removida de Pergaminhos**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && grep -n "building-effective-agents" 01-Pergaminhos/entradas.md || echo "OK: link removido"
```

Expected: `OK: link removido`.

A mensagem da skill deveria ter dito: "Link removido de Pergaminhos: ✓"

---

### Task B4: Validar a skill — edge cases

**Files:**

- N/A (validação live)

- [ ] **Step 1: Testar URL de YouTube (tipo não suportado)**

Peça ao usuário pra invocar:

```text
/glosa https://www.youtube.com/watch?v=Unzc731iCUY
```

Expected: skill detecta YouTube, avisa que não está no MVP, e NÃO escreve arquivo.

Verificar:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 02-Glosas/ | grep -i youtube || echo "OK: arquivo não criado"
```

Expected: `OK: arquivo não criado`.

- [ ] **Step 2: Testar URL de PDF**

Peça ao usuário pra invocar:

```text
/glosa https://arxiv.org/pdf/2310.06770.pdf
```

Expected: skill detecta `.pdf`, avisa, e NÃO escreve arquivo.

- [ ] **Step 3: Testar URL malformada**

Peça ao usuário pra invocar:

```text
/glosa not-a-url
```

Expected: skill reporta erro de validação e NÃO escreve arquivo.

- [ ] **Step 4: Testar invocação por linguagem natural**

Peça ao usuário pra digitar (sem slash):

```text
Claude, fiche esse artigo: https://addyosmani.com/blog/agentic-engineering/
```

Expected: skill ativa pelo trigger no description, fluxo normal procede.

Verificar:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && ls 02-Glosas/ | grep agentic-engineering
```

Expected: arquivo gerado.

---

### Task B5: Commit da Fase B

**Files:**

- N/A (apenas commit)

- [ ] **Step 1: Revisar o que vai ser commitado**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git status
```

Expected:
- Novo arquivo: `.claude/skills/glosa/SKILL.md`
- Novos arquivos em `02-Glosas/` (as Glosas geradas pelos testes)
- Modificação em `01-Pergaminhos/entradas.md` (link removido em B3)

- [ ] **Step 2: Decidir o que commitar nesta fase**

A spec diz "Commit: `feat(skill): /glosa cria fichamento de artigo a partir de URL`" — isso cobre a SKILL.md em si.

As Glosas de teste em `02-Glosas/` e a remoção do link de Pergaminhos devem ir num commit separado tipo "test: validação inicial da skill /glosa" OU podem ir junto.

**Decisão recomendada:** dois commits.
- Commit 1: só `SKILL.md` (a skill em si)
- Commit 2: as Glosas de teste + entradas.md modificado (validação)

- [ ] **Step 3: Commit 1 — a skill**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git add .claude/skills/glosa/SKILL.md && \
git commit -m "$(cat <<'EOF'
feat(skill): /glosa cria fichamento de artigo a partir de URL

Skill que recebe uma URL HTTP/HTTPS de artigo, faz WebFetch, gera
template de fichamento (TL;DR, pontos-chave, citações verbatim, tags
em PT-BR; citações em língua original), escreve em 02-Glosas/<ano>-<slug>.md
e remove o link de 01-Pergaminhos/entradas.md se estava lá.

Edge cases: PDFs, YouTube, podcasts, redes sociais avisam e abortam.
Meu comentário e Ver também sempre vazios — campos do autor.
EOF
)"
```

- [ ] **Step 4: Commit 2 — Glosas de validação**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git add 02-Glosas/ 01-Pergaminhos/entradas.md && \
git commit -m "$(cat <<'EOF'
test(glosa): primeiras Glosas geradas pela skill (validação)

Glosas iniciais criadas durante validação da skill /glosa:
- 2026-ai-now-writes-97-of-my-code (Swizec Teller)
- 2026-building-effective-agents (Anthropic)
- 2026-agentic-engineering (Addy Osmani)

Confirma comportamento end-to-end: WebFetch, geração do template,
escrita em 02-Glosas/, remoção de link de Pergaminhos.
EOF
)"
```

- [ ] **Step 5: Confirmar commits**

Run:

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus && git log --oneline -3
```

Expected: três commits topo (Fase B 1+2 + Fase A).

**Fase B concluída.** Skill `/glosa` operacional e validada.

---

## Critérios de aceitação global

- [ ] Vault tem 5 zonas top-level numeradas (`00-Meta` ... `04-Sendas`)
- [ ] Nenhuma das 14 pastas antigas existe mais (`_guia`, `_templates`, `Recursos`, `Aprendizado`, `00 - Inbox`, e os 9 domínios não-renomeados)
- [ ] `00-Meta/workflow.md` documenta as 5 zonas e o fluxo `/glosa`
- [ ] `00-Meta/templates/Template - Glosa.md` existe e funciona via Templater
- [ ] `00-Meta/guia/Como usar este vault.md` reflete a nova estrutura
- [ ] `.claude/skills/glosa/SKILL.md` existe com frontmatter `name: glosa`
- [ ] Skill `/glosa <url>` foi validada com URL real (Swizec) — Glosa gerada manual ou automaticamente passa nos critérios da seção 6 da spec
- [ ] Skill remove link de Pergaminhos quando presente
- [ ] Skill avisa e aborta para tipos não suportados (PDF, YouTube)
- [ ] Quartz continua publicando (validar manualmente cross-repo se aplicável)
- [ ] Wikilinks com path (se existiam) atualizados
- [ ] Commits seguem convenção: sem `Co-Authored-By`, em PT-BR, conventional commits

---

## Notas de execução

- **Paths com espaço:** `00 - Inbox`, `Trilha Entrevistas.md` precisam de aspas em comandos shell. Os comandos no plano já usam aspas — se executar manualmente fora do plano, não esqueça.
- **`git mv` preserva histórico:** todas as movimentações usam `git mv` em vez de `mv` + `git add`. Crucial pra `git log --follow` funcionar nos arquivos movidos.
- **Validação Quartz cross-repo:** este plano não roda o build Quartz porque vive em outro repo. Após a Fase A, o autor pode rodar manualmente em `/home/josenaldo/repos/personal/josenaldo.github.io/` (se aplicável) e reportar regressões.
- **Reload de skill no Claude Code:** após criar `.claude/skills/glosa/SKILL.md`, pode ser necessário reiniciar a sessão pra a skill ser reconhecida. Task B2 pede confirmação ao usuário antes de invocar.
