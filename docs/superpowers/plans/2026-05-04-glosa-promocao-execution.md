# Pipeline de promoção de glosas — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar o pipeline glosa→domínio (frontmatter + estrutura de pastas + 4 skills), reorganizar a documentação do guia em `00-Meta/guia/pipeline/`, e migrar a glosa existente.

**Architecture:** Conjunto de convenções markdown + 4 skills declarativas (Markdown lido pelo Claude). Sem código de runtime — operações sobre arquivos via Edit/Write/Bash. Tudo no repo `codex-technomanticus`; nenhuma alteração no site ou apocrypha.

**Tech Stack:** Markdown + YAML frontmatter, Obsidian (Templater + Dataview), skills do Claude Code (`.claude/skills/<nome>/SKILL.md`).

**Spec:** `docs/superpowers/specs/2026-05-04-glosa-promocao-design.md`

---

## File Structure

### Repo `codex-technomanticus`

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `00-Meta/templates/Template - Glosa.md` | Modify | Frontmatter ganha `created`, `updated`, `promovida_em: []`. |
| `00-Meta/templates/Template - Nota.md` | Modify | Adicionar seção `## Fontes` entre `## Armadilhas comuns` e `## Aprofundamento`. |
| `02-Glosas/2026-design-md-spec-coding-agents.md` | Modify | Migração da glosa existente: incluir os 3 novos campos. |
| `02-Glosas/Promovidas/.gitkeep` | Create | Versionar a pasta vazia. |
| `02-Glosas/Arquivadas/.gitkeep` | Create | Versionar a pasta vazia. |
| `00-Meta/guia/pipeline/index.md` | Create | Visão geral do pipeline. |
| `00-Meta/guia/pipeline/Pergaminhos.md` | Create | Documenta etapa 1 (captura). |
| `00-Meta/guia/pipeline/Glosas.md` | Create | Documenta etapa 2 (fichamento + promoção). |
| `00-Meta/guia/pipeline/Domínios.md` | Create | Documenta corpus de conhecimento. |
| `00-Meta/guia/pipeline/Sendas.md` | Create | Documenta mapas de leitura. |
| `00-Meta/guia/sendas-e-dominios.md` | Delete | Conteúdo migrado pros 5 novos arquivos. |
| `.claude/skills/promover-glosa/SKILL.md` | Create | Skill `/promover-glosa <slug>`. |
| `.claude/skills/sintetizar-glosas/SKILL.md` | Create | Skill `/sintetizar-glosas <criterio>`. |
| `.claude/skills/arquivar-glosas/SKILL.md` | Create | Skill `/arquivar-glosas`. |
| `.claude/skills/acordar-glosas/SKILL.md` | Create | Skill `/acordar-glosas <criterio>`. |

### Notas pro implementador

- **Sem testes unitários.** Skills são markdown declarativo; "testar" significa criar glosas-teste e rodar a skill (Task 15).
- **Sem TDD.** Não aplicável a este tipo de código (Markdown+procedimento). Validação é manual.
- **Commits frequentes.** Cada task termina com 1 commit. Mensagens em português, estilo dos commits recentes (`feat:`, `docs:`, `chore:`). **NÃO usar `Co-Authored-By: Claude`** (preferência do usuário).
- **Caracteres especiais nos paths.** `00-Meta`, `03-Dominios`, `Validação`, etc. — preserve acentos.
- **Hoje é 2026-05-04.**
- **Apocrypha NÃO é tocado.** Restrição absoluta.

---

## Task 1: Atualizar `Template - Glosa.md`

**Files:**
- Modify: `00-Meta/templates/Template - Glosa.md`

- [ ] **Step 1: Ler o arquivo atual**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Glosa.md"
```

Expected (frontmatter):
```yaml
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
progresso: andamento
tags:
  -
lang:
publish: false
---
```

- [ ] **Step 2: Adicionar `created`, `updated`, `promovida_em` no frontmatter**

Use `Edit` tool. Substitua a linha `read: <% tp.date.now("YYYY-MM-DD") %>` por três linhas:

```yaml
read: <% tp.date.now("YYYY-MM-DD") %>
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
```

E após `progresso: andamento`, adicione `promovida_em: []`:

```yaml
progresso: andamento
promovida_em: []
```

Frontmatter final:

```yaml
---
title: "<% tp.file.title %>"
aliases: []
source:
author:
site:
published:
read: <% tp.date.now("YYYY-MM-DD") %>
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
type: glosa
status: lido
progresso: andamento
promovida_em: []
tags:
  -
lang:
publish: false
---
```

Não modifique o body do template.

- [ ] **Step 3: Validar**

```bash
head -25 "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Glosa.md"
```

Confirme que `created`, `updated`, `promovida_em: []` estão presentes na ordem correta.

- [ ] **Step 4: Commit**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add "00-Meta/templates/Template - Glosa.md"
git commit -m "feat(templates): adiciona created, updated, promovida_em em glosas"
```

---

## Task 2: Atualizar `Template - Nota.md` com seção `## Fontes`

**Files:**
- Modify: `00-Meta/templates/Template - Nota.md`

- [ ] **Step 1: Ler o arquivo atual**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Nota.md"
```

Expected: frontmatter com `progresso: pendente`; body com seções "O que é", "Como funciona", "Quando usar", "Armadilhas comuns", "Aprofundamento", "Veja também".

- [ ] **Step 2: Inserir `## Fontes` entre `## Armadilhas comuns` e `## Aprofundamento`**

Use `Edit` tool. Localize o trecho:

```markdown
## Armadilhas comuns

<!-- O que evitar, erros frequentes -->

## Aprofundamento
```

Substitua por:

```markdown
## Armadilhas comuns

<!-- O que evitar, erros frequentes -->

## Fontes

<!--
Glosas e outras fontes que alimentaram esta nota. Wikilinks pras glosas
em `02-Glosas/Promovidas/<ano>/` (ou raiz, se ainda não promovidas).
Skills /promover-glosa e /sintetizar-glosas populam essa seção
automaticamente.

- [[02-Glosas/Promovidas/2026/2026-exemplo-slug|Título da glosa]]
-->

## Aprofundamento
```

- [ ] **Step 3: Validar a ordem das seções**

```bash
grep -n '^## ' "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Nota.md"
```

Expected (ordem):
```
## O que é
## Como funciona
## Quando usar
## Armadilhas comuns
## Fontes
## Aprofundamento
## Veja também
```

- [ ] **Step 4: Commit**

```bash
git add "00-Meta/templates/Template - Nota.md"
git commit -m "feat(templates): adiciona seção Fontes em notas de domínio"
```

---

## Task 3: Migrar a glosa existente

**Files:**
- Modify: `02-Glosas/2026-design-md-spec-coding-agents.md`

- [ ] **Step 1: Ler o frontmatter atual da glosa**

```bash
sed -n '1,20p' "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/2026-design-md-spec-coding-agents.md"
```

Expected (aproximado):
```yaml
---
title: "DESIGN.md — A format specification..."
aliases: ["..."]
source: https://github.com/google-labs-code/design.md?ref=dailydev
author: google-labs-code
site: GitHub
published:
read: 2026-04-27
type: glosa
status: lido
tags: [design-systems, design-tokens, coding-agents, specification]
lang: en
publish: false
---
```

(Pode ter `progresso: andamento` se já foi adicionado em commit anterior — verificar.)

- [ ] **Step 2: Adicionar `created`, `updated`, `promovida_em` ao frontmatter da glosa**

Use `Edit` tool. Após a linha `read: 2026-04-27`, insira:

```yaml
read: 2026-04-27
created: 2026-04-27
updated: 2026-05-04
```

Após a linha `progresso: andamento` (se existir; senão depois de `status: lido`):

```yaml
progresso: andamento
promovida_em: []
```

Se o campo `progresso` ainda não existe, adicione-o também (após `status: lido`):

```yaml
status: lido
progresso: andamento
promovida_em: []
```

- [ ] **Step 3: Validar**

```bash
sed -n '1,20p' "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/2026-design-md-spec-coding-agents.md"
```

Frontmatter deve conter os 3 novos campos. YAML deve permanecer válido.

- [ ] **Step 4: Commit**

```bash
git add "02-Glosas/2026-design-md-spec-coding-agents.md"
git commit -m "chore(glosas): migra glosa existente pros novos campos do frontmatter"
```

---

## Task 4: Criar pastas `Promovidas/` e `Arquivadas/`

**Files:**
- Create: `02-Glosas/Promovidas/.gitkeep`
- Create: `02-Glosas/Arquivadas/.gitkeep`

- [ ] **Step 1: Criar as pastas e os `.gitkeep`**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/Promovidas"
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/Arquivadas"
touch "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/Promovidas/.gitkeep"
touch "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/Arquivadas/.gitkeep"
```

- [ ] **Step 2: Validar**

```bash
ls -la "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/"
ls -la "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/Promovidas/"
ls -la "/home/josenaldo/repos/personal/codex-technomanticus/02-Glosas/Arquivadas/"
```

Expected: as duas subpastas existem e cada uma contém um `.gitkeep`.

- [ ] **Step 3: Commit**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add "02-Glosas/Promovidas/.gitkeep" "02-Glosas/Arquivadas/.gitkeep"
git commit -m "feat(glosas): cria pastas Promovidas/ e Arquivadas/"
```

---

## Task 5: Criar `pipeline/index.md` (visão geral)

**Files:**
- Create: `00-Meta/guia/pipeline/index.md`

- [ ] **Step 1: Criar a subpasta**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline"
```

- [ ] **Step 2: Escrever `pipeline/index.md`**

Use `Write` tool. Conteúdo:

```markdown
---
title: "Pipeline do Codex — Visão geral"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - vault
  - canon
  - pipeline
---

# Pipeline do Codex — Visão geral

O Codex Technomanticus é um grimório vivo: o conhecimento entra como link bruto, amadurece em fichamento, consolida em corpus, e é navegado por mapas. Este documento dá a visão de alto nível do pipeline; cada etapa tem documento próprio nesta subpasta.

## As quatro zonas

| Zona | Pasta | Papel |
|---|---|---|
| 1. Pergaminhos | `01-Pergaminhos/` | Captura inicial: inbox, links soltos, ideias cruas. |
| 2. Glosas | `02-Glosas/` | Fichamentos de materiais externos consumidos. |
| 3. Domínios | `03-Dominios/` | Corpus do conhecimento. **Centro gravitacional do vault**. |
| 4. Sendas | `04-Sendas/` | Mapas curatoriais — fluxogramas de leitura sobre os domínios. |

## Pipeline de alimentação

```text
Pergaminhos → Glosas → Domínios
   ↓             ↓         ↑
captura     fichamento  consolidação
                            ↑
                          Sendas (mapas transversais)
```

A seta de Sendas pra Domínios é dupla: sendas **consomem** notas dos domínios (referenciando wikilinks), mas não alimentam os domínios.

## Princípios

1. **Domínios são estantes; sendas são fluxograma.** Domínios guardam o conhecimento; sendas dizem em que ordem ler.
2. **Glosa é leitura, nota é conhecimento.** Coisas diferentes — glosa permanece como artefato datado, nota nasce como síntese atemporal.
3. **Materiais externos são convites.** Vivem dentro de notas de domínio (callout `[!convite]`), não nas sendas. Quando consumidos, viram glosas.
4. **Progresso é estado de estudo.** Campo `progresso` no frontmatter rastreia o estado pessoal de cada nota/glosa, ortogonal ao `status` (maturidade do conteúdo).

## Documentos por etapa

- [[Pergaminhos]] — etapa 1: captura inicial.
- [[Glosas]] — etapa 2: fichamento e promoção.
- [[Domínios]] — etapa 3: corpus de conhecimento.
- [[Sendas]] — mapas de leitura.

## Ver também

- [[Como usar este vault]]
- [[Convenções de escrita]]
- [[Decisões do vault]]
- [[workflow]]
- [[Wikilinks e MOCs]]
```

- [ ] **Step 3: Validar**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline/index.md" | head -20
```

Confirme frontmatter e início do conteúdo.

- [ ] **Step 4: Commit**

```bash
git add "00-Meta/guia/pipeline/index.md"
git commit -m "docs(guia/pipeline): visão geral do pipeline"
```

---

## Task 6: Criar `pipeline/Pergaminhos.md`

**Files:**
- Create: `00-Meta/guia/pipeline/Pergaminhos.md`

- [ ] **Step 1: Escrever o arquivo**

Use `Write` tool. Conteúdo:

```markdown
---
title: "Pergaminhos — captura inicial"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - pipeline
  - pergaminhos
---

# Pergaminhos — captura inicial

A zona `01-Pergaminhos/` é a **inbox** do vault: tudo que ainda não foi processado. Links interessantes, ideias soltas, capturas de chat com LLMs, anotações de reunião, fragmentos.

## O que vai aqui

- URLs encontradas em redes/feeds que merecem leitura.
- Ideias cruas que não cabem ainda em domínio nenhum.
- Notas tomadas em contexto de captura rápida (mobile, durante leitura, em conversa).
- Fragmentos de chat com LLMs que valem revisitar.

## Convenções

### `entradas.md`

Arquivo principal da zona. É a inbox de URLs. Funciona como TODO list de leituras pendentes.

Formato (não rígido):

```markdown
- https://exemplo.com/artigo-interessante
- [Título legível](https://exemplo.com/outro)
- https://blog.tecnomante.dev/topic — comentário curto
```

A skill `/glosa <url>` lê uma URL daqui (ou recebida diretamente) e produz uma glosa. Se o link estava em `entradas.md`, a skill remove a linha automaticamente.

### Outros pergaminhos

Arquivos `.md` soltos em `01-Pergaminhos/` são notas não-estruturadas. Sem template fixo. Podem virar glosas ou notas de domínio quando o tema amadurecer (manual ou via skill futura).

## Como passa pra próxima etapa

| Origem | Caminho | Skill |
|---|---|---|
| URL em `entradas.md` ou compartilhada | URL → Glosa em `02-Glosas/` | `/glosa <url>` |
| Pergaminho de texto livre | Manual: ler, decidir destino | (sem skill atual; futuro) |

A skill `/glosa` cobre apenas artigos web (HTML). PDF, vídeo, podcast, tweets ficam pendentes — vide [[Glosas]].

## Ver também

- [[Codex/index|Pipeline do Codex]]
- [[Glosas]]
```

- [ ] **Step 2: Validar**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline/Pergaminhos.md" | head -20
```

- [ ] **Step 3: Commit**

```bash
git add "00-Meta/guia/pipeline/Pergaminhos.md"
git commit -m "docs(guia/pipeline): pergaminhos como captura inicial"
```

---

## Task 7: Criar `pipeline/Glosas.md`

**Files:**
- Create: `00-Meta/guia/pipeline/Glosas.md`

- [ ] **Step 1: Escrever o arquivo**

Use `Write` tool. Conteúdo:

```markdown
---
title: "Glosas — fichamento e promoção"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - pipeline
  - glosas
---

# Glosas — fichamento e promoção

A zona `02-Glosas/` é o **fichamento de leituras**. Cada glosa é um snapshot datado de um material externo consumido — com voz situada ("li este artigo, achei interessante X"). Glosas alimentam notas de domínio mas **não viram** notas de domínio.

## Anatomia de uma glosa

Frontmatter:

```yaml
---
title: "..."
aliases: []
source: https://...
author: ...
site: ...
published: 2026-04-15
read: 2026-04-27
created: 2026-04-27
updated: 2026-05-04
type: glosa
status: lido
progresso: andamento | feito | abandonado
promovida_em: []
tags: [...]
lang: pt | en
publish: false
---
```

Body padrão:

- `## TL;DR` — síntese em 1-3 frases (PT-BR).
- `## Pontos-chave` — bullets fiéis ao texto (PT-BR).
- `## Citações` — verbatim na língua original.
- `## Meu comentário` — sua voz: reação, surpresa, discordância.
- `## Ver também` — wikilinks pra notas/glosas relacionadas.

## Estados de uma glosa

| Estado | Significado |
|---|---|
| `progresso: andamento` | Criada (possivelmente em batch), não totalmente lida. |
| `progresso: feito` | Lida, decisão sobre promover/abandonar pendente. |
| `progresso: abandonado` | Lida, decidiu não promover. Fica na raiz até arquivar. |
| `promovida_em: [...]` | Tem ao menos uma promoção registrada. Já alimentou nota(s). |

`progresso: pendente` não se aplica a glosas — toda glosa nasce porque o usuário decidiu processar o material.

## Estrutura de pastas

```
02-Glosas/
├── <ano>-<slug>.md            ← raiz: ativas, decisão pendente
├── Promovidas/
│   └── <ano>/<slug>.md        ← arquivado por /promover-glosa ou /sintetizar-glosas
└── Arquivadas/
    └── <ano>/<slug>.md        ← arquivado por /arquivar-glosas
```

**`<ano>` na subpasta** é o ano da DECISÃO (promoção ou arquivamento), não o ano da glosa em si. O nome do arquivo (`<ano-de-criação>-<slug>.md`) é imutável.

## Pipeline de promoção

Glosa **alimenta** notas de domínio; ela mesma não vira nota. Quando o tema merece consolidação:

- **Glosa → Nota (1→1):** `/promover-glosa <slug>` cria uma nota nova em `03-Dominios/X/` com a TL;DR como ponto de partida e a glosa em `## Fontes`.
- **N glosas → 1 nota:** `/sintetizar-glosas tag:<X>` cria uma nota sintetizando várias glosas (ela prepara o esqueleto com `## Fontes` populada; você escreve a síntese).

Em ambos os casos:
- A glosa é **movida** pra `Promovidas/<ano>/`.
- O frontmatter da glosa ganha `promovida_em: ["[[03-Dominios/X/Nome]]"]`.
- A nota nasce com `progresso: andamento` e `status: seedling` (ponto de partida — você amadurece depois).

## Manutenção do repositório

Glosas inativas há mais de 30 dias na raiz são arquivadas automaticamente:

- `/arquivar-glosas` varre raiz, lista candidatas (idade = `hoje - max(updated, mtime)` > 30d), pede confirmação, move pra `Arquivadas/<ano>/`.
- `/acordar-glosas <slug-ou-tag-ou-assunto>` reativa glosas arquivadas: move de volta pra raiz, reseta `progresso: andamento`.

O critério dos 30 dias aplica-se a TODAS as glosas na raiz, independente de `progresso`. Se você não mexeu numa glosa por 30 dias, ela é arquivada — você pode acordá-la quando precisar.

## Skills do pipeline de glosa

| Skill | O que faz |
|---|---|
| `/glosa <url>` | Cria glosa em `02-Glosas/<slug>.md` a partir de uma URL. |
| `/promover-glosa <slug>` | Promove 1 glosa pra nota nova de domínio + move pra `Promovidas/`. |
| `/sintetizar-glosas <criterio>` | Consolida N glosas em 1 nota nova de domínio + move todas pra `Promovidas/`. |
| `/arquivar-glosas` | Varre raiz, arquiva inativas há >30d. |
| `/acordar-glosas <criterio>` | Reativa glosas previamente arquivadas. |

Cada skill pede confirmação antes de mover ou criar arquivos. Detalhes completos em `.claude/skills/<nome>/SKILL.md`.

## Ver também

- [[Codex/index|Pipeline do Codex]]
- [[Pergaminhos]]
- [[Domínios]]
- [[Sendas]]
```

- [ ] **Step 2: Validar**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline/Glosas.md" | head -30
```

- [ ] **Step 3: Commit**

```bash
git add "00-Meta/guia/pipeline/Glosas.md"
git commit -m "docs(guia/pipeline): glosas como fichamento e promoção"
```

---

## Task 8: Criar `pipeline/Domínios.md`

**Files:**
- Create: `00-Meta/guia/pipeline/Domínios.md`

- [ ] **Step 1: Escrever o arquivo**

Use `Write` tool. Conteúdo:

```markdown
---
title: "Domínios — corpus do conhecimento"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - pipeline
  - dominios
---

# Domínios — corpus do conhecimento

A zona `03-Dominios/` é o **centro gravitacional do vault**. Cada domínio é uma estante coerente sobre um tema, com vocabulário próprio, ferramental próprio, comunidade própria. Notas de domínio são amadurecidas, sintetizadas, idiomáticas do vault.

## Modelo de organização (estantes)

Cada domínio é uma estante. Tipos:

- **Linguagens próprias** ganham estante: `JavaScript/` (apenas core), `TypeScript/`, `HTML/`, `CSS/`, `Java/`, `Python/`, `Go/`.
- **Bibliotecas/frameworks grandes** ganham estante: `React/`, `Vue/`, `Svelte/`, `HTMX/`. Bibliotecas menores moram como notas dentro do domínio mais relevante.
- **Disciplinas (cross-tech)** ganham estante: `Frontend/` é engenharia frontend (arquitetura, perf, a11y, padrões). Não é agrupador de tecnologias.
- **Ferramentas** vão pra `Ferramentas/` (Vite, bundlers, monorepos — cross-tech).

Sendas atravessam estantes naturalmente — vide [[Sendas]].

## Estrutura de uma nota de domínio

Frontmatter (vide `00-Meta/templates/Template - Nota.md`):

```yaml
---
title: "..."
created: 2026-05-04
updated: 2026-05-04
type: concept
status: seedling | budding | evergreen
progresso: pendente | andamento | feito | pausado | abandonado
tags: [...]
publish: true
---
```

Body padrão (todas as seções podem ser preenchidas ou ficar com comentário-placeholder):

```
## O que é
## Como funciona
## Quando usar
## Armadilhas comuns
## Fontes              ← glosas que alimentaram esta nota
## Aprofundamento      ← convites pra externos (callout [!convite])
## Veja também
```

## `progresso` × `status`

São **eixos ortogonais**:

- `status` (`seedling`/`budding`/`evergreen`): maturidade do **conteúdo** da nota — quanto ela foi desenvolvida.
- `progresso` (`pendente`/`andamento`/`feito`/`pausado`/`abandonado`): **seu estado de estudo** — onde você está em relação a essa nota.

Ex.: nota `evergreen` (madura) com `progresso: pendente` (ainda não estudou). Ou nota `seedling` (stub) com `progresso: feito` (consumiu o material via glosa, anotou o essencial, sem aprofundar).

## Callout `[!convite]`

Materiais externos (artigos, vídeos, livros) são apresentados dentro de notas de domínio como **convites a aprofundamento**:

```markdown
> [!convite] Aprofundamento — <tema>
> - [Texto do link](https://...) — autor/origem
>
> Consumiu? Faça uma glosa em `02-Glosas/` e amadureça pro domínio quando fizer sentido.
```

Convite é convite: opcional, sem `progresso` próprio. Quando você consome o material, faz uma glosa via `/glosa <url>`. A glosa eventualmente alimenta uma nota nova (ou esta mesma) via `/promover-glosa` ou `/sintetizar-glosas`.

## Seção `## Fontes`

Lista as glosas (ou outras fontes externas) que alimentaram a nota. Skills `/promover-glosa` e `/sintetizar-glosas` populam automaticamente:

```markdown
## Fontes

- [[02-Glosas/Promovidas/2026/2026-design-md-spec-coding-agents|DESIGN.md spec]]
```

Notas escritas a partir de experiência ou observação direta podem deixar a seção vazia ou removê-la.

## Como passa pra próxima etapa

Domínios não "passam" pra outra etapa — são o destino do pipeline. Mas:

- **Sendas** referenciam notas de domínio (vide [[Sendas]]).
- **Notas se conectam entre si** via wikilinks (`## Veja também`, citações inline, callouts).

## Ver também

- [[Codex/index|Pipeline do Codex]]
- [[Glosas]]
- [[Sendas]]
```

- [ ] **Step 2: Validar**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline/Domínios.md" | head -30
```

- [ ] **Step 3: Commit**

```bash
git add "00-Meta/guia/pipeline/Domínios.md"
git commit -m "docs(guia/pipeline): domínios como corpus do conhecimento"
```

---

## Task 9: Criar `pipeline/Sendas.md`

**Files:**
- Create: `00-Meta/guia/pipeline/Sendas.md`

- [ ] **Step 1: Escrever o arquivo**

Use `Write` tool. Conteúdo:

```markdown
---
title: "Sendas — mapas de leitura"
type: moc
publish: true
created: 2026-05-04
updated: 2026-05-04
tags:
  - guia
  - pipeline
  - sendas
---

# Sendas — mapas de leitura

A zona `04-Sendas/` é o conjunto de **fluxogramas de leitura** que atravessam os domínios. Uma senda diz em que ordem ler as notas de um (ou mais) domínio para atingir um objetivo: aprender React, preparar entrevista, dominar IA, etc.

## O que uma senda contém

- Frontmatter com metadados (`type: trail`, `domain`, `maturity`, etc.).
- Descrição curta da senda (pra quem é, qual o destino, em quanto tempo).
- Pré-requisitos — wikilinks pra notas de outros domínios.
- Sequência ordenada de wikilinks pra notas do domínio principal.
- Bloco dataview de progresso (agregação automática).

## O que uma senda **NÃO** contém

- Texto explicativo de conceitos (vai pra nota do domínio).
- Links externos a artigos, vídeos, livros, cursos (vão pra notas de domínio, dentro de callouts `[!convite]`, ou viram glosas).
- Exercícios, projetos, checkpoints conceituais (vão pro domínio).
- Wikilinks pra headings internos do próprio arquivo.

A senda é um mapa, não a estante.

## Formas: minimal × structured

### `maturity: minimal`

Lista plana ordenada. Use quando a senda é direta e não precisa de fases.

```markdown
## Sequência

1. [[03-Dominios/Tecnologia/Frontend/index|Frontend (engenharia)]]
2. [[03-Dominios/Tecnologia/JavaScript/JavaScript|JavaScript]]
3. [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]]
...
```

### `maturity: structured`

Estrutura em fases. Use quando a senda tem etapas conceituais distintas.

```markdown
## Fase 0 — Cultura e intuição

1. [[03-Dominios/Tecnologia/IA/O que é IA]]
2. [[03-Dominios/Tecnologia/IA/LLMs vs ML clássico]]

## Fase 1 — Fundamentos

1. [[03-Dominios/Tecnologia/IA/Tokenização]]
...
```

## Bloco dataview de progresso

Toda senda tem um bloco `## Progresso` no fim, populado por queries Dataview que agregam o `progresso` das notas referenciadas. Vide `00-Meta/templates/trail.md`.

A primeira tabela mostra cada nota referenciada com seu status atual (`pendente`, `andamento`, `feito`, etc.), com display em formato `Pasta/Arquivo` (caminho relativo a `03-Dominios/`). A segunda tabela ("Resumo") mostra contagens.

No site Quartz, esse bloco aparece como markdown bruto (Quartz não roda Dataview). Tracking é experiência local do Obsidian.

## Como passa pra próxima etapa

Sendas não "passam" pra próxima etapa — são uma forma de navegação dos domínios. Mas:

- **Quando uma senda atinge maturidade**: pode-se subdividi-la em sub-sendas, ou criar sendas relacionadas (ex.: `Senda Frontend` + `Senda React Avançada`).
- **Quando uma senda fica obsoleta**: marcar `status: archived` no frontmatter, deixar como referência histórica.

## Ver também

- [[Codex/index|Pipeline do Codex]]
- [[Domínios]]
```

- [ ] **Step 2: Validar**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline/Sendas.md" | head -30
```

- [ ] **Step 3: Commit**

```bash
git add "00-Meta/guia/pipeline/Sendas.md"
git commit -m "docs(guia/pipeline): sendas como mapas de leitura"
```

---

## Task 10: Deletar `sendas-e-dominios.md`

**Files:**
- Delete: `00-Meta/guia/sendas-e-dominios.md`

- [ ] **Step 1: Confirmar que o conteúdo migrou**

```bash
ls "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/pipeline/"
```

Expected: 5 arquivos (`index.md`, `Pergaminhos.md`, `Glosas.md`, `Domínios.md`, `Sendas.md`).

- [ ] **Step 2: Deletar o arquivo antigo**

```bash
rm "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/sendas-e-dominios.md"
```

- [ ] **Step 3: Verificar que outros arquivos não referenciam o deletado**

```bash
grep -rn "sendas-e-dominios" /home/josenaldo/repos/personal/codex-technomanticus/ 2>/dev/null
```

Expected: nenhum resultado relevante (apenas referências em specs antigas que documentam histórico — aceitável).

- [ ] **Step 4: Commit**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add -A "00-Meta/guia/sendas-e-dominios.md"
git commit -m "docs(guia): remove sendas-e-dominios.md (conteúdo migrado pra pipeline/)"
```

---

## Task 11: Skill `/promover-glosa`

**Files:**
- Create: `.claude/skills/promover-glosa/SKILL.md`

- [ ] **Step 1: Criar a pasta**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/promover-glosa"
```

- [ ] **Step 2: Escrever o `SKILL.md`**

Use `Write` tool. Conteúdo:

```markdown
---
name: promover-glosa
description: Promove uma glosa em `02-Glosas/` para uma nota nova em `03-Dominios/`. Cria a nota usando Template - Nota, popula `## Fontes` com wikilink pra glosa, move a glosa pra `02-Glosas/Promovidas/<ano>/`, e atualiza o frontmatter da glosa com `promovida_em`. Use quando o usuário invocar `/promover-glosa <slug>`, falar em "promover glosa", "criar nota a partir dessa glosa", "esta glosa merece nota", ou pedir explicitamente pra fazer essa transição.
---

# Skill: promover-glosa

Promove **uma** glosa para o status de fonte de uma nota nova de domínio. A glosa permanece como artefato de leitura (movida pra subpasta de promovidas); a nota nasce nova com a TL;DR da glosa como ponto de partida.

## Quando usar

- Usuário invoca `/promover-glosa <slug>` (slug ou wikilink da glosa).
- Usuário invoca `/promover-glosa` sem argumento (modo interativo).
- Usuário diz "promover esta glosa", "criar nota a partir dessa glosa", "esta glosa merece nota de domínio".

## Quando NÃO usar

- Usuário quer consolidar VÁRIAS glosas em UMA nota: use `/sintetizar-glosas` em vez disso.
- Usuário quer apenas marcar glosa como lida (`progresso: feito`): edição manual ou skill futura.

## Argumentos

| Forma | Comportamento |
|---|---|
| `/promover-glosa <slug>` | Promove a glosa especificada (slug do nome de arquivo, sem extensão). |
| `/promover-glosa <wikilink>` | Aceita wikilink (`[[<slug>]]` ou `[[02-Glosas/<slug>]]`). |
| `/promover-glosa` | Modo interativo: lista glosas em raiz com `progresso: feito` ou `andamento`, usuário escolhe. |

## Fluxo de execução

1. **Resolver a glosa.**
   - Se argumento explícito: localizar arquivo em `02-Glosas/` (raiz) ou `02-Glosas/Promovidas/<ano>/`. Se não existir, abortar com erro.
   - Se modo interativo: listar candidatas (em `02-Glosas/` raiz com `progresso` em `andamento` ou `feito`), apresentar pra escolha.

2. **Ler a glosa** com `Read` tool. Extrair:
   - `title` (do frontmatter).
   - `tags` (lista do frontmatter).
   - TL;DR (texto da seção `## TL;DR`).
   - `promovida_em` (lista atual; se já tiver itens, será incrementada).

3. **Sugerir domínio destino.** Heurística:
   - Mapear cada tag pra um domínio candidato olhando `03-Dominios/`. Ex.: tag `react` → `03-Dominios/Tecnologia/React/`. Tag `validacao` → `03-Dominios/Tecnologia/Frontend/Validação/`.
   - Apresentar a sugestão com a tag correspondente. Se múltiplas tags casam com domínios diferentes, listar todas e pedir escolha.
   - Permitir o usuário corrigir/digitar outro caminho.

4. **Sugerir nome da nota.** Default: derivar do `title` da glosa. Ex.: glosa "DESIGN.md — A format specification for describing a visual identity to coding agents — google-labs-code" → sugerir `DESIGN.md` ou `Design Spec for AI Agents`. Pedir confirmação.

5. **Verificar se a nota já existe** em `03-Dominios/<X>/<Nome>.md`:
   - Se SIM: perguntar (a) anexar a glosa às fontes da nota existente, (b) escolher outro nome, (c) cancelar.
   - Se NÃO: prosseguir.

6. **Criar a nota nova** com `Write` tool em `03-Dominios/<X>/<Nome>.md`. Conteúdo:

   ```markdown
   ---
   title: "<Nome da nota>"
   created: <hoje YYYY-MM-DD>
   updated: <hoje YYYY-MM-DD>
   type: concept
   status: seedling
   progresso: andamento
   tags:
     - <tags-da-glosa>
     - <tag-do-domínio se houver convenção>
   publish: true
   ---

   # <Nome da nota>

   <!-- Ponto de partida da glosa: -->
   <!-- <TL;DR da glosa, como comentário, pra você expandir em prosa própria> -->

   ## O que é

   <!-- Definição clara e objetiva -->

   ## Como funciona

   <!-- Mecanismo, funcionamento, detalhes relevantes -->

   ## Quando usar

   <!-- Casos de uso, contexto adequado -->

   ## Armadilhas comuns

   <!-- O que evitar, erros frequentes -->

   ## Fontes

   - [[02-Glosas/Promovidas/<ano-decisão>/<slug-da-glosa>|<title-da-glosa>]]

   ## Aprofundamento

   <!-- Vide Template - Nota.md -->

   ## Veja também

   -
   ```

7. **Mover a glosa** (apenas se ainda na raiz):

   ```bash
   mkdir -p "02-Glosas/Promovidas/<ano-atual>"
   git mv "02-Glosas/<slug>.md" "02-Glosas/Promovidas/<ano-atual>/<slug>.md"
   ```

   Use `git mv` em vez de `mv` para preservar histórico do git.

   Se a glosa já estava em `02-Glosas/Promovidas/<ano>/`, NÃO mover de novo (idempotência).

8. **Atualizar frontmatter da glosa** com `Edit` tool:
   - `promovida_em`: append `[[03-Dominios/<X>/<Nome>]]` (lista cresce; preserva itens anteriores).
   - `updated`: hoje.
   - `progresso`: se atual é `andamento`, mudar pra `feito`.

9. **Reportar ao usuário:**

   ```
   Glosa promovida: <slug>.
   Nota criada: 03-Dominios/<X>/<Nome>.md
   Glosa movida pra: 02-Glosas/Promovidas/<ano>/<slug>.md
   ```

   Se a glosa já estava promovida (apenas append no `promovida_em`):

   ```
   Glosa <slug> já estava em Promovidas/<ano>/.
   Nova nota criada: 03-Dominios/<X>/<Nome>.md
   Glosa agora referencia <N> notas.
   ```

## Edge cases

| Caso | Comportamento |
|---|---|
| Glosa não existe | Erro claro com sugestão de listar glosas existentes |
| Glosa já em Promovidas/ | Append em `promovida_em`, não move; cria nota normalmente |
| Domínio destino não existe | Pergunta se cria. Se sim, criar `03-Dominios/<X>/index.md` mínimo antes de criar a nota |
| Nota já existe | Perguntar (a) anexar fonte, (b) outro nome, (c) cancelar |
| Conflito de nome em Promovidas | Avisar e abortar (nome de arquivo é único por construção) |
| Tags da glosa não mapeiam pra nenhum domínio | Listar TODOS os domínios disponíveis e pedir escolha |
| TL;DR vazia ou ausente | Criar nota sem comentário-TL;DR; ainda popular `## Fontes` |
| Glosa sem tags | Pedir tags pro usuário antes de criar a nota |

## Convenções

- **Nota nasce com `progresso: andamento` e `status: seedling`** — ponto de partida, não produto pronto.
- **`updated` da glosa é atualizado** em toda interação.
- **`git mv` em vez de `mv`** pra preservar histórico.
- **Nunca deletar a glosa** — sempre mover (perda zero).
- **Confirmação humana** para nome da nota e domínio destino (antes de criar arquivos).
```

- [ ] **Step 3: Validar**

```bash
head -10 "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/promover-glosa/SKILL.md"
```

Confirme que o frontmatter da skill (`name`, `description`) está correto.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/promover-glosa/SKILL.md"
git commit -m "feat(skill): adiciona /promover-glosa"
```

---

## Task 12: Skill `/sintetizar-glosas`

**Files:**
- Create: `.claude/skills/sintetizar-glosas/SKILL.md`

- [ ] **Step 1: Criar a pasta**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/sintetizar-glosas"
```

- [ ] **Step 2: Escrever o `SKILL.md`**

Use `Write` tool. Conteúdo:

```markdown
---
name: sintetizar-glosas
description: Consolida várias glosas em UMA nota nova de domínio. Cria nota com `## Fontes` populada com wikilinks pras N glosas selecionadas, move cada glosa pra `02-Glosas/Promovidas/<ano>/`, e atualiza `promovida_em` em cada uma. Use quando o usuário invocar `/sintetizar-glosas <criterio>` ou pedir pra "sintetizar glosas sobre X", "consolidar essas glosas em uma nota", "criar nota a partir de várias glosas".
---

# Skill: sintetizar-glosas

Cria UMA nota nova de domínio sintetizando VÁRIAS glosas relacionadas a um tema. A skill prepara o esqueleto da nota com a seção `## Fontes` populada com wikilinks pras glosas selecionadas; o usuário escreve a síntese em prosa própria — a skill **não** gera a síntese textual automaticamente.

## Quando usar

- Usuário invoca `/sintetizar-glosas tag:<X>` (filtro por tag).
- Usuário invoca `/sintetizar-glosas <assunto>` (busca textual).
- Usuário invoca `/sintetizar-glosas` sem argumento (modo interativo).
- Usuário diz "sintetizar glosas sobre X", "consolidar essas glosas em uma nota", "criar nota a partir de várias glosas".

## Quando NÃO usar

- Usuário quer promover apenas UMA glosa: use `/promover-glosa`.
- Usuário quer apenas listar glosas sobre um tema: skill futura `/glosas-list` ou dataview manual.

## Argumentos

| Forma | Comportamento |
|---|---|
| `/sintetizar-glosas tag:<X>` | Filtra glosas (raiz + Promovidas) com tag `<X>`. |
| `/sintetizar-glosas <assunto>` | Busca textual em `title`, `aliases`, `tags`. |
| `/sintetizar-glosas` | Modo interativo: pergunta filtro. |

## Fluxo de execução

1. **Filtrar candidatas.**
   - Se `tag:<X>`: usar Glob/Grep em `02-Glosas/**/*.md` pra encontrar arquivos com a tag (verificar frontmatter).
   - Se `<assunto>`: busca textual em `title`, `aliases`, `tags` de cada glosa.
   - Se modo interativo: pergunta filtro ao usuário.

2. **Apresentar lista pra seleção.** Cada candidata: slug, título curto, tags, status (raiz vs Promovidas).
   - Default: todas marcadas pra incluir.
   - Usuário pode tirar itens.
   - Se 0 candidatas: avisar e abortar.
   - Se 1 candidata: sugerir usar `/promover-glosa` em vez disso.

3. **Ler conteúdo de cada glosa selecionada** (TL;DR + tags + título). Use `Read` tool em cada arquivo.

4. **Sugerir domínio + nome da nota:**
   - **Domínio**: interseção das tags das glosas mapeadas pra domínios. Se múltiplos candidatos, pedir escolha.
   - **Nome**: derivar do tema comum (heurística simples — pode usar a tag mais frequente ou o assunto buscado).
   - Pedir confirmação ao usuário.

5. **Verificar se a nota já existe.** Mesma lógica de `/promover-glosa`.

6. **Criar a nota nova** em `03-Dominios/<X>/<Nome>.md`:

   ```markdown
   ---
   title: "<Nome da nota>"
   created: <hoje YYYY-MM-DD>
   updated: <hoje YYYY-MM-DD>
   type: concept
   status: seedling
   progresso: andamento
   tags:
     - <tags-consolidadas-das-glosas>
   publish: true
   ---

   # <Nome da nota>

   <!-- Síntese a partir das glosas listadas em ## Fontes. -->
   <!-- Escreva aqui a sua interpretação consolidada. -->

   ## O que é

   <!-- Definição clara e objetiva -->

   ## Como funciona

   <!-- Mecanismo, funcionamento, detalhes relevantes -->

   ## Quando usar

   <!-- Casos de uso, contexto adequado -->

   ## Armadilhas comuns

   <!-- O que evitar, erros frequentes -->

   ## Fontes

   - [[02-Glosas/Promovidas/<ano>/<slug-1>|<title-1>]]
   - [[02-Glosas/Promovidas/<ano>/<slug-2>|<title-2>]]
   - <... outras glosas selecionadas ...>

   ## Aprofundamento

   <!-- Vide Template - Nota.md -->

   ## Veja também

   -
   ```

   **Importante:** NÃO popular as outras seções com texto extraído das glosas. Síntese é voz própria do usuário; deixar comentários como guia.

7. **Mover cada glosa selecionada que ainda esteja na raiz** pra `02-Glosas/Promovidas/<ano-atual>/`. Use `git mv`. Pular glosas já em Promovidas.

8. **Atualizar `promovida_em` em cada glosa** (append do novo wikilink). Atualizar `updated` pra hoje.

9. **Reportar ao usuário:**

   ```
   Síntese criada: 03-Dominios/<X>/<Nome>.md (<N> fontes)
   Glosas movidas pra Promovidas/<ano>/:
     - <slug-1>
     - <slug-2>
     - ...
   Glosas que já estavam em Promovidas (frontmatter atualizado):
     - <slug-N>
   ```

## Edge cases

| Caso | Comportamento |
|---|---|
| 0 candidatas | Avisar e abortar |
| 1 candidata | Sugerir `/promover-glosa` em vez disso |
| Tags inconsistentes | Apresentar interseção; se vazia, união como sugestão |
| Domínio destino não existe | Mesma lógica de `/promover-glosa` (perguntar se cria) |
| Nota já existe | Perguntar anexar/outro nome/cancelar |
| Mistura de glosas (raiz + Promovidas) | OK; mover só as da raiz; atualizar frontmatter de todas |
| Conflito de nome no destino | Abortar com erro |

## Convenções

- **Skill NÃO escreve a síntese textual.** Apenas prepara `## Fontes` e o esqueleto. Síntese é voz própria.
- **Confirmação humana** antes de mover/criar.
- **`git mv`** pra preservar histórico.
- **`updated` em todas as glosas tocadas**.
```

- [ ] **Step 3: Validar**

```bash
head -10 "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/sintetizar-glosas/SKILL.md"
```

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/sintetizar-glosas/SKILL.md"
git commit -m "feat(skill): adiciona /sintetizar-glosas"
```

---

## Task 13: Skill `/arquivar-glosas`

**Files:**
- Create: `.claude/skills/arquivar-glosas/SKILL.md`

- [ ] **Step 1: Criar a pasta**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/arquivar-glosas"
```

- [ ] **Step 2: Escrever o `SKILL.md`**

Use `Write` tool. Conteúdo:

```markdown
---
name: arquivar-glosas
description: Move glosas inativas há mais de 30 dias em `02-Glosas/` raiz pra `02-Glosas/Arquivadas/<ano>/`. Inatividade = `hoje - max(updated, mtime) > 30 dias`. Aplica-se a TODAS as glosas na raiz, independente de `progresso`. Use quando o usuário invocar `/arquivar-glosas`, falar em "arquivar glosas antigas", "limpar glosas antigas", "arquivar glosas paradas".
---

# Skill: arquivar-glosas

Varre `02-Glosas/` raiz e move pra `02-Glosas/Arquivadas/<ano-atual>/` glosas que não foram modificadas nos últimos 30 dias. Pede confirmação antes de mover. Glosas em `Promovidas/` não são afetadas.

## Quando usar

- Usuário invoca `/arquivar-glosas`.
- Usuário diz "arquivar glosas antigas", "limpar glosas paradas", "arquivar glosas inativas".

## Quando NÃO usar

- Usuário quer DELETAR glosas: skill não suporta deleção (só move pra Arquivadas).
- Usuário quer reativar glosas arquivadas: use `/acordar-glosas`.

## Argumentos

Sem argumentos. A skill é uma varredura.

## Fluxo de execução

1. **Listar arquivos em `02-Glosas/` raiz.**
   - Use Glob ou `ls` em `02-Glosas/*.md`.
   - NÃO descer em `Promovidas/` ou `Arquivadas/`.
   - Excluir o `.gitkeep` se existir.

2. **Para cada glosa, calcular `idade_inativa`:**
   - Ler frontmatter, extrair `updated` (string `YYYY-MM-DD`).
   - Obter `mtime` do arquivo (use `stat` via `Bash`).
   - `data_referencia = max(parse(updated), mtime)` (a mais recente das duas).
   - `idade_inativa = hoje - data_referencia` em dias.
   - Se `updated` ausente, usar só `mtime`.

3. **Filtrar candidatas:** `idade_inativa > 30 dias`.

4. **Listar candidatas pro usuário:**

   ```
   Candidatas a arquivar (>30 dias inativas):
   1. <slug-1>  |  idade: 47d  |  tags: [react, ui]  |  progresso: feito
   2. <slug-2>  |  idade: 95d  |  tags: [ai, rag]    |  progresso: andamento
   ...
   N. <slug-N>  |  idade: 32d  |  tags: [...]        |  progresso: abandonado

   Arquivar todas? (s)im / (n)ão / (e)scolher quais
   ```

5. **Pedir confirmação:**
   - "s": arquiva todas.
   - "n": cancelar (sem ação).
   - "e": permitir desselecionar (lista de números a tirar).

6. **Mover cada confirmada** pra `02-Glosas/Arquivadas/<ano-atual>/`:

   ```bash
   mkdir -p "02-Glosas/Arquivadas/<ano-atual>"
   git mv "02-Glosas/<slug>.md" "02-Glosas/Arquivadas/<ano-atual>/<slug>.md"
   ```

   Para cada glosa movida, atualizar `updated` no frontmatter pra hoje. (Razão: registrar o evento; permite a `/acordar-glosas` filtrar por `updated` se desejado.)

7. **Reportar ao usuário:**

   ```
   Arquivadas <N> glosas em 02-Glosas/Arquivadas/<ano-atual>/:
     - <slug-1>
     - <slug-2>
     - ...
   ```

   Se nada foi arquivado: `Nenhuma glosa atendia ao critério (>30 dias inativas).`

## Edge cases

| Caso | Comportamento |
|---|---|
| Sem candidatas | Avisar "nada a arquivar" e sair sem ação |
| Pasta `Arquivadas/<ano>/` ainda não existe | Criar com `mkdir -p` |
| Conflito de nome (improvável) | Abortar com erro claro |
| `updated` no frontmatter inválido | Cair no `mtime` puro |
| Glosa em `Promovidas/` | Ignorar (skill só varre raiz) |

## Convenções

- **Critério: `idade_inativa = hoje - max(updated, mtime) > 30d`.**
- **Aplica-se a TUDO na raiz**, independente de `progresso` (`andamento`, `feito`, `abandonado` — todos são candidatos).
- **Confirmação humana obrigatória** antes de mover.
- **`git mv`** pra preservar histórico.
- **Atualiza `updated`** ao mover (registra o evento de arquivamento).
```

- [ ] **Step 3: Validar**

```bash
head -10 "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/arquivar-glosas/SKILL.md"
```

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/arquivar-glosas/SKILL.md"
git commit -m "feat(skill): adiciona /arquivar-glosas"
```

---

## Task 14: Skill `/acordar-glosas`

**Files:**
- Create: `.claude/skills/acordar-glosas/SKILL.md`

- [ ] **Step 1: Criar a pasta**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/acordar-glosas"
```

- [ ] **Step 2: Escrever o `SKILL.md`**

Use `Write` tool. Conteúdo:

```markdown
---
name: acordar-glosas
description: Reativa glosas previamente arquivadas em `02-Glosas/Arquivadas/<ano>/`. Move pra raiz `02-Glosas/`, reseta `progresso: andamento`, atualiza `updated`. Aceita filtro por slug, tag, ou assunto. Use quando o usuário invocar `/acordar-glosas <criterio>` ou pedir pra "reativar glosas sobre X", "tirar glosas do arquivo", "acordar glosas pra estudar X".
---

# Skill: acordar-glosas

Move glosas de `02-Glosas/Arquivadas/**` de volta pra raiz `02-Glosas/`, com confirmação. Útil pra retomar trabalho em um assunto previamente arquivado.

## Quando usar

- Usuário invoca `/acordar-glosas <slug>` (uma glosa específica).
- Usuário invoca `/acordar-glosas tag:<X>` (todas com tag).
- Usuário invoca `/acordar-glosas <assunto>` (busca textual).
- Usuário invoca `/acordar-glosas` (modo interativo).
- Usuário diz "reativar glosas sobre X", "tirar glosas do arquivo", "acordar glosas pra estudar X".

## Quando NÃO usar

- Usuário quer reativar glosa que foi PROMOVIDA (em `Promovidas/`): glosas promovidas são histórico imutável; edite-as in-place sem mover. Esta skill **não** mexe em `Promovidas/`.

## Argumentos

| Forma | Comportamento |
|---|---|
| `/acordar-glosas <slug>` | Reativa a glosa especificada (slug). |
| `/acordar-glosas tag:<X>` | Reativa todas as glosas em `Arquivadas/` com a tag. |
| `/acordar-glosas <assunto>` | Busca textual em `title`, `aliases`, `tags`. |
| `/acordar-glosas` | Modo interativo: pergunta filtro. |

## Fluxo de execução

1. **Filtrar candidatas em `02-Glosas/Arquivadas/**`** (recursivo, todos os anos).
   - Se `<slug>`: localizar arquivo. Erro se não existir.
   - Se `tag:<X>`: percorrer arquivos, ler frontmatter, filtrar por tag.
   - Se `<assunto>`: busca textual em `title`, `aliases`, `tags`.
   - Se modo interativo: perguntar filtro.

2. **Listar candidatas pro usuário:**

   ```
   Candidatas a acordar:
   1. <slug-1>  |  arquivada: 2025/  |  tags: [react, ui]   |  updated: 2025-08-12
   2. <slug-2>  |  arquivada: 2026/  |  tags: [ai, rag]     |  updated: 2026-02-03
   ...

   Acordar todas? (s)im / (n)ão / (e)scolher quais
   ```

3. **Pedir confirmação:**
   - "s": acordar todas.
   - "n": cancelar.
   - "e": desselecionar.

4. **Para cada confirmada:**

   ```bash
   git mv "02-Glosas/Arquivadas/<ano>/<slug>.md" "02-Glosas/<slug>.md"
   ```

   Verificar conflito: se `02-Glosas/<slug>.md` já existe na raiz, abortar com erro pra esta glosa específica e seguir com as demais.

5. **Atualizar frontmatter de cada glosa acordada:**
   - `progresso`: resetar pra `andamento`.
   - `updated`: hoje.

6. **Reportar ao usuário:**

   ```
   Acordadas <N> glosas (movidas pra raiz com progresso: andamento):
     - <slug-1>
     - <slug-2>
     ...
   ```

   Se houve conflitos:

   ```
   Conflitos (não foi possível acordar):
     - <slug-X>: já existe arquivo de mesmo nome em 02-Glosas/. Inspecionar manualmente.
   ```

## Edge cases

| Caso | Comportamento |
|---|---|
| Glosa não está arquivada | Erro claro com sugestão de listar arquivadas |
| 0 candidatas | "Nenhuma glosa arquivada com esse critério" |
| Conflito de nome na raiz | Abortar pra esta glosa, seguir com outras; reportar conflito |
| Glosa em `Promovidas/` | Ignorar (skill só atua em `Arquivadas/`); explicar |

## Convenções

- **Skill atua APENAS em `Arquivadas/`** — `Promovidas/` é histórico imutável.
- **Reset de `progresso: andamento`** ao acordar (assume que vai trabalhar).
- **`updated` atualizado** pra registrar evento.
- **`git mv`** pra preservar histórico.
- **Confirmação humana obrigatória.**
```

- [ ] **Step 3: Validar**

```bash
head -10 "/home/josenaldo/repos/personal/codex-technomanticus/.claude/skills/acordar-glosas/SKILL.md"
```

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/acordar-glosas/SKILL.md"
git commit -m "feat(skill): adiciona /acordar-glosas"
```

---

## Task 15: Validação manual end-to-end

**Files:**
- (nenhum — apenas validação interativa)

> Esta task é executada pelo usuário (você precisa do Obsidian aberto e do Claude Code). Tasks 1-14 entregaram a infraestrutura; aqui validamos que ela funciona.

- [ ] **Step 1: Criar 2 glosas de teste**

No Claude Code, executar (com URLs reais que produzem glosas distintas, mesma tag):

```
/glosa https://example.com/artigo-test-rag-1
/glosa https://example.com/artigo-test-rag-2
```

(Substituir pelas URLs reais — ou criar glosas-stub manualmente em `02-Glosas/2026-test-1.md` e `02-Glosas/2026-test-2.md` com tag `rag-test`.)

Verificar:
- Glosas criadas em `02-Glosas/`.
- Frontmatter inclui `created`, `updated`, `progresso: andamento`, `promovida_em: []`.

- [ ] **Step 2: Testar `/promover-glosa`**

```
/promover-glosa 2026-test-1
```

Acompanhar fluxo interativo:
- Skill pergunta domínio destino.
- Skill pergunta nome da nota.
- Skill cria nota.
- Skill move glosa pra `Promovidas/2026/`.

Validar:
- Nota criada em `03-Dominios/<X>/<Nome>.md`.
- Frontmatter da nota: `progresso: andamento`, `status: seedling`.
- Seção `## Fontes` da nota tem wikilink pra glosa.
- Glosa em `02-Glosas/Promovidas/2026/2026-test-1.md`.
- Frontmatter da glosa: `promovida_em: ["[[03-Dominios/<X>/<Nome>]]"]`, `updated: hoje`, `progresso: feito`.

- [ ] **Step 3: Testar `/sintetizar-glosas`**

Criar mais uma glosa-stub (`2026-test-3.md` com tag `rag-test`) pra ter 2 candidatas (test-2 e test-3, já que test-1 foi promovida e moveu).

```
/sintetizar-glosas tag:rag-test
```

Validar:
- Skill lista as 2 candidatas (test-2 + test-3).
- Confirmar a seleção.
- Skill cria nota nova com `## Fontes` apontando pras 2 glosas.
- Ambas glosas movidas pra `Promovidas/2026/`.
- `promovida_em` populado em ambas.

- [ ] **Step 4: Testar `/arquivar-glosas`**

Criar uma glosa-stub `2026-test-arquivar.md` com `mtime` antigo (>30 dias). Pra simular, edite o frontmatter `updated` pra uma data passada (ex.: `updated: 2026-03-01`).

```bash
# Forçar mtime antigo
touch -d "2026-03-01" "02-Glosas/2026-test-arquivar.md"
```

Executar:
```
/arquivar-glosas
```

Validar:
- Skill lista a glosa de teste como candidata.
- Confirmar.
- Glosa movida pra `02-Glosas/Arquivadas/2026/`.

- [ ] **Step 5: Testar `/acordar-glosas`**

```
/acordar-glosas 2026-test-arquivar
```

Validar:
- Skill lista a glosa.
- Confirmar.
- Glosa volta pra raiz `02-Glosas/2026-test-arquivar.md`.
- `progresso: andamento` resetado.
- `updated` atualizado pra hoje.

- [ ] **Step 6: Limpeza**

Apagar todas as glosas e notas de teste criadas:
- `02-Glosas/2026-test-arquivar.md`
- `02-Glosas/Promovidas/2026/2026-test-1.md`, `2026-test-2.md`, `2026-test-3.md`
- Notas de domínio criadas pelas skills (em `03-Dominios/<X>/`)

```bash
# Listar pra confirmar antes de remover
git status

# Reverter (não commitado ainda):
git checkout -- <files-to-revert>
git clean -fd "02-Glosas/" "03-Dominios/"
```

Não commit. Esta task é apenas validação.

- [ ] **Step 7: Reportar resultado**

Resumir o que funcionou e o que não funcionou. Se algo falhou, criar issue / followup task. Se tudo funcionou, marcar a task como completa.

---

## Self-Review

### Spec coverage

| Item da spec | Task que implementa |
|---|---|
| §4.1 Glosa vs nota | Task 5 (index), Task 7 (Glosas), Task 8 (Domínios) |
| §4.2 Vínculo bidirecional (`promovida_em`, `## Fontes`) | Task 1, Task 2, Tasks 11-12 |
| §4.3 Ciclo de vida da glosa | Task 7 (Glosas docs), Tasks 11-14 (skills) |
| §4.4 Nota nasce em estado preliminar | Tasks 11-12 (skills criam com `andamento`/`seedling`) |
| §5.1 `Template - Glosa.md` atualizado | Task 1 |
| §5.2 `Template - Nota.md` com `## Fontes` | Task 2 |
| §5.3 Migração da glosa existente | Task 3 |
| §6 Estrutura física (`Promovidas/`, `Arquivadas/`) | Task 4 |
| §7 Critério temporal | Task 13 (skill `/arquivar-glosas`) |
| §8.1 `/promover-glosa` | Task 11 |
| §8.2 `/sintetizar-glosas` | Task 12 |
| §8.3 `/arquivar-glosas` | Task 13 |
| §8.4 `/acordar-glosas` | Task 14 |
| §9 Reorganização do guia | Tasks 5-10 |
| §11 Plano de execução | Tasks 1-15 cobrem todos os 11 passos numerados da spec |
| §14 Aceitação | Task 15 (validação manual) |

Coberto. Itens fora de escopo (§13 trabalhos subsequentes) não têm tasks aqui — corretos.

### Placeholder scan

Sem `TBD` / `TODO` / "implement later". Tasks 11-14 contêm SKILL.md completos com fluxo de execução detalhado. Task 15 (validação) tem steps de simulação concretos.

### Type consistency

- `progresso` valores: `pendente | andamento | feito | pausado | abandonado` — consistente em templates, glosas, notas, e descrições de skill.
- `promovida_em`: lista de wikilinks `[[03-Dominios/X/Y]]` — consistente em todas as referências.
- Estrutura de pastas: `02-Glosas/Promovidas/<ano>/`, `02-Glosas/Arquivadas/<ano>/` — consistente em descrições e operações `git mv`.
- Critério temporal: `max(updated, mtime) > 30 dias` — consistente em spec, em Task 13.
- Skills: nomes `promover-glosa`, `sintetizar-glosas`, `arquivar-glosas`, `acordar-glosas` — consistentes em todas as referências.
- Templates: `00-Meta/templates/Template - Glosa.md` (com espaços e hífen) — consistente.

Plano íntegro.
