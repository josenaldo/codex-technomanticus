# Tracking de progresso nas sendas — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Estabelecer infraestrutura de tracking de progresso de estudo nas sendas do Codex Technomanticus, com modelo conceitual canon (domínios = estantes, sendas = fluxograma), campo `progresso` no frontmatter, callout `[!convite]` para externos, e piloto na Senda Frontend.

**Architecture:** Conjunto de convenções markdown + Obsidian (frontmatter, dataview, callouts) sem código de runtime. Estado factual no vault público; visões agregadas/narrativas ficam pro apocrypha (fora deste plano). Site Quartz consome o vault via symlink; precisa de SCSS adicional pro novo callout.

**Tech Stack:** Markdown + YAML frontmatter, plugin Dataview (DQL) do Obsidian, Quartz v4 (SCSS).

**Spec:** `docs/superpowers/specs/2026-05-03-progresso-sendas-design.md`

---

## File Structure

### Repo `codex-technomanticus` (público)

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `00-Meta/guia/sendas-e-dominios.md` | Create | Documenta o modelo conceitual: domínios = estantes, sendas = fluxograma; campo `progresso`; convite `[!convite]`. |
| `00-Meta/templates/Template - Nota.md` | Modify | Adicionar `progresso: pendente` no frontmatter; seção opcional `## Aprofundamento` com exemplo comentado. |
| `00-Meta/templates/Template - Glosa.md` | Modify | Adicionar `progresso: feito` no frontmatter (glosa nasce já lida — vide nota na Task 4). |
| `00-Meta/templates/trail.md` | Modify (substituir) | Substituir conteúdo pelo template canônico de senda (frontmatter completo, formas minimal/structured, bloco dataview). |
| `03-Dominios/Tecnologia/Frontend/index.md` | Create | Estante de engenharia frontend (disciplina cross-tech). |
| `03-Dominios/Tecnologia/React/index.md` | Create | Estante React. |
| `03-Dominios/Tecnologia/TypeScript/index.md` | Create | Estante TypeScript. |
| `03-Dominios/<outras estantes>/index.md` | Create (conforme auditoria) | Estantes adicionais necessárias pelo piloto (CSS, HTML, etc.). |
| `03-Dominios/<estantes>/<notas-stub>.md` | Create (conforme auditoria) | Notas-stub mapeadas a partir do conteúdo da Senda Frontend atual. |
| `04-Sendas/Senda Frontend.md` | Modify (reescrever) | Reescrever no template canônico, apenas wikilinks ordenados, com bloco dataview. |

### Repo `codex-technomanticus-site` (Quartz)

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `quartz/styles/callouts.scss` | Modify | Adicionar variável `--callout-icon-convite` e bloco `&[data-callout="convite"]` com cor/ícone próprios. |

### Repo `codex-technomanticus-apocrypha`

**Não tocar.** Pendências catalogadas em `docs/apocrypha-pendencias.md` (público).

---

## Notas pro implementador

- **Sem testes unitários**: o "sistema" é convenção markdown + plugin Dataview. "Validação" = abrir no Obsidian e ver se renderiza/agrega corretamente; rodar build do Quartz pra ver renderização do site.
- **Trabalho em duas pastas**: a maior parte fica em `codex-technomanticus`; uma task é em `codex-technomanticus-site`. Cada repo tem seu próprio git.
- **Commits frequentes**: cada task termina com commit. Use mensagens em português, no estilo dos commits recentes (ex.: `feat: ...`, `docs: ...`, `chore: ...`). Não usar `Co-Authored-By: Claude` (preferência do usuário).
- **Auditoria interativa**: a Task 10 (mapeamento da Senda Frontend) é interativa — exige decisões do usuário sobre quais conceitos viram quais notas. Não pré-popular sem alinhar.
- **Caracteres especiais**: a estrutura usa `Domínios` com acento e ç. Wikilinks/paths preservam.
- **Datas**: a data de hoje é 2026-05-03. Use isso em campos `created` ao criar arquivos novos.

---

## Task 1: Documentação do modelo conceitual (guia)

**Files:**
- Create: `00-Meta/guia/sendas-e-dominios.md`

- [ ] **Step 1: Verificar o padrão dos arquivos existentes em `00-Meta/guia/`**

```bash
ls /home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/
head -20 "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/guia/Como usar este vault.md"
```
Expected: lista de arquivos do guia, e frontmatter padrão (provavelmente `type: moc` ou similar, `publish: true`).

- [ ] **Step 2: Criar o arquivo `00-Meta/guia/sendas-e-dominios.md`**

