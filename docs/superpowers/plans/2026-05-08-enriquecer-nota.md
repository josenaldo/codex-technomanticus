# enriquecer-nota Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `.claude/skills/enriquecer-nota/SKILL.md` file that codifies the note enrichment process for the Codex vault.

**Architecture:** A single Markdown skill file following the same conventions as the existing `verbete` skill. No code to write — the deliverable is the instruction document that Claude Code reads when `/enriquecer-nota` is invoked. The skill delegates verbete creation to the existing `/verbete` skill logic.

**Tech Stack:** Obsidian Flavored Markdown, Claude Code skill format (frontmatter + structured sections), Bash (grep, find) for vault discovery.

**Spec:** `docs/superpowers/specs/2026-05-08-enriquecer-nota-design.md`
**Reference skill:** `.claude/skills/verbete/SKILL.md`

---

## File Map

| Action | Path | Responsibility |
| ------ | ---- | -------------- |
| Create | `.claude/skills/enriquecer-nota/SKILL.md` | Full skill document |

---

### Task 1: Scaffolding — criar diretório e arquivo vazio

**Files:**
- Create: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Criar o diretório da skill**

```bash
mkdir -p .claude/skills/enriquecer-nota
```

- [ ] **Step 2: Verificar que o diretório existe**

```bash
ls .claude/skills/
```

Expected: lista inclui `enriquecer-nota/`

- [ ] **Step 3: Commit do scaffold**

```bash
git add .claude/skills/enriquecer-nota/
git commit -m "chore: scaffold enriquecer-nota skill directory"
```

---

### Task 2: Escrever o SKILL.md — frontmatter e seções de contexto

**Files:**
- Modify: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Escrever frontmatter + seção "Quando usar"**

Conteúdo a escrever no arquivo:

```markdown
---
name: enriquecer-nota
description: >
  Enriquece uma nota do vault: analisa estrutura e conteúdo, adiciona wikilinks
  para termos já presentes no dicionário do domínio, cria verbetes ausentes,
  busca referências externas e atualiza frontmatter. Apresenta plano antes de
  executar. Use quando o usuário invocar /enriquecer-nota [path] [instrução],
  ou pedir pra "enriquecer", "melhorar", "atualizar" ou "revisar" uma nota.
---

# Skill: enriquecer-nota

Enriquece uma nota do vault em cinco fases: identificar alvo → analisar →
planejar → confirmar → executar. Nunca edita sem confirmação prévia.

## Invocação

```
/enriquecer-nota [path] [instrução complementar]
```

- **Sem `path`:** Pergunta ao usuário qual nota deve ser enriquecida.
- **Com `path`:** Usa o arquivo indicado diretamente (relativo à raiz do vault).
- **Instrução complementar:** Texto livre tratado como contexto adicional —
  ex: foco temático, URLs de referência a incorporar, ênfase em seção específica.

Exemplos:
```
/enriquecer-nota
/enriquecer-nota 03-Dominios/IA/Economia de Tokens/02 - Anatomia.md
/enriquecer-nota 03-Dominios/IA/02 - Anatomia.md foca na parte de reasoning
/enriquecer-nota 03-Dominios/IA/02 - Anatomia.md https://example.com/artigo
```

## Quando usar

Ative quando o usuário:

- Invoca `/enriquecer-nota [path] [instrução]`
- Pede "enriquece essa nota", "melhora o conteúdo de X", "atualiza a nota Y"
- Pede "adiciona referências / links / verbetes" a uma nota específica

## Quando NÃO usar (e o que fazer)

| Situação | Resposta |
| -------- | -------- |
| Usuário quer criar nota nova | Esta skill só enriquece notas existentes; use o template correto |
| Usuário quer só adicionar um verbete | Use `/verbete` diretamente |
| Usuário quer reescrever a nota do zero | Reescrita completa é fora de escopo; faça manualmente |
```

- [ ] **Step 2: Verificar que o frontmatter está correto**

```bash
head -10 .claude/skills/enriquecer-nota/SKILL.md
```

Expected: mostra `---`, `name: enriquecer-nota`, `description:` sem erros de YAML.

---

### Task 3: Escrever Fase 1 — Identificar nota-alvo

**Files:**
- Modify: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Adicionar a Fase 1 ao arquivo**

Append ao SKILL.md:

