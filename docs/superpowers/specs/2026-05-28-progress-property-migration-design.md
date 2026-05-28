---
title: "Spec — Migração da propriedade `progresso` → `progress`"
created: 2026-05-28
type: spec
status: approved
publish: false
---

# Spec — Migração da propriedade `progresso` → `progress`

## Contexto

O vault (público `codex-technomanticus` + privado `codex-technomanticus-apocrypha`) usa a propriedade de frontmatter `progresso:` para rastrear o estado de leitura/processamento de uma nota. Os valores estão em português (`pendente`, `andamento`, `feito`, ...) e há inconsistência: alguns templates listam um conjunto de valores, outros outro, e algumas notas usam variações (`em-curso`, `completo`) não previstas.

O apocrypha consome essa propriedade em 3 dashboards (`Dataview`/`DataviewJS`) que dependem dos nomes exatos do campo e dos valores.

A migração tem dois objetivos:
1. Renomear a propriedade para `progress` (inglês, alinhado com convenção de estados).
2. Trocar os valores para um conjunto enxuto de 5 estados em inglês com underscore.

## Decisões de design

### Escopo — quem recebe `progress`

A propriedade aplica-se **apenas a notas consumíveis** — notas que têm um ciclo de "começar a estudar → terminar". Notas de referência ou índice usam apenas o campo `status:` existente (maturidade: `seedling`/`growing`/`evergreen`), que é semântica diferente e independente.

**Tipos consumíveis** (recebem `progress`):
- `glosa` — fichamento de artigo
- `concept` — nota conceitual (Template - Nota, Template - Interview Note)
- `lesson`, `workbook` — aula e caderno de exercícios (canal Lucy no apocrypha)
- `lesson-workbook` — caderno de exercícios de aula (GCA)
- `community-session`, `community-workbook` — sessões e workbooks de comunidade (GCA)
- `mock-interview`, `mock-interview-script`, `mock-interview-coaching-log` — material de mock interview (GCA)

A regra "todo material consumível de mentoria recebe `progress`" cobre tanto Lucy quanto GCA sem distinção.

**Tipos não consumíveis** (não recebem `progress`):
- `moc`, `glossary`, `reference` (Mestre), `how-to`, `til`, `dashboard`
- `trail`/`senda`, `trail-index`, `roadmap`, `todo-list` — índices/planos/listas vivas; usam outros campos (`status: active|seedling`, etc.)

### Conjunto de estados

| Estado | Significado |
|---|---|
| `backlog` | Fila, ainda não comecei |
| `in_progress` | Em processamento ativo |
| `paused` | Comecei e parei temporariamente |
| `done` | Processei completamente |
| `abandoned` | Desisti definitivamente |

Convenção: underscore (`in_progress`), não hífen. Consistente com convenções de state machine em inglês e evita ambiguidade do hífen no YAML.

### Mapeamento dos valores existentes

```
pendente   → backlog
andamento  → in_progress
em-curso   → in_progress
feito      → done
completo   → done
pausado    → paused
abandonado → abandoned
```

### Comportamento por situação

| Situação | Ação |
|---|---|
| Nota consumível **com** `progresso:` | Renomear chave para `progress:` + remapear valor |
| Nota consumível **sem** `progresso:` (identificada por `type:`) | Adicionar `progress: backlog` |
| Nota não consumível **com** `progresso:` (uso herdado) | **Remover** o campo (limpa inconsistência) |
| Nota não consumível **sem** `progresso:` | Não tocar |

### Sem backward-compat

Cutover completo. Sem alias `progresso` na transição. Notas, skills e dashboards são atualizados num único esforço coordenado entre os dois repos.

## Inventário do impacto

### Público (`codex-technomanticus`)