```markdown
---
title: "Sendas e Domínios — modelo canônico"
type: moc
publish: true
created: 2026-05-03
updated: 2026-05-03
tags:
  - guia
  - vault
  - canon
---

# Sendas e Domínios — modelo canônico

Este documento define como notas, domínios e sendas se relacionam no Codex.

## As quatro zonas

| Zona | Papel |
|---|---|
| `01-Pergaminhos/` | Captura inicial: inbox, links soltos, ideias cruas. |
| `02-Glosas/` | Fichamentos de materiais externos consumidos. |
| `03-Dominios/` | Corpus do conhecimento. **Centro gravitacional do vault**. Notas amadurecidas, organizadas por domínio. |
| `04-Sendas/` | Mapas de leitura. Wikilinks ordenados pra notas dos domínios. **Apenas isso**. |

**Pipeline de alimentação:** pergaminho → glosa → nota de domínio.

## Domínios = estantes; Sendas = fluxograma

- **Domínios** são estantes de livros: corpus de conhecimento sobre um tema. Notas, materiais externos contextualizados (via callout `[!convite]`), exercícios, projetos — tudo aqui.
- **Sendas** são fluxogramas de faculdade: indicam a ordem de leitura das notas (livros) das estantes. Não contêm conhecimento próprio; apenas referenciam.

### Uma senda **não** contém

- Texto explicativo de conceitos (vai pra nota do domínio).
- Links externos a artigos, vídeos, livros, cursos (vão pra notas de domínio, dentro de callouts `[!convite]`, ou viram glosas).
- Exercícios, projetos, checkpoints conceituais (vão pro domínio).
- Wikilinks pra headings internos do próprio arquivo.

### Uma senda **contém**

- Frontmatter com metadados.
- Descrição curta da senda (pra quem é, qual o destino).
- Pré-requisitos (wikilinks pra notas de outros domínios).
- Sequência ordenada de wikilinks pra notas do domínio principal (forma plana ou em fases).
- Bloco dataview de agregação de progresso.

## Organização dos domínios (modelo de estantes)

Cada domínio é uma estante coerente: uma área de conhecimento com vocabulário próprio, comunidade própria, ferramental próprio.

- **Linguagens próprias** ganham estante própria: `JavaScript/` (apenas core), `TypeScript/`, `HTML/`, `CSS/`, `Java/`, `Python/`, `Go/`.
- **Bibliotecas/frameworks grandes** ganham estante própria: `React/`, `Vue/`, `Svelte/`, `HTMX/`. Bibliotecas menores moram como notas dentro do domínio mais relevante.
- **Disciplinas (cross-tech)** ganham estante própria: `Frontend/` é a estante de **engenharia frontend** — arquitetura, performance, acessibilidade, padrões.
- **Ferramentas** vão pra `Ferramentas/` (tooling cross-tech: Vite, bundlers, monorepos).

Sendas atravessam estantes naturalmente.

## Campo `progresso` no frontmatter

Toda nota de domínio (e toda glosa) tem o campo `progresso`:

```yaml
progresso: pendente | andamento | feito | pausado | abandonado
```

| Valor | Significado |
|---|---|
| `pendente` | Ainda não comecei. Default quando o campo está ausente. |
| `andamento` | Estou estudando ativamente. |
| `feito` | Concluí o estudo dessa nota; conteúdo absorvido. |
| `pausado` | Comecei e parei intencionalmente; pretendo retomar. |
| `abandonado` | Decidi não estudar; fora do meu radar. |

`progresso` é **ortogonal** a `status` (maturidade da nota: `seedling`/`budding`/`evergreen`). São dois eixos independentes.

## Callout `[!convite]`

Materiais externos (artigos, vídeos, cursos) são apresentados dentro de notas de domínio como **convites a aprofundamento**:

```markdown
> [!convite] Aprofundamento — <tema>
> - [Texto do link](https://...) — autor/origem
> - Outro item
>
> Consumiu? Faça uma glosa em `02-Glosas/` e amadureça pro domínio quando fizer sentido.
```

Convite é convite: opcional, sem `progresso` próprio. Quando o usuário consome o material, cria uma glosa, e a glosa carrega o `progresso`.

## Ver também

- [[Como usar este vault]]
- [[Convenções de escrita]]
- [[Decisões do vault]]
- [[Wikilinks e MOCs]]
```

- [ ] **Step 3: Validar que o arquivo abre no Obsidian e segue o padrão dos outros do guia**

Comparar visualmente com `00-Meta/guia/Como usar este vault.md` no Obsidian. Frontmatter, headings, links — tudo coerente?

- [ ] **Step 4: Commit**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add "00-Meta/guia/sendas-e-dominios.md"
git commit -m "docs(guia): modelo canônico de sendas e domínios"
```

---

## Task 2: Atualizar `Template - Nota.md`

**Files:**
- Modify: `00-Meta/templates/Template - Nota.md`

- [ ] **Step 1: Ler o arquivo atual**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Nota.md"
```

Expected: frontmatter com `title`, `created`, `updated`, `type: concept`, `status: seedling`, `tags`, `publish: false`. Conteúdo: seções "O que é", "Como funciona", "Quando usar", "Armadilhas comuns", "Veja também".

- [ ] **Step 2: Adicionar `progresso: pendente` no frontmatter**

Editar o arquivo. Frontmatter final deve ficar:

```yaml
---
title: "<% tp.file.title %>"
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
type: concept
status: seedling
progresso: pendente
tags:
  -
publish: false
---
```

`progresso: pendente` vai logo após `status: seedling`.

- [ ] **Step 3: Adicionar seção `## Aprofundamento` no fim do template**

Editar o arquivo. Antes de `## Veja também` (que é a última seção), adicionar:

```markdown
## Aprofundamento

<!--
Se houver materiais externos relevantes pra aprofundar este conceito, liste-os
como convite. Estrutura:

> [!convite] <Título do aprofundamento>
> - [Texto do link](https://...) — autor/origem
> - Outro item
>
> Consumiu? Faça uma glosa em `02-Glosas/` e amadureça pro domínio quando fizer sentido.

Apague esta seção se a nota não tiver convites.
-->

```

- [ ] **Step 4: Validar que o template renderiza no Obsidian**

Criar uma nota nova de teste com Templater (Ctrl+P → "Templater: Create new note from template") e verificar:
1. O frontmatter inclui `progresso: pendente`.
2. A seção `## Aprofundamento` aparece com o comentário HTML explicativo.
3. Apagar a nota de teste após validar.

- [ ] **Step 5: Commit**

```bash
git add "00-Meta/templates/Template - Nota.md"
git commit -m "feat(templates): adiciona campo progresso e seção Aprofundamento em notas"
```

---

## Task 3: Atualizar `Template - Glosa.md`

**Files:**
- Modify: `00-Meta/templates/Template - Glosa.md`

> **Nota importante pro implementador:** A spec original (§5.3) sugeria glosa nascendo com `progresso: andamento`. Revisando o fluxo real: a skill `/glosa` cria a glosa **após** a leitura (campo `read: <% tp.date.now %>` no template atual), então `progresso: feito` é mais coerente. Confirmar com o usuário antes de implementar; ajustar se necessário.

- [ ] **Step 1: Confirmar com o usuário o valor inicial de `progresso` em glosas**

Pergunta: "Glosa nasce com `progresso: feito` (porque a skill /glosa cria após a leitura) ou com `progresso: andamento` (caso o usuário esteja escrevendo enquanto lê)?"

Aguardar resposta antes de seguir. Default sugerido: `feito`.

- [ ] **Step 2: Ler o arquivo atual**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/Template - Glosa.md"
```

Expected: frontmatter com `title`, `aliases`, `source`, `author`, `site`, `published`, `read`, `type: glosa`, `status: lido`, `tags`, `lang`, `publish: false`.

- [ ] **Step 3: Adicionar `progresso: <valor confirmado>` no frontmatter**

Editar logo após `status: lido`:

```yaml
status: lido
progresso: feito  # ou "andamento" conforme decisão da Step 1
```

- [ ] **Step 4: Validar que o template renderiza no Obsidian**

Criar uma glosa de teste (via skill `/glosa <url>` ou via Templater) e verificar que `progresso` aparece. Apagar após validar.

- [ ] **Step 5: Commit**

```bash
git add "00-Meta/templates/Template - Glosa.md"
git commit -m "feat(templates): adiciona campo progresso em glosas"
```

---

## Task 4: Substituir `00-Meta/templates/trail.md` pelo template canônico

**Files:**
- Modify (substituir): `00-Meta/templates/trail.md`

- [ ] **Step 1: Ler o arquivo atual pra referência**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/00-Meta/templates/trail.md"
```

Expected: template mínimo com `type: trail`, `title`, `description`, `level`, `prerequisites`, `tags`, `status`, `created`. Conteúdo: "## Goal", "## Modules".

- [ ] **Step 2: Substituir todo o conteúdo pelo template canônico**

Conteúdo final do arquivo (com Templater):

````markdown
---
type: trail
title: "Senda <% tp.file.title %>"
domain: "[[03-Dominios/<Domínio>/index]]"
maturity: minimal
status: active
publish: true
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - senda
---

# Senda <% tp.file.title %>

> Pra quem é, qual o destino, em quanto tempo.

## Pré-requisitos

- [[03-Dominios/<Outro Domínio>/<nota>]]

## Sequência

<!--
Versão MINIMAL (lista plana ordenada). Use esta forma se a senda é direta
e não precisa ser dividida em fases.
-->

1. [[03-Dominios/<Domínio>/<Nota A>]]
2. [[03-Dominios/<Domínio>/<Nota B>]]
3. [[03-Dominios/<Domínio>/<Nota C>]]

<!--
Versão STRUCTURED (com fases). Comente a "## Sequência" acima e descomente
o bloco abaixo. Atualize o frontmatter pra `maturity: structured`.

## Fase 0 — <Tema>

1. [[03-Dominios/<Domínio>/<Nota A>]]
2. [[03-Dominios/<Domínio>/<Nota B>]]

## Fase 1 — <Tema>

1. [[03-Dominios/<Domínio>/<Nota C>]]
-->

## Progresso

```dataview
TABLE WITHOUT ID
  file.link AS "Nota",
  default(progresso, "pendente") AS "Status"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
SORT file.name ASC
```

**Resumo:**

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "feito")) AS "Feitas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "andamento")) AS "Em andamento",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pausado")) AS "Pausadas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pendente")) AS "Pendentes"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
GROUP BY true
```
````

- [ ] **Step 3: Validar que o template renderiza no Obsidian**

Criar uma senda de teste (via Templater) e verificar:
1. Frontmatter renderiza corretamente.
2. Bloco dataview executa (mesmo que vazio, sem erros).
3. Estrutura de fases comentada está disponível.

Apagar após validar.

- [ ] **Step 4: Commit**

```bash
git add "00-Meta/templates/trail.md"
git commit -m "feat(templates): template canônico de senda com dataview de progresso"
```

---

## Task 5: Adicionar callout `convite` ao SCSS do Quartz

**Files:**
- Modify: `/home/josenaldo/repos/personal/codex-technomanticus-site/quartz/styles/callouts.scss`

> **Nota:** Esta task é em outro repo (`codex-technomanticus-site`). Ela é independente das tasks do vault — pode ser executada em paralelo ou em sessão separada.

- [ ] **Step 1: Localizar a região correta para inserção**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-site
grep -n "callout-icon-quote\|data-callout=\"quote\"" quartz/styles/callouts.scss
```
Expected: encontrar a definição de `--callout-icon-quote` (perto da linha 34) e o bloco `&[data-callout="quote"]` mais abaixo. O callout `convite` será adicionado no estilo desses dois.