```markdown
## Fase 1 — Identificar nota-alvo

1. Se `path` foi fornecido, valida que o arquivo existe:
   ```bash
   ls "<vault_root>/<path>"
   ```
   Se não existir, aborta com erro claro: "Arquivo não encontrado: `<path>`".

2. Se `path` não foi fornecido, pergunta ao usuário:
   ```
   Qual nota você quer enriquecer? Informe o path relativo ao vault ou o título.
   ```

3. Lê o arquivo inteiro (frontmatter + corpo).

4. Identifica o **domínio** da nota pelo path:
   - `03-Dominios/IA/...` → domínio IA
   - `03-Dominios/Programacao/...` → domínio Programação
   - Nota fora de `03-Dominios/` → domínio indefinido (continua sem dicionário)

5. Localiza o **dicionário do domínio**:
   ```bash
   grep -rl "^type: glossary$" --include="*.md" "<pasta_do_dominio>"
   ```
   - 1 resultado → usa direto.
   - Vários → lista títulos e pergunta qual.
   - 0 → continua sem dicionário (as fases de linkagem ficam desativadas).
```

---

### Task 4: Escrever Fase 2 — Análise

**Files:**
- Modify: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Adicionar a Fase 2 ao arquivo**

Append ao SKILL.md:

```markdown
## Fase 2 — Análise

A skill examina a nota em cinco dimensões e constrói a lista de mudanças
propostas. Nada é editado ainda.

### 2a. Frontmatter

Verifica campo a campo:

| Campo | Condição | Ação proposta |
| ----- | --------- | ------------- |
| `status` | valor é `seedling` | `seedling → growing` |
| `updated` | qualquer valor | bumpar para hoje (`YYYY-MM-DD`) |
| `progresso` | ausente e `status` atual é `seedling` | adicionar `progresso: andamento` |
| `publish` | ausente | sugerir adicionar (pergunta ao usuário o valor) |

### 2b. Estrutura

- TL;DR (`> [!abstract] TL;DR`) está presente?
  - Se não: propor adicionar antes do primeiro `##`.
- Existe parágrafo de introdução entre o TL;DR e o primeiro `##`?
  - Se não: propor adicionar introdução.
- Seção `## Veja também` existe?
  - Se não e houver referências a adicionar: propor criar no final da nota.

### 2c. Conteúdo

- Identifica typos e erros gramaticais óbvios (ex: palavra digitada errada,
  concordância verbal, crase).
- Identifica frases ambíguas que uma reescrita cirúrgica clarificaria.
- Se instrução complementar trouxer URLs: busca web nesses links via WebSearch
  para extrair informação relevante e propor adição ao conteúdo.
- Se instrução complementar indicar foco temático: prioriza lacunas nessa área.

**Nível de intervenção: moderado** — corrige typos e reescreve frases ambíguas.
Nunca reescreve seções inteiras, nunca remove conteúdo existente.

### 2d. Termos técnicos — varredura de linkagem

Para cada termo técnico identificado no corpo da nota:

1. Verifica se já está linkado (`[[...]]`). Se sim, ignora.
2. Busca no dicionário do domínio por `### <Termo>` (case-insensitive):
   - **Encontrado:** propor adicionar wikilink inline preservando texto original:
     `[[NomeDoDicionário#Termo|texto original da nota]]`
   - **Não encontrado:** propor criar verbete no dicionário (via lógica da skill
     `/verbete`) + adicionar wikilink na nota após a criação.

Agrupa os resultados em dois grupos para o plano:
- **LINKS** — termos já no dicionário (só wikilink na nota)
- **DICIONÁRIO** — termos ausentes (criar verbete + wikilink)

### 2e. Referências externas e notas relacionadas

- Busca web (WebSearch) por artigos, papers ou docs oficiais relevantes ao
  tema da nota (usando instrução complementar como guia quando presente).
- Grep no vault por notas com tags ou títulos semanticamente relacionados:
  ```bash
  grep -rl "<termo_principal>" --include="*.md" 03-Dominios/
  ```
- Candidatos à seção `## Veja também` (notas internas + links externos).
```

---

### Task 5: Escrever Fase 3 — Plano

**Files:**
- Modify: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Adicionar a Fase 3 ao arquivo**

Append ao SKILL.md:

```markdown
## Fase 3 — Plano

Após a análise completa, apresenta ao usuário um plano categorizado.
Nenhuma edição é feita antes da confirmação.

Formato do plano:

```
PLANO — <título da nota>

FRONTMATTER
[ ] status: seedling → growing
[ ] updated: → 2026-05-08
[ ] progresso: → andamento

ESTRUTURA
[ ] Adicionar parágrafo de introdução após TL;DR

CONTEÚDO
[ ] Corrigir typo: 'estatégia' → 'estratégia'
[ ] Reescrever frase ambígua em §Reasoning Tokens: "<frase atual>" → "<proposta>"

LINKS — termos já no dicionário (wikilink a adicionar na nota)
[ ] [[Dicionário de IA#Reasoning tokens|reasoning tokens]] — ocorrência em §Reasoning Tokens
[ ] [[Dicionário de IA#Prompt caching|estratégia de caching]] — ocorrência em §Input Tokens

DICIONÁRIO — termos ausentes (criar verbete + adicionar wikilink)
[ ] speculative decoding

REFERÊNCIAS
[ ] Seção "Veja também": [[05 - Prompt caching na prática]]
[ ] Seção "Veja também": https://example.com/artigo-relevante

[c] confirmar tudo  [x] cancelar  [e] editar item N
```