- **91 notas** com frontmatter `progresso:` (distribuição: 77 `andamento`, 32 `pendente`, 4 `feito`, 1 `em-curso`, 1 `completo`; mais 7 linhas em comentários de templates/exemplos)
- **2 templates atuais com o campo**: `Template - Glosa.md` (default `andamento`), `Template - Nota.md` (default `pendente`)
- **1 template a equipar**: `Template - Interview Note.md` (type=concept, falta o campo) → adicionar `progress: backlog`
- **5 skills** com referência ao campo:
  - `.claude/skills/arquivar-glosas/SKILL.md`
  - `.claude/skills/acordar-glosas/SKILL.md`
  - `.claude/skills/promover-glosa/SKILL.md`
  - `.claude/skills/sintetizar-glosas/SKILL.md`
  - `.claude/skills/enriquecer-nota/references/lentes.md`
- `.agents/skills/` é symlink para `.claude/skills/` (memória `project_skills_symlink`) — uma cópia, não duplicar

### Apocrypha (`codex-technomanticus-apocrypha`)

- **21 notas** com frontmatter `progresso:` (20 `pendente`, 1 `andamento`); 15 delas em `03-Dominios/Ingles/Lucy/` (lessons e workbooks)
- **GCA**: 36 notas em `03-Dominios/Inglês/GCA/` cobrindo tipos consumíveis (`community-*`, `lesson*`, `mock-interview*`) — nenhuma tem `progresso:` hoje; todas recebem `progress: backlog` (regra "Lucy + GCA seguem o mesmo esquema" confirmada pelo usuário)
- 4 notas raiz do GCA são não consumíveis (`index.md` trail-index, `Roadmap.md` roadmap, `Tarefas.md` todo-list, `Entradas.md` sem frontmatter): não recebem
- **3 templates próprios**: `Template - Nota.md`, `Template - Glosa.md` (ambos com o campo); `trail.md` (sem o campo, **não adicionar**)
- **Templates Lucy** (`00-Meta/templates/Lucy/Lucy - *.md`): aplicar regra automática por `type:` — `Lucy - Processed.md` (provavelmente `lesson`) e `Lucy - Workbook.md` (provavelmente `workbook`) recebem; `Lucy - Ebook MOC.md` (`moc`) não recebe
- **3 dashboards** com queries que dependem do campo:
  - `Dashboard - Progresso agregado.md`
  - `Dashboard - O que estudar hoje.md`
  - `Dashboard - Cross-glosa.md`
- **Prosa com menção literal ao campo**:
  - `00-Meta/guia/skills.md` (linhas 52 e 59): "independente de `progresso`" e "reseta `progresso: andamento`"
- **Prosa onde "progresso" é palavra comum** (não tocar):
  - `CLAUDE.md`, `AGENTS.md`, `00-Meta/guia/Como usar este vault.md`

## Mudanças semânticas nas skills

| Skill | Mudança |
|---|---|
| `arquivar-glosas` | Renomear referências de `progresso` → `progress`; comportamento mantido (arquiva por idade, independente de `progress`) |
| `acordar-glosas` | Reset para `progress: in_progress` ao acordar (era `andamento`) |
| `promover-glosa` | Filtra candidatas com `progress ∈ {in_progress, done}` (era `andamento`/`feito`); ao promover, transiciona `in_progress → done` |
| `sintetizar-glosas` | Atualizar exemplos no SKILL.md (frontmatter de exemplo passa a usar `progress: in_progress`) |
| `enriquecer-nota` | Setar `progress: in_progress` se ausente (e nota é consumível) |

## Mudanças nos dashboards do apocrypha

### `Dashboard - Progresso agregado.md`

Queries Dataview/DataviewJS:
- `default(r.progresso, "pendente")` → `default(r.progress, "backlog")`
- Colunas remapeadas: `Feitas` (done), `Em andamento` (in_progress), `Pausadas` (paused), `Abandonadas` (abandoned), `Pendentes` (backlog) — rótulos em PT preservados, valores comparados em EN
- Objeto de grupo: `{ feito, andamento, pausado, abandonado, pendente }` → `{ done, in_progress, paused, abandoned, backlog }`