- [ ] **Step 2: Adicionar a variável `--callout-icon-convite`**

Logo após a linha que define `--callout-icon-fold` (perto da linha 35), adicionar:

```scss
  --callout-icon-convite: url('data:image/svg+xml; utf8, <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>');
```

(Esse é o ícone "settings/portal" do Lucide, simbolizando portal/convite. Pode ser substituído por outro SVG com mesma estrutura `data:image/svg+xml; utf8, <svg ...></svg>` se o usuário preferir.)

- [ ] **Step 3: Adicionar o bloco de regras `&[data-callout="convite"]`**

Localizar o último bloco `&[data-callout="..."]` no arquivo (provavelmente em torno da linha 180-187). Adicionar o novo bloco logo após:

```scss
  &[data-callout="convite"] {
    --color: #9c27b0;
    --border: #9c27b044;
    --bg: #9c27b010;
    --callout-icon: var(--callout-icon-convite);
  }
```

(Cor roxa/violeta — combina com a estética tecnomância. Cor pode ser ajustada conforme paleta do tema.)

- [ ] **Step 4: Validar build local do Quartz**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-site
npx quartz build
```
Expected: build completa sem erros relacionados ao SCSS.

- [ ] **Step 5: Validar visualmente**

```bash
npx quartz build --serve
```
Abrir `http://localhost:8080` e navegar até uma página com callout `[!convite]` (depois das Tasks 8-12 estarem prontas, ou criar uma nota de teste local). Verificar que renderiza com cor roxa e ícone próprio.