Opções de resposta do usuário:

- `[c]` — confirma tudo, avança para Fase 4.
- `[x]` — cancela, nenhuma edição feita.
- `[e] N` — apresenta o item N e permite ao usuário fornecer texto revisado;
  após confirmação do item, retorna ao plano completo para confirmação final.

Se o plano estiver vazio (nada a fazer), informa ao usuário e encerra.
```

---

### Task 6: Escrever Fase 4 — Execução

**Files:**
- Modify: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Adicionar a Fase 4 ao arquivo**

Append ao SKILL.md:

```markdown
## Fase 4 — Execução

Aplica as mudanças aprovadas na ordem abaixo. Cada etapa lê o estado atual
do arquivo antes de editar (nunca trabalha com estado em cache).

**Ordem determinística:**

1. **Frontmatter** — atualiza `status`, `updated`, `progresso` e demais campos
   aprovados. Formato de data: `YYYY-MM-DD`.

2. **Estrutura** — adiciona TL;DR (`> [!abstract] TL;DR\n> <texto>`) se ausente,
   seguido do parágrafo de introdução se ausente. Ambos inseridos antes do
   primeiro `##` do corpo.

3. **Conteúdo** — aplica correções cirúrgicas aprovadas (typos, reescritas).
   Substituição exata da string original pela proposta aprovada.

4. **Wikilinks inline (LINKS)** — substitui cada ocorrência do texto original
   pela forma linkada `[[Dicionário#Termo|texto original]]`. Apenas a primeira
   ocorrência não linkada de cada termo por parágrafo.

5. **Verbetes (DICIONÁRIO)** — para cada termo aprovado:
   a. Pesquisa definição (lógica da skill `/verbete`: conhecimento geral ou
      WebSearch se termo obscuro).
   b. Propõe definição ao usuário no formato da skill `/verbete` (`[c]/[e]/[x]`).
   c. Após confirmação, insere verbete em ordem alfabética na seção correta
      do dicionário, bumpa `updated:` do dicionário.
   d. Insere wikilink `[[Dicionário#Termo|texto original]]` na nota.

6. **Seção "Veja também"** — se a seção já existir, acrescenta entradas novas
   ao final sem remover existentes. Se não existir, cria no final da nota:
   ```markdown
   ## Veja também

   - [[Nota Interna]]
   - [Título do Artigo](https://url)
   ```
```

---

### Task 7: Escrever Fase 5 — Relatório e seções de suporte

**Files:**
- Modify: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Adicionar Fase 5, Edge cases, Convenções e Exemplo**

Append ao SKILL.md:

```markdown
## Fase 5 — Relatório final

```
CONCLUÍDO — <título da nota>

✓ Frontmatter atualizado (status, updated, progresso)
✓ Introdução adicionada
✓ 1 typo corrigido
✓ 2 wikilinks adicionados (termos já no dicionário)
✓ 1 verbete criado: speculative decoding → Dicionário de IA
✓ Seção "Veja também" criada com 2 entradas
```

Se algum item do plano foi pulado (usuário editou para remover), indica com `–` no lugar de `✓`.

---

## Edge cases

| Caso | Comportamento |
| ---- | ------------- |
| Arquivo não encontrado | Aborta com erro claro; sugere verificar o path |
| Nota sem domínio definido | Continua sem dicionário; fases 2d e 5 ficam desativadas |
| Dicionário ambíguo (vários) | Lista títulos + pergunta qual usar |
| Plano vazio (nada a fazer) | Informa "Nota já está enriquecida" e encerra |
| Termo já linkado na nota | Ignorado na varredura (não duplica links) |
| Termo encontrado mais de uma vez no texto | Linka só a primeira ocorrência não linkada por parágrafo |
| Verbete já existe no dicionário | Só adiciona wikilink na nota; não cria verbete duplicado |
| Usuário cancela no meio da Fase 4 | Para imediatamente; mantém edições já aplicadas; reporta o que foi feito |
| instrução complementar com URL inválida | WebSearch falha silenciosamente; continua com análise padrão |
| Seção "Veja também" já existe | Adiciona entradas novas sem remover as existentes |
| `status` já é `growing` ou `mature` | Não regride; não propõe mudança de status |

---

## Convenções rígidas