### `Dashboard - O que estudar hoje.md`

- Filtro principal: `.where(p => p.progresso === "andamento")` → `.where(p => p.progress === "in_progress")`
- Filtro de seção "Convites": `prog === "andamento" || prog === "feito"` → `prog === "in_progress" || prog === "done"`
- Default ao ler ausência: `p.progresso ?? "pendente"` → `p.progress ?? "backlog"`

### `Dashboard - Cross-glosa.md`

- `g.progresso ?? "—"` → `g.progress ?? "—"` (puro display, sem semântica de filtro)

### Nomes dos arquivos de dashboard

Mantidos em português (`Dashboard - Progresso agregado.md` etc.). "Progresso" no título é palavra comum, não o campo.

## Plano de execução (ordem)

1. **Branch nova** em **ambos** os repos: `feat/migrate-progress-property`
2. **Templates** atualizados primeiro (público + apocrypha)
3. **Frontmatter das notas existentes**: script `sed` direcionado, com **dry-run + amostra de 5** apresentada pra confirmação antes da aplicação em massa. Estratégia:
   - Renomear chave: `s/^progresso:/progress:/` em arquivos selecionados
   - Remapear valor em mesma linha: 7 substituições conforme tabela de mapeamento
   - Seleção: arquivos com `type ∈ {glosa, concept, lesson, workbook}` (consumíveis); os demais com `progresso:` herdado têm a linha removida
   - Adição de `progress: backlog` em consumíveis sem o campo: identificar por `type:` e inserir no frontmatter
4. **Skills** atualizadas (5 arquivos no público — `.agents/skills` pega de graça via symlink)
5. **Dashboards** atualizados (3 arquivos no apocrypha)
6. **Prosa** atualizada em `guia/skills.md` do apocrypha
7. **Diff revisado**: `git diff --stat` + spot-check em arquivos representativos antes de commitar
8. **Commits** separados em cada repo, sem assinatura (conforme memória `feedback_commits`)

## Critérios de verificação

- `grep -rh "^progresso:" --include="*.md"` em **ambos** os repos → **0 matches**
- `grep -rh "^progress:" --include="*.md" | sort | uniq -c` em ambos os repos → todos os valores ∈ `{backlog, in_progress, paused, done, abandoned}`
- Skills: `grep -rn "progresso" .claude/skills/` → 0 matches
- Templates: `grep -l "progresso" 00-Meta/templates/*.md` → 0 matches em ambos os repos
- Dashboards: abrir no Obsidian e validar que os 3 dashboards populam (verificação manual do usuário)

## Não-objetivos

- Sem backward-compat (sem alias `progresso`); cutover completo
- Sem tocar `memory/` (auto-memória do Claude) nem `devlog/`
- Sem tocar prosa onde "progresso" é palavra comum (português, não o campo)
- Sem migrar tipos não consumíveis para o novo campo (eles perdem o campo se tinham)
- Sem criar referências cruzadas público↔apocrypha (memória `feedback_public_apocrypha_separation`)

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| `sed` mal calibrado corrompe frontmatter | Dry-run + amostra de 5 antes da execução em massa; `git diff --stat` antes de commit |
| Tipo de nota não previsto recebe/perde o campo erroneamente | Lista explícita de tipos consumíveis; auditar `type:` no inventário antes de migrar |
| Dashboards quebram no Obsidian | Verificação manual nos 3 dashboards após migração |
| Templates Lucy passam despercebidos | Inspeção explícita dos templates `Lucy - *.md` durante a execução; aplicar regra do tipo `lesson`/`workbook` |

## Critério de pronto

- Branches `feat/migrate-progress-property` em ambos os repos, com commits coesos
- Verificações da seção anterior passando
- Confirmação visual do usuário de que os 3 dashboards do apocrypha populam
- Spec arquivado (este documento) referenciado no commit message