Se ainda não houver nenhum callout `[!convite]` no vault: validação visual fica pendente até a Task 11+.

- [ ] **Step 6: Commit**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-site
git add quartz/styles/callouts.scss
git commit -m "feat(callouts): adiciona estilo do callout 'convite'"
```

---

## Task 6: Criar estante `Frontend/` (engenharia)

**Files:**
- Create: `03-Dominios/Tecnologia/Frontend/index.md`

- [ ] **Step 1: Verificar se a pasta já existe**

```bash
ls "/home/josenaldo/repos/personal/codex-technomanticus/03-Dominios/Tecnologia/Frontend/" 2>/dev/null
```
Expected: erro ("No such file or directory") ou pasta vazia. Se houver conteúdo legado, **parar e alinhar com o usuário**.

- [ ] **Step 2: Criar a pasta e o `index.md`**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/03-Dominios/Tecnologia/Frontend"
```

Escrever `03-Dominios/Tecnologia/Frontend/index.md`:

```markdown
---
title: "Frontend"
type: moc
publish: true
created: 2026-05-03
updated: 2026-05-03
status: seedling
progresso: pendente
tags:
  - frontend
  - moc
  - engenharia
aliases:
  - Engenharia Frontend
  - Frontend Engineering
---

# Frontend

Estante de **engenharia frontend** — disciplina cross-tecnologia. Cobre arquitetura de apps, performance, acessibilidade, padrões de UI, responsividade, design systems, e práticas de qualidade no client-side.

> [!info] O que **não** está aqui
> Tecnologias específicas têm estantes próprias:
> - Linguagens e libs: [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]], [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]], [[03-Dominios/HTML/index|HTML]], [[03-Dominios/CSS/index|CSS]]
> - Frameworks/UI: [[03-Dominios/Tecnologia/React/index|React]], (futuras: Vue, Svelte, HTMX)
> - Tooling: [[03-Dominios/Tecnologia/Ferramentas/index|Ferramentas]] (Vite, bundlers, monorepos)
>
> Aqui mora o que **é frontend mesmo quando trocamos a tecnologia**.

## Conteúdo

(notas serão adicionadas conforme amadurecimento)

## Veja também

- [[Senda Frontend]]
```