- **Confirmação sempre antes de executar** — nenhuma edição sem plano aprovado.
- **Wikilink format:** `[[NomeDoDicionário#Termo|texto original da nota]]` —
  preserva o texto exato que estava na nota.
- **Primeira ocorrência por parágrafo** — não linka todo uso do termo, só o
  primeiro não linkado em cada parágrafo.
- **Verbetes seguem `/verbete`** — ordem alfabética, idioma do glossário,
  `updated:` do dicionário sempre bumpado.
- **Não remove conteúdo** — nunca apaga texto existente.
- **Não regride status** — `growing` e `mature` não voltam para `seedling`.
- **Não cria notas novas** — só edita a nota-alvo e o dicionário do domínio.

---

## Exemplo completo

```
Usuário: /enriquecer-nota 03-Dominios/IA/Economia de Tokens/02 - Anatomia.md

Skill:
1. Lê a nota. Domínio: IA. Localiza Dicionário de IA.md.
2. Análise:
   - Frontmatter: status=seedling → growing, updated=2026-05-02 → 2026-05-08
   - Estrutura: TL;DR presente, sem intro → propor intro
   - Conteúdo: typo 'estatégia'
   - Termos: 'reasoning tokens' (no dicionário), 'speculative decoding' (ausente)
   - Referências: nota relacionada [[05 - Prompt caching na prática]]
3. Apresenta plano (ver formato na Fase 3)
4. Usuário: "c"
5. Executa em ordem: frontmatter → intro → typo → wikilinks → verbete → veja também
6. Reporta:
   ✓ Frontmatter atualizado (status, updated)
   ✓ Introdução adicionada
   ✓ 1 typo corrigido
   ✓ 1 wikilink adicionado: [[Dicionário de IA#Reasoning tokens|reasoning tokens]]
   ✓ 1 verbete criado: speculative decoding → Dicionário de IA
   ✓ Seção "Veja também" criada com 1 entrada
```
```

---

### Task 8: Verificar cobertura do spec e commit final

**Files:**
- Read: `docs/superpowers/specs/2026-05-08-enriquecer-nota-design.md`
- Read: `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Verificar cobertura do spec**

Ler o spec (`docs/superpowers/specs/2026-05-08-enriquecer-nota-design.md`) e
confirmar que cada requisito tem correspondência no SKILL.md:

| Requisito do spec | Coberto em |
| ----------------- | ---------- |
| Invocação com path opcional | Fase 1, §Invocação |
| Instrução complementar como texto livre | §Invocação, Fase 2c |
| Atualizar status seedling→growing | Fase 2a, Fase 4 step 1 |
| Bumpar updated | Fase 2a, Fase 4 step 1 |
| TL;DR e intro na estrutura | Fase 2b, Fase 4 step 2 |
| Typos e reescritas cirúrgicas | Fase 2c, Fase 4 step 3 |
| Termos já no dicionário → wikilink | Fase 2d, Fase 4 step 4 |
| Termos ausentes → verbete + wikilink | Fase 2d, Fase 4 step 5 |
| Referências externas (web) | Fase 2e, Fase 4 step 6 |
| Notas relacionadas do vault | Fase 2e, Fase 4 step 6 |
| Seção "Veja também" | Fase 2b, Fase 4 step 6 |
| Plano antes de executar | Fase 3 |
| Relatório final | Fase 5 |
| Sem regressão de status | Convenções rígidas, Edge cases |

- [ ] **Step 2: Fazer commit do SKILL.md**

```bash
git add .claude/skills/enriquecer-nota/SKILL.md
git commit -m "feat: add enriquecer-nota skill"
```

- [ ] **Step 3: Verificar que a skill aparece no projeto**

```bash
ls .claude/skills/
```

Expected: lista inclui `enriquecer-nota/`

- [ ] **Step 4: Teste de sanidade — invocar a skill na nota de exemplo**

Invocar `/enriquecer-nota` passando uma nota real do vault (ex: uma nota com
`status: seedling` em `03-Dominios/`). Verificar que:

- A skill apresenta o plano sem executar nada imediatamente
- O plano contém ao menos as categorias FRONTMATTER e LINKS
- Ao responder `[x]`, nenhuma edição é feita no arquivo

---

## Self-review checklist (executor)

Antes de dar a tarefa como concluída, verificar:

- [ ] `name:` no frontmatter do SKILL.md corresponde ao nome da pasta (`enriquecer-nota`)
- [ ] Todas as fases (1–5) estão documentadas
- [ ] Edge cases cobrem os casos do spec
- [ ] Convenções rígidas listadas
- [ ] Exemplo completo presente
- [ ] Nenhum TBD, TODO ou placeholder no SKILL.md
- [ ] Commit feito com mensagem `feat: add enriquecer-nota skill`