- [ ] **Step 3: Validar no Obsidian**

Abrir a nota no Obsidian. Verificar:
1. Frontmatter renderiza.
2. Wikilinks aparecem (mesmo que apontem pra notas que ainda não existem — Obsidian permite "links não resolvidos").

- [ ] **Step 4: Commit**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git add "03-Dominios/Tecnologia/Frontend/index.md"
git commit -m "feat(domínios): cria estante Frontend (engenharia)"
```

---

## Task 7: Criar estante `React/`

**Files:**
- Create: `03-Dominios/Tecnologia/React/index.md`

- [ ] **Step 1: Criar a pasta e o `index.md`**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/03-Dominios/Tecnologia/React"
```

Escrever `03-Dominios/Tecnologia/React/index.md`:

```markdown
---
title: "React"
type: moc
publish: true
created: 2026-05-03
updated: 2026-05-03
status: seedling
progresso: pendente
tags:
  - react
  - moc
aliases:
  - ReactJS
  - React.js
---

# React

Estante de React: a biblioteca, seu ecossistema, frameworks que rodam sobre ela (Next.js, Remix), bibliotecas de UI (MUI, Mantine), gerenciamento de formulários e estado, padrões e idiomas.

## Conteúdo

(notas serão adicionadas conforme amadurecimento)

## Veja também

- [[Senda Frontend]]
- [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]]
- [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]]
```

- [ ] **Step 2: Validar no Obsidian**

Abrir e verificar renderização.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/React/index.md"
git commit -m "feat(domínios): cria estante React"
```

---

## Task 8: Criar estante `TypeScript/`

**Files:**
- Create: `03-Dominios/Tecnologia/TypeScript/index.md`

- [ ] **Step 1: Criar a pasta e o `index.md`**

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/03-Dominios/Tecnologia/TypeScript"
```

Escrever `03-Dominios/Tecnologia/TypeScript/index.md`:

```markdown
---
title: "TypeScript"
type: moc
publish: true
created: 2026-05-03
updated: 2026-05-03
status: seedling
progresso: pendente
tags:
  - typescript
  - moc
aliases:
  - TS
---

# TypeScript

Estante de TypeScript: tipos, generics, inferência, type narrowing, utility types, padrões idiomáticos, configuração (`tsconfig.json`), interoperabilidade com JavaScript.

## Conteúdo

(notas serão adicionadas conforme amadurecimento)

## Veja também

- [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]]
- [[Senda Frontend]]
```

- [ ] **Step 2: Validar no Obsidian**

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Tecnologia/TypeScript/index.md"
git commit -m "feat(domínios): cria estante TypeScript"
```

---

## Task 9: Auditar Senda Frontend e mapear conteúdo (interativa)

**Files:**
- Read: `04-Sendas/Senda Frontend.md`

> **Esta task é interativa — exige decisões do usuário sobre cada item.** Não pré-popular. Apresentar o mapeamento e aguardar confirmação antes de prosseguir.

- [ ] **Step 1: Reler a Senda Frontend atual e enumerar cada link/seção**

```bash
cat "/home/josenaldo/repos/personal/codex-technomanticus/04-Sendas/Senda Frontend.md"
```

Catalogar:
- Cada heading (`# React`, `# Frameworks`, etc.) → vai virar nota de domínio?
- Cada link externo (URLs `https://...`) → vira convite em qual nota? Ou é descartado?
- Cada wikilink interno (`[[#...]]`) → não é wikilink real (aponta a heading deste arquivo); descartar.

Saída esperada: tabela com colunas:
| Item original | Tipo | Destino sugerido |
|---|---|---|
| React (heading + links docs) | heading | `03-Dominios/Tecnologia/React/index.md` (já existe) — adicionar links no convite |
| TanStack Query (subheading + links profy.dev) | nota nova | `03-Dominios/Tecnologia/React/TanStack Query.md` |
| ... | ... | ... |

- [ ] **Step 2: Apresentar a tabela ao usuário e iterar**

Mostrar a tabela. Perguntar:
- Algum item deve virar nota numa estante diferente (ex.: NextJS pode ser nota em React/, ou estante própria `NextJS/`)?
- Algum item deve ser **descartado** (link morto, irrelevante hoje)?
- Algum item exige uma estante adicional ainda não criada (ex.: `HTML/`, `CSS/`)?

Aguardar confirmação. Atualizar a tabela conforme feedback.

- [ ] **Step 3: Salvar o mapeamento aprovado em arquivo de trabalho**

Salvar em `docs/superpowers/plans/2026-05-03-progresso-sendas-mapeamento-frontend.md` (não-versionado da spec, é trabalho interno):

```markdown
# Mapeamento da Senda Frontend (auditoria 2026-05-03)

| Item original | Tipo | Destino |
|---|---|---|
| ... | ... | ... |
```

(Esse arquivo é referência pras tasks 10-13. Não precisa ser commitado, mas pode ser pra rastreabilidade.)

- [ ] **Step 4: Commit (opcional, se decidir versionar o mapeamento)**

```bash
git add docs/superpowers/plans/2026-05-03-progresso-sendas-mapeamento-frontend.md
git commit -m "docs(plano): mapeamento da Senda Frontend pra novas estantes"
```

---

## Task 10: Criar estantes adicionais identificadas na auditoria

**Files:**
- Create: `03-Dominios/HTML/index.md` (se necessário)
- Create: `03-Dominios/CSS/index.md` (se necessário)
- Create: outras `03-Dominios/<X>/index.md` conforme Task 9

> **Esta task é condicional**: só rode se a auditoria da Task 9 identificou estantes adicionais necessárias.

- [ ] **Step 1: Para cada estante adicional identificada, criar pasta e index.md**

Padrão (substituir `<X>`, descrição, aliases conforme apropriado):

```bash
mkdir -p "/home/josenaldo/repos/personal/codex-technomanticus/03-Dominios/<X>"
```

Conteúdo:

```markdown
---
title: "<X>"
type: moc
publish: true
created: 2026-05-03
updated: 2026-05-03
status: seedling
progresso: pendente
tags:
  - <tag-x>
  - moc
---

# <X>

<descrição em uma frase>

## Conteúdo

(notas serão adicionadas conforme amadurecimento)

## Veja também

- [[Senda Frontend]]
```

- [ ] **Step 2: Validar no Obsidian**

- [ ] **Step 3: Commit (uma estante por commit OU agrupado)**

```bash
git add "03-Dominios/<X>/index.md"
git commit -m "feat(domínios): cria estante <X>"
```

---

## Task 11: Criar notas-stub conforme mapeamento

**Files:**
- Create: várias notas em `03-Dominios/<estantes>/<conceito>.md`

> Use o mapeamento da Task 9. Cada conceito identificado vira uma nota-stub.

- [ ] **Step 1: Para cada nota-stub a criar, usar o template padrão**

Aplicar o `Template - Nota.md` (atualizado na Task 2). Cada nota nasce com:

```yaml
---
title: "<Nome do conceito>"
created: 2026-05-03
updated: 2026-05-03
type: concept
status: seedling
progresso: pendente  # ou "andamento" se o usuário já está estudando
tags:
  - <tag-domínio>
publish: true
---

# <Nome do conceito>

<!-- Uma frase descrevendo do que se trata esta nota -->

## O que é

<!-- Definição clara e objetiva -->

## Como funciona

<!-- Mecanismo, funcionamento, detalhes relevantes -->

## Quando usar

<!-- Casos de uso, contexto adequado -->

## Armadilhas comuns

<!-- O que evitar, erros frequentes -->

## Aprofundamento

> [!convite] <Título do aprofundamento>
> - [<Texto do link>](https://...) — autor/origem
>
> Consumiu? Faça uma glosa em `02-Glosas/` e amadureça pro domínio quando fizer sentido.

## Veja também

-
```

- [ ] **Step 2: Mover os links externos do mapeamento (Task 9) pra dentro do callout `[!convite]` da nota apropriada**

Para cada link externo enumerado, posicionar dentro do `> [!convite]` da nota correspondente. Manter títulos e autores dos links.

Notas que **não** tinham links externos correspondentes ficam com a seção `## Aprofundamento` removida (ou comentada).

- [ ] **Step 3: Validar cada nota no Obsidian**

Abrir 2-3 notas-stub criadas. Verificar:
1. Frontmatter completo (`progresso`, `status`, etc.).
2. Callout `[!convite]` renderiza com estilo (no Obsidian — pode ser estilo genérico até a Task 5 ser deployada).
3. Wikilinks da seção "Veja também" e do callout funcionam.

- [ ] **Step 4: Commit (uma nota por commit OU agrupado por estante)**

Sugestão: uma estante por commit, agrupando notas relacionadas.

```bash
git add "03-Dominios/Tecnologia/React/"
git commit -m "feat(domínios/react): notas-stub de TanStack, NextJS, MUI, ..."
```

---

## Task 12: Reescrever a Senda Frontend com template canônico

**Files:**
- Modify (substituir): `04-Sendas/Senda Frontend.md`

- [ ] **Step 1: Backup do arquivo atual (opcional, segurança)**

```bash
cp "/home/josenaldo/repos/personal/codex-technomanticus/04-Sendas/Senda Frontend.md" \
   "/tmp/Senda Frontend.bak.md"
```

(Esse backup pode ser deletado depois da Task 14 validar tudo.)

- [ ] **Step 2: Substituir o conteúdo pelo template canônico aplicado**

Usar o `00-Meta/templates/trail.md` (atualizado na Task 4) como base. Preencher:

```markdown
---
type: trail
title: "Senda Frontend"
domain: "[[03-Dominios/Tecnologia/Frontend/index]]"
maturity: minimal
status: active
publish: true
created: 2024-01-01  # data original da senda; manter pra preservar histórico
updated: 2026-05-03
tags:
  - senda
  - frontend
---

# Senda Frontend

> Caminho de estudo de engenharia frontend. Atravessa fundamentos de linguagem (HTML, CSS, JavaScript core, TypeScript), libs e frameworks (React e ecossistema), tooling, e disciplinas cross-tech (arquitetura, perf, acessibilidade).

## Pré-requisitos

- (deixar vazio inicialmente; popular conforme necessário)

## Sequência

<!-- Ordem aproximada — ajustar conforme prioridade de estudo -->

1. [[03-Dominios/Tecnologia/Frontend/index]]
2. [[03-Dominios/HTML/index]]            <!-- omitir se HTML não foi criado -->
3. [[03-Dominios/CSS/index]]             <!-- omitir se CSS não foi criado -->
4. [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]]
5. [[03-Dominios/Tecnologia/TypeScript/index]]
6. [[03-Dominios/Tecnologia/React/index]]
7. <demais notas-stub criadas na Task 11, em ordem>

## Progresso

```dataview
TABLE WITHOUT ID
  file.link AS "Nota",
  default(progresso, "pendente") AS "Status"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
SORT file.name ASC
```

**Resumo:**

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "feito")) AS "Feitas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "andamento")) AS "Em andamento",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pausado")) AS "Pausadas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pendente")) AS "Pendentes"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
GROUP BY true
```
```

- [ ] **Step 3: Validar no Obsidian**

Abrir Senda Frontend. Verificar:
1. Bloco dataview executa e mostra a lista das notas referenciadas.
2. Cada nota aparece com seu `progresso` (ou `pendente` por default).
3. Resumo numérico mostra contagens corretas.

Se algo falhar (query não executa, ou retorna vazio): debug:
- Plugin Dataview habilitado? (`Ctrl+P` → "Open Dataview Reference").
- Plugin habilitado pra inline JS? (config Dataview → "Enable Inline JS Queries" — se a query falhar, talvez precise dessa config; testes com fallback DQL primeiro).
- Wikilinks resolvem corretamente? (rodar `outgoing([[]])` num bloco dataview de teste).

- [ ] **Step 4: Commit**

```bash
git add "04-Sendas/Senda Frontend.md"
git commit -m "refactor(senda/frontend): aplica template canônico + dataview de progresso"
```

---

## Task 13: Aplicar `progresso` real nas notas referenciadas

**Files:**
- Modify: várias notas em `03-Dominios/<estantes>/` (criadas nas Tasks 6-11)

> Esta task popula o estado real do usuário — interativa.

- [ ] **Step 1: Listar todas as notas que aparecem na Senda Frontend**

Abrir a Senda Frontend no Obsidian. O bloco dataview mostra cada uma. Listar.

- [ ] **Step 2: Para cada nota, perguntar ao usuário o estado real**

Pergunta padrão: "Para a nota `<Nome>` — `pendente`, `andamento`, `feito`, `pausado` ou `abandonado`?"

Default sugerido: `pendente` para tudo recém-criado, `andamento` para o que ele declarou estar estudando ativamente.

Compilar respostas em uma lista.

- [ ] **Step 3: Aplicar `progresso` em cada nota**

Para cada nota com valor diferente do default:

```bash
# Exemplo (ajuste o caminho e valor):
# Editar o frontmatter de "03-Dominios/Tecnologia/React/TanStack Query.md"
# trocar `progresso: pendente` por `progresso: andamento`
```

Usar Edit tool ou editor de texto. Não precisa script — são poucas notas.

- [ ] **Step 4: Validar no Obsidian que o resumo da Senda Frontend reflete o estado real**

Abrir Senda Frontend. O resumo numérico deve mostrar contagens não-zeradas em "Em andamento", "Feitas", etc., conforme as marcações.

- [ ] **Step 5: Commit**

```bash
git add "03-Dominios/"
git commit -m "feat(progresso): aplica estado real nas notas da Senda Frontend"
```

---

## Task 14: Validação final no Obsidian

**Files:**
- (nenhum — apenas validação)

- [ ] **Step 1: Abrir a Senda Frontend e validar o sistema completo**

Checklist:
1. Frontmatter da senda renderiza (`type: trail`, `domain`, `maturity`, etc.).
2. Lista "Sequência" mostra todos os wikilinks; cada um resolve pra uma nota existente.
3. Bloco dataview principal executa: tabela com Nota + Status.
4. Resumo numérico executa: Total, Feitas, Em andamento, Pausadas, Pendentes.
5. Nenhum link externo direto na senda (todos foram movidos pra notas de domínio via `[!convite]`).
6. Nenhum wikilink pra heading interno do arquivo (`[[#...]]`).

- [ ] **Step 2: Abrir 3 notas-stub e validar callouts `[!convite]`**

Em pelo menos 3 notas-stub:
1. Callout `[!convite]` renderiza (com cor padrão do tema, já que a Task 5 só afeta o site).
2. Links externos dentro do callout funcionam (ctrl+click abre).

- [ ] **Step 3: Validar que outras sendas ainda funcionam (não-regressão)**

Abrir 2-3 sendas existentes não tocadas (ex.: Senda IA, Senda Java). Verificar:
- Não há erro pelo Templater ou Dataview por causa do template alterado (o template novo só afeta sendas criadas depois).
- Sendas existentes renderizam como antes.

- [ ] **Step 4: Sem commit (já está tudo commitado das tasks anteriores)**

Apenas marcar a task como concluída.

---

## Task 15: Validação final no Quartz (site)

**Files:**
- (nenhum — apenas validação)

- [ ] **Step 1: Build local do site**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus-site
npx quartz build
```
Expected: build completa sem erros.

- [ ] **Step 2: Servir localmente**

```bash
npx quartz build --serve
```

- [ ] **Step 3: Navegar e validar**

Abrir `http://localhost:8080` e validar:
1. Senda Frontend renderiza no site.
2. A seção "## Progresso" da senda — decisão: aceitar que ela aparece como markdown bruto (visitante vê o código `dataview`), OU configurar Quartz pra omitir essa seção. Se for omitir, será uma task adicional (não estimada aqui — vide spec §8).
3. Notas-stub do domínio renderizam.
4. Callouts `[!convite]` aparecem com cor roxa e ícone do "portal/settings" (Task 5).

- [ ] **Step 4: Confirmar que o deploy automático funciona**

Após push no `codex-technomanticus`, o repository_dispatch pra `codex-technomanticus-site` é disparado. Acompanhar o GH Action e abrir o site público após o deploy. Validar no site público.

- [ ] **Step 5: Sem commit (validação apenas)**

Marcar como concluída. Se a renderização do site mostrar problemas com a seção `## Progresso` que justifiquem omissão, criar task de follow-up.

---

## Self-Review

### Spec coverage

| Item da spec | Task que implementa |
|---|---|
| §4.1 Modelo conceitual (zonas) | Task 1 (guia) |
| §4.2 Domínios = estantes; Sendas = fluxograma | Task 1 (guia) |
| §4.3 Organização dos domínios | Task 1 (guia) + Tasks 6-10 (criação das estantes) |
| §4.4 Convite | Task 1 (guia) + Task 5 (CSS) + Task 11 (uso em notas) |
| §5 Modelo de dados (`progresso`) | Task 1 (guia) + Tasks 2-3 (templates) + Task 13 (aplicação) |
| §6.1 Template canônico de senda | Task 4 |
| §6.2 Atualizações em outros templates | Tasks 2-3 |
| §6.3 Bloco dataview de agregação | Task 4 (no template) + Task 12 (na Senda Frontend) |
| §6.4 Callout `[!convite]` | Task 5 (CSS) + Task 11 (uso) |
| §7 Privacy (apocrypha não tocado) | (não há task; é restrição negativa) |
| §8 Visibilidade no Quartz | Task 5 (CSS) + Task 15 (validação) |
| §9 Repos afetados | Tasks 1-13 (público) + Task 5 (site) |
| §10 Piloto Senda Frontend | Tasks 6-13 |
| §14 Aceitação | Tasks 14-15 (validação contra critérios) |

Coberto. Itens fora de escopo (§13 trabalhos subsequentes) não têm tasks aqui — corretos.

### Placeholder scan

Sem `TBD` / `TODO` / "implement later". Tasks 9-11 são interativas por natureza (exigem decisão do usuário), e isso é explícito — não é placeholder.

### Type consistency

- `progresso` com 5 valores consistentes em todas as tasks: `pendente`, `andamento`, `feito`, `pausado`, `abandonado`. ✓
- `maturity` com 2 valores: `minimal`, `structured`. ✓
- `status` da senda: `active | done | archived` (separado do `status` da nota: `seedling | budding | evergreen`). ✓
- Frontmatter de `index.md` de domínio: `type: moc`, `publish: true`. ✓
- Frontmatter de senda: `type: trail`, `publish: true`. ✓
- Caminhos consistentes: `03-Dominios/<X>/index.md`, `00-Meta/templates/...`, `00-Meta/guia/...`. ✓

Plano íntegro.
