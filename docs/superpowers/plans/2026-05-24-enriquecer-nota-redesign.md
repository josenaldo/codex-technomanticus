# enriquecer-nota v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reescrever a skill `enriquecer-nota` para fechar lacunas reais de conhecimento (4 lentes selecionáveis) com conteúdo de fonte verificável, filtrado por um subagente crítico calibrado pela fase da nota.

**Architecture:** `SKILL.md` orquestra 7 fases e delega para 3 arquivos de referência (`lentes.md`, `critico.md`, `proveniencia.md`). A análise gera um pool de candidatos; um subagente crítico (Agent tool) poda os óbvios/sem-fonte antes do plano; o usuário faz cherry-pick; a execução é aditiva + reescrita-com-diff.

**Tech Stack:** Markdown (Claude Code skill format), Agent tool para o subagente crítico. Sem runtime de testes — "teste" = verificação estrutural + dry-run contra notas reais.

**Spec:** [`docs/superpowers/specs/2026-05-24-enriquecer-nota-redesign-design.md`](../specs/2026-05-24-enriquecer-nota-redesign-design.md)

---

## Convenções deste plano

- **Sem `Co-Authored-By`** em commits (preferência do usuário).
- **Mensagens** em conventional commits, escopo `enriquecer-nota`.
- A skill existe em DOIS locais idênticos: `.claude/skills/enriquecer-nota/` (canônico) e
  `.agents/skills/enriquecer-nota/` (espelho). Autora-se no canônico e espelha-se no fim (Task 6).
- Estamos na branch default (`main`) → a execução começa criando uma branch (Task 0).

## File Structure

| Arquivo | Responsabilidade |
|---|---|
| `.claude/skills/enriquecer-nota/SKILL.md` | Orquestra as 7 fases; invocação; formatos de plano/relatório; despacho do crítico |
| `.claude/skills/enriquecer-nota/references/lentes.md` | Define as 4 lentes + higiene baseline + schema do candidato |
| `.claude/skills/enriquecer-nota/references/critico.md` | Prompt do subagente crítico: I/O, rubrica por fase, formato de saída |
| `.claude/skills/enriquecer-nota/references/proveniencia.md` | Regras de fonte: quais lentes exigem, o que conta, como registrar |
| `.agents/skills/enriquecer-nota/**` | Espelho idêntico do canônico (sincronizado na Task 6) |
| `00-Meta/guia/skills.md` | Catálogo: atualizar a descrição de "cinco fases" → modelo de lentes (Task 7) |

**Schema canônico do candidato** (usado em `lentes.md`, `critico.md`, `SKILL.md` — manter idêntico):

```yaml
- id: C1                       # C1, C2, ...
  lente: profundidade          # profundidade | lacunas | novidade | conexoes
  tipo: adicao                 # adicao | reescrita | link | verbete
  local: "§Nome da Seção"      # ou "após §X" | "fim da nota" | "frontmatter"
  conteudo: "<texto rascunho>" # para tipo: reescrita, é o texto "depois"
  antes: "<trecho original>"   # SÓ quando tipo: reescrita
  fonte: { tipo: url, ref: "https://..." }   # tipo: url | nota | geral
```

**Quem passa pelo crítico:** apenas candidatos de conteúdo (`tipo: adicao | reescrita`) das lentes
`profundidade | lacunas | novidade`. Candidatos de `conexoes` (`link | verbete`) e a higiene baseline
**bypassam** o crítico (são objetivos).

---

## Task 0: Criar branch de trabalho

**Files:** nenhum (setup git)

- [ ] **Step 1: Criar e entrar na branch**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
git checkout -b feat/enriquecer-nota-v2
```

- [ ] **Step 2: Confirmar branch limpa do escopo**

Run: `git status --short`
Expected: nenhuma alteração pendente nos arquivos da skill (alterações prévias em outras notas podem existir; não commitá-las aqui).

---

## Task 1: `references/proveniencia.md`

**Files:**
- Create: `.claude/skills/enriquecer-nota/references/proveniencia.md`

- [ ] **Step 1: Criar o arquivo com o conteúdo completo**

````markdown
# Regras de proveniência — enriquecer-nota

Todo candidato que entra na nota por uma lente que exige fonte precisa de proveniência registrável.
Isso é o que impede a skill de adicionar "parágrafos óbvios" sem lastro.

## Quais lentes exigem fonte

| Lente              | Exige fonte? |
| ------------------ | ------------ |
| Profundidade       | **Sim** — todo candidato precisa de fonte verificável |
| Novidade c/ fonte  | **Sim** — sem fonte, o candidato é descartado na origem (nem chega ao crítico) |
| Lacunas            | Preferível; se for conhecimento estrutural consolidado, `geral` é aceito |
| Conexões           | N/A — são wikilinks internos; a "fonte" é a própria nota/dicionário |
| Higiene baseline   | N/A |

## O que conta como fonte verificável

- URL de artigo, doc oficial ou paper (com título).
- Nota do próprio vault (path ou wikilink).
- `geral` ("conhecimento geral") **só** é aceito para a lente Lacunas (cobertura estrutural).
  Nunca para Profundidade ou Novidade.

## Como registrar

- Fontes externas (URL/paper) entram na seção `## Referências` da nota, no formato já usado no vault:
  `- **Fonte** — [*Título*](url) (ano). Nota curta.`
- Se a nota não tem `## Referências`, criar a seção antes de `## Veja também` (ou ao final, se não houver).
- A fonte **nunca** vai no corpo do parágrafo — só na seção Referências (mantém a nota limpa).
- Durante o pipeline, cada candidato carrega sua fonte no campo `fonte` do schema.
- Fontes do tipo `nota` viram entradas em `## Veja também`, não em `## Referências`.
````

- [ ] **Step 2: Verificar estrutura**

Run: `grep -c "^## " .claude/skills/enriquecer-nota/references/proveniencia.md`
Expected: `3` (as três seções H2).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/enriquecer-nota/references/proveniencia.md
git commit -m "feat(enriquecer-nota): add provenance rules reference"
```

---

## Task 2: `references/lentes.md`

**Files:**
- Create: `.claude/skills/enriquecer-nota/references/lentes.md`

- [ ] **Step 1: Criar o arquivo com o conteúdo completo**

````markdown
# Lentes de enriquecimento — enriquecer-nota

Cada lente é um analisador focado com um *motor* próprio. O usuário escolhe quais rodar (Fase 2 da
SKILL). Cada lente produz **candidatos** no schema abaixo.

## Schema do candidato

```yaml
- id: C1                       # C1, C2, ... (sequencial global)
  lente: profundidade          # profundidade | lacunas | novidade | conexoes
  tipo: adicao                 # adicao | reescrita | link | verbete
  local: "§Nome da Seção"      # ou "após §X" | "fim da nota" | "frontmatter"
  conteudo: "<texto rascunho>" # para tipo: reescrita, é o texto "depois"
  antes: "<trecho original>"   # SÓ quando tipo: reescrita
  fonte: { tipo: url, ref: "https://..." }   # tipo: url | nota | geral
```

## Lente: Profundidade

- **Objetivo:** ir além do óbvio — trade-offs, edge cases, gotchas, o detalhe que separa júnior de sênior.
- **Motor (query-and-file):**
  1. Liste as *perguntas em aberto* que um leitor da fase-alvo (ou acima) faria à nota.
  2. Para cada pergunta sem resposta na nota, pesquise (WebSearch dirigido) e componha uma resposta curta.
  3. Cada resposta vira um candidato `tipo: adicao` (ou `reescrita` se aprofunda trecho raso existente).
- **Exige fonte:** sim (ver `proveniencia.md`).
- **Web:** sim.

## Lente: Lacunas

- **Objetivo:** sub-tópicos que a nota deveria cobrir e não cobre.
- **Motor:**
  1. Monte o outline de cobertura esperada do tema no nível da nota (o que uma nota completa teria).
  2. Faça diff com as seções/conteúdo atuais.
  3. Cada item faltante vira candidato `tipo: adicao`, `local: "fim da nota"` ou seção apropriada.
- **Exige fonte:** preferível; `geral` aceito para cobertura estrutural.
- **Web:** às vezes.

## Lente: Novidade c/ fonte

- **Objetivo:** fatos líquidos-novos que o leitor-alvo provavelmente não sabe.
- **Motor:**
  1. Pesquisa dirigida (WebSearch) por desenvolvimentos/dados/nuances recentes ou pouco conhecidos.
  2. Descarte na origem qualquer fato sem fonte verificável.
  3. Cada fato com fonte vira candidato `tipo: adicao`.
- **Exige fonte:** sim (sem fonte = descartado antes do crítico).
- **Web:** sim.

## Lente: Conexões

- **Objetivo:** densidade de grafo — wikilinks pro dicionário do domínio + notas/trilhas relacionadas.
- **Motor (lógica herdada da v1):**
  1. Para cada termo técnico não-linkado no corpo: `grep` por `### <Termo>` no dicionário do domínio.
     - Encontrado → candidato `tipo: link`, `conteudo: "[[Dicionário#Termo|texto original]]"`.
     - Ausente → candidato `tipo: verbete` (cria verbete via lógica `/verbete` + wikilink).
  2. `grep` no vault por notas relacionadas (tags/título) → candidatos `tipo: link` com `fonte.tipo: nota`
     (entram em `## Veja também`).
- **Exige fonte:** N/A (links internos).
- **Web:** não.
- **Bypassa o crítico.**

## Higiene baseline (sempre roda)

Independente das lentes, sempre roda um passe barato, apresentado em grupo próprio e **fora do crítico**:

- **Frontmatter:** `status: seedling → growing`; `updated: → hoje`; `progresso: andamento` se ausente e aplicável.
  Nunca regride `growing`/`mature`.
- **Typos / erros gramaticais óbvios** (correção cirúrgica).
- **Estrutura:** TL;DR (`> [!abstract] TL;DR`) e parágrafo de introdução presentes? Se não, propor.
````

- [ ] **Step 2: Verificar que as 4 lentes + higiene estão presentes**

Run:
```bash
grep -c "^## Lente:" .claude/skills/enriquecer-nota/references/lentes.md
grep -c "^## Higiene baseline" .claude/skills/enriquecer-nota/references/lentes.md
```
Expected: `4` e `1`.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/enriquecer-nota/references/lentes.md
git commit -m "feat(enriquecer-nota): add lens definitions reference"
```

---

## Task 3: `references/critico.md`

**Files:**
- Create: `.claude/skills/enriquecer-nota/references/critico.md`

- [ ] **Step 1: Criar o arquivo com o prompt completo do subagente**

````markdown
# Subagente crítico — enriquecer-nota

A SKILL despacha este prompt via Agent tool (`subagent_type: general-purpose`), UMA vez por execução,
passando o pool de candidatos de conteúdo. O crítico é um julgador **independente** de quem gerou os
candidatos — é o que mata o "parágrafo óbvio".

## Entrada (a SKILL preenche)

```yaml
fase: Magus                  # Iniciado | Adepto | Magus (default Magus se a nota não tem fase)
nota:
  titulo: "<título>"
  corpo: |
    <corpo integral da nota>
candidatos:                  # SÓ tipo adicao|reescrita das lentes profundidade|lacunas|novidade
  - { id: C1, lente: profundidade, tipo: adicao, conteudo: "...", fonte: {...} }
  - ...
```

## Rubrica por fase (corta se...)

| Fase                | Corta o candidato se... |
| ------------------- | ----------------------- |
| **Iniciado** (júnior) | for trivial até para quem está começando no tema |
| **Adepto** (pleno)    | um pleno da área já saberia; só passa se trouxer nuance/trade-off real |
| **Magus** (sênior)    | um sênior já domina; só passa edge case, gotcha ou detalhe de produção |

Regra adicional, todas as fases: **descarte qualquer candidato sem fonte verificável** quando a lente
for Profundidade ou Novidade (ver proveniência).

## Tarefa

Para cada candidato, pontue de 0 a 3:
- **novidade** — quão provável é que o leitor-alvo NÃO saiba disso (0 = todos sabem; 3 = realmente novo).
- **profundidade** — quão além do óbvio o conteúdo vai (0 = superficial; 3 = nuance de especialista).

Mantenha (`keep`) apenas candidatos com `novidade >= 2` **e** `profundidade >= 2` para a fase dada.
Descarte (`drop`) o resto, com motivo de 1 linha.

## Saída (formato exato — devolva só isto)

```yaml
sobreviventes:
  - id: C1
    veredito: keep
    novidade: 3
    profundidade: 2
    justificativa: "edge case de produção não-óbvio para sênior"
    confianca: alta            # alta | media | baixa
descartados:
  - id: C3
    veredito: drop
    motivo: "definição básica que um pleno já domina"
```
````

- [ ] **Step 2: Verificar presença da rubrica e do formato de saída**

Run:
```bash
grep -c "Iniciado\|Adepto\|Magus" .claude/skills/enriquecer-nota/references/critico.md
grep -c "sobreviventes:\|descartados:" .claude/skills/enriquecer-nota/references/critico.md
```
Expected: `>=3` na primeira; `2` na segunda.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/enriquecer-nota/references/critico.md
git commit -m "feat(enriquecer-nota): add critic subagent prompt with per-phase rubric"
```

---

## Task 4: Reescrever `SKILL.md`

**Files:**
- Modify (rewrite): `.claude/skills/enriquecer-nota/SKILL.md`

- [ ] **Step 1: Substituir o conteúdo inteiro pelo novo SKILL.md**

Escreva o arquivo com EXATAMENTE este conteúdo:

````markdown
---
name: enriquecer-nota
description: Enriquece uma nota do vault com lentes selecionáveis (profundidade, lacunas, novidade com fonte, conexões), filtradas por um subagente crítico calibrado pela fase da nota. Apresenta plano antes de executar. Use quando o usuário invocar /enriquecer-nota [path] [instrução], ou pedir pra "enriquecer", "aprofundar", "melhorar", "atualizar" ou "revisar" uma nota.
---

# Skill: enriquecer-nota

Enriquece uma nota do vault em 7 fases: identificar alvo → escolher lentes → analisar →
**criticar** → planejar → executar → reportar. Nunca edita sem confirmação prévia.

O eixo é **fechar lacunas reais com fonte verificável**, não decorar a nota. Um subagente crítico
calibrado pela fase poda candidatos óbvios antes de você ver o plano.

## Invocação

```
/enriquecer-nota [path] [instrução complementar]
```

- **Sem `path`:** pergunta qual nota enriquecer.
- **Com `path`:** usa o arquivo indicado (relativo à raiz do vault).
- **Instrução complementar:** texto livre como contexto (foco temático, URLs a incorporar). Pode
  pré-selecionar lentes (ex: "só profundidade e conexões").

## Referências (ler antes de executar)

- `references/lentes.md` — as 4 lentes, seus motores, higiene baseline, schema do candidato.
- `references/critico.md` — prompt do subagente crítico (I/O + rubrica por fase).
- `references/proveniencia.md` — quais lentes exigem fonte e como registrar.

## Quando NÃO usar

| Situação | Resposta |
| -------- | -------- |
| Criar nota nova | Esta skill só enriquece notas existentes; use o template |
| Só adicionar um verbete | Use `/verbete` diretamente |
| Reescrever a nota do zero | Fora de escopo; reescrita aqui é cirúrgica (trecho a trecho, com diff) |

---

## Fase 1 — Identificar alvo

1. Valida `path` (`ls "<vault>/<path>"`); se ausente, pergunta o path/título.
2. Lê a nota inteira (frontmatter + corpo).
3. Infere o **domínio** pelo path (`03-Dominios/<X>/`). Fora de `03-Dominios/` → domínio indefinido
   (lente Conexões e verbetes desativados).
4. Localiza o **dicionário do domínio**: `grep -rl "^type: glossary$" --include="*.md" "<pasta_do_dominio>"`.
   1 resultado → usa; vários → pergunta; 0 → segue sem dicionário.
5. Lê **`fase:`** do frontmatter (Iniciado/Adepto/Magus). Se ausente: infere pelo conteúdo; default
   **Magus** (régua sênior, a mais estrita).

## Fase 2 — Escolher lentes

Apresenta menu multi-select:

```
Quais lentes rodar? (a higiene baseline sempre roda)
[ ] Profundidade — trade-offs, edge cases, o que separa júnior de sênior
[ ] Lacunas — sub-tópicos que faltam
[ ] Novidade c/ fonte — fatos novos com fonte verificável
[ ] Conexões — wikilinks pro dicionário + notas relacionadas
```

Se a instrução complementar já indicou lentes, pré-seleciona e confirma. Pelo menos 1 lente.

## Fase 3 — Análise por lente

Para cada lente selecionada, roda o motor de `references/lentes.md` e acumula um pool de **candidatos**
(schema em `lentes.md`). Lentes que precisam de fora fazem WebSearch dirigido e registram a fonte
(`proveniencia.md`). Reescritas carregam `tipo: reescrita` + o texto `antes`.

A higiene baseline também roda aqui (frontmatter/typos/estrutura), em paralelo, mas seus itens NÃO
entram no pool do crítico.

## Fase 4 — Crítica (subagente)

Despacha UMA vez o subagente de `references/critico.md` via Agent tool (`subagent_type: general-purpose`),
passando: `fase`, `nota` (título + corpo) e os candidatos de conteúdo (`tipo: adicao|reescrita` das
lentes profundidade/lacunas/novidade). Candidatos de Conexões e a higiene **não** vão ao crítico.

Recebe `sobreviventes` (com novidade/profundidade/justificativa/confiança) e `descartados` (com motivo).

## Fase 5 — Plano

Apresenta os sobreviventes **agrupados por lente** + Conexões + Higiene. Reescritas como **diff
antes→depois**. Lista de descartados recolhida (resgatável).

```
PLANO — <título>   (fase-alvo: <Magus>)

HIGIENE
[x] status: seedling → growing
[x] updated: → <hoje>

PROFUNDIDADE
[x] +§<seção>: <rascunho>   — fonte: <url>   (crítico: "<justificativa>", alta)
[x] ~reescrever §<X> (raso): "<antes>" → "<depois>"   — fonte: <url>

LACUNAS
[x] +§<sub-tópico>: <rascunho>   — fonte: <url|geral>

NOVIDADE
[x] +<fato>   — fonte: <url>   (crítico: "<justificativa>", media)

CONEXÕES
[x] [[Dicionário#Termo|texto]] — §<Y>
[x] DICIONÁRIO: criar verbete <termo> + wikilink

DESCARTADOS PELO CRÍTICO (N) ▸ (expanda para resgatar)

[c] confirmar marcados   [x] cancelar   alternar item N   [e] editar item N
```

`[c]` executa só os itens marcados. O usuário pode desmarcar/marcar e resgatar descartados.

## Fase 6 — Execução

Ordem determinística (relê o arquivo antes de cada edição):

1. **Frontmatter** (higiene).
2. **Estrutura** — TL;DR/intro se aprovados.
3. **Adições de conteúdo** — insere blocos aprovados nos locais indicados.
4. **Reescritas (diffs)** — substituição EXATA do trecho `antes` pelo `depois` aprovado.
5. **Wikilinks inline** — `[[Dicionário#Termo|texto original]]`; 1ª ocorrência não-linkada por parágrafo.
   Dentro de tabela, escapar o pipe: `[[...\|...]]`.
6. **Verbetes** — lógica `/verbete` (alfabético na seção, idioma do glossário, bump do `updated:` do
   dicionário); depois insere o wikilink na nota.
7. **Referências** — fontes externas usadas (formato de `proveniencia.md`).
8. **Veja também** — notas internas relacionadas (sem remover existentes).

## Fase 7 — Relatório

```
CONCLUÍDO — <título>   (fase-alvo: <Magus>)
✓ Higiene: status, updated
✓ Profundidade: <n> adições + <m> trechos aprofundados (<k> fontes)
✓ Lacunas: <n> sub-tópicos
✓ Novidade: <n> fatos (<k> fontes)
✓ Conexões: <n> wikilinks, <m> verbetes criados
– Crítico cortou <n> candidatos (óbvios para a fase)
```

Itens pulados pelo usuário aparecem com `–`.

## Convenções rígidas

- **Confirmação antes de executar** — nenhuma edição sem plano aprovado.
- **Aditivo + reescrita-com-diff** — pode aprofundar trecho raso, mas só via diff antes→depois aprovado
  item a item. **Nunca remove em silêncio.** Não reorganiza a nota inteira.
- **Wikilink format:** `[[NomeDoDicionário#Termo|texto original]]`.
- **Verbetes seguem `/verbete`** (alfabético, idioma do glossário, `updated:` bumpado).
- **Proveniência obrigatória** para Profundidade/Novidade (`proveniencia.md`). Fonte vai na seção
  Referências, nunca no corpo.
- **Crítico é independente e calibrado pela fase.** Higiene e Conexões não passam por ele.
- **Não cria notas novas** — só edita a nota-alvo e o dicionário.
- **Não progride `status` para `mature`** — decisão do usuário.

## Edge cases

| Caso | Comportamento |
| ---- | ------------- |
| Arquivo não encontrado | Aborta com erro claro |
| Nota sem domínio | Conexões/verbetes desativados; demais lentes seguem |
| Nota sem `fase:` | Infere; default Magus |
| Sem dicionário no domínio | Conexões e verbetes desativados |
| Crítico devolve 0 sobreviventes | Mostra só Higiene + Conexões; avisa que nada de conteúdo passou o gate |
| WebSearch falha / offline | Lentes que dependem de web reportam "sem candidatos"; segue com o resto |
| Todas as lentes vazias e higiene vazia | "Nota já está enriquecida"; encerra |
| Reescrita: `antes` não casa exato | Pula o item, avisa; não edita às cegas |
````

- [ ] **Step 2: Verificar as 7 fases e a referência aos 3 arquivos**

Run:
```bash
grep -c "^## Fase " .claude/skills/enriquecer-nota/SKILL.md
grep -c "references/lentes.md\|references/critico.md\|references/proveniencia.md" .claude/skills/enriquecer-nota/SKILL.md
```
Expected: `7` na primeira; `>=3` na segunda.

- [ ] **Step 3: Verificar que o frontmatter `name` e `description` existem**

Run: `head -3 .claude/skills/enriquecer-nota/SKILL.md`
Expected: bloco `---` com `name: enriquecer-nota` e `description:` mencionando lentes + crítico.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/enriquecer-nota/SKILL.md
git commit -m "feat(enriquecer-nota): rewrite SKILL.md with 7-phase lens pipeline"
```

---

## Task 5: Atualizar o catálogo `00-Meta/guia/skills.md`

**Files:**
- Modify: `00-Meta/guia/skills.md` (a entrada `### /enriquecer-nota`, linha ~93-95)

- [ ] **Step 1: Localizar a descrição atual**

Run: `grep -n "cinco fases" 00-Meta/guia/skills.md`
Expected: aponta a linha da descrição da `/enriquecer-nota`.

- [ ] **Step 2: Substituir a frase de descrição**

Trocar:
```
Enriquece uma nota do vault em cinco fases: **identificar alvo → analisar → planejar → confirmar → executar**. Nunca edita sem confirmação prévia.
```
Por:
```
Enriquece uma nota com **lentes selecionáveis** (profundidade, lacunas, novidade com fonte, conexões), filtradas por um **subagente crítico calibrado pela fase** da nota. 7 fases: **identificar alvo → escolher lentes → analisar → criticar → planejar → executar → reportar**. Nunca edita sem confirmação; reescritas aparecem como diff.
```

- [ ] **Step 3: Verificar**

Run: `grep -n "subagente crítico\|lentes selecionáveis" 00-Meta/guia/skills.md`
Expected: encontra a nova descrição.

- [ ] **Step 4: Commit**

```bash
git add 00-Meta/guia/skills.md
git commit -m "docs(guia): update enriquecer-nota catalog entry for v2 lens model"
```

---

## Task 6: Espelhar para `.agents/skills/`

**Files:**
- Sync: `.agents/skills/enriquecer-nota/` ← `.claude/skills/enriquecer-nota/`

- [ ] **Step 1: Copiar o diretório canônico por cima do espelho**

```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
rm -rf .agents/skills/enriquecer-nota
cp -r .claude/skills/enriquecer-nota .agents/skills/enriquecer-nota
```

- [ ] **Step 2: Verificar que ficaram idênticos**

Run: `diff -r .claude/skills/enriquecer-nota .agents/skills/enriquecer-nota && echo IDENTICAL`
Expected: `IDENTICAL` (sem saída de diff).

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/enriquecer-nota
git commit -m "chore(enriquecer-nota): mirror v2 skill to .agents"
```

---

## Task 7: Dry-run de verificação

**Files:** nenhum (verificação manual; não commitar edições de teste)

- [ ] **Step 1: Dry-run contra nota SEM `fase:` (default Magus)**

Invoque mentalmente/realmente a skill em:
`03-Dominios/IA/Agentes de Codificação/02 - Vibe coding vs engenharia disciplinada.md`
Selecione as lentes Profundidade + Novidade. Pare na Fase 5 (plano) — **não execute**.

Verifique:
- O menu de lentes (Fase 2) apareceu.
- A Fase 4 despachou o subagente crítico.
- O plano (Fase 5) está agrupado por lente, com fase-alvo = Magus.
- Há candidatos descartados pelo crítico (prova de que o gate funciona) com motivo.
- Toda adição de Profundidade/Novidade tem fonte.

- [ ] **Step 2: Dry-run contra nota COM `fase:`**

Encontre uma nota de trilha com frontmatter `fase:` (ex.: `grep -rl "^fase:" 03-Dominios/`).
Invoque a skill, selecione Lacunas + Conexões, pare na Fase 5.

Verifique:
- A fase-alvo no plano = o valor de `fase:` da nota (não Magus).
- Conexões NÃO passou pelo crítico (links aparecem direto).
- Higiene aparece em grupo próprio.

- [ ] **Step 3: Verificação estrutural final**

Run:
```bash
cd /home/josenaldo/repos/personal/codex-technomanticus
test -f .claude/skills/enriquecer-nota/references/lentes.md && \
test -f .claude/skills/enriquecer-nota/references/critico.md && \
test -f .claude/skills/enriquecer-nota/references/proveniencia.md && \
diff -r .claude/skills/enriquecer-nota .agents/skills/enriquecer-nota && \
echo "ALL OK"
```
Expected: `ALL OK`.

- [ ] **Step 4: Registrar resultado do dry-run**

Anote no PR/branch (ou no relatório final ao usuário) o que o crítico cortou em cada dry-run — é a
evidência de que a v2 resolve o problema de "parágrafos óbvios".

---

## Self-Review (preenchido)

**1. Spec coverage:**
- 4 lentes selecionáveis → Task 2 (`lentes.md`) + Fase 2 do SKILL (Task 4). ✓
- Dois níveis de controle (lentes no início + cherry-pick no fim) → Fase 2 + Fase 5. ✓
- Crítico calibrado pela fase → Task 3 (`critico.md`) + Fase 4. ✓
- Escopo aditivo + reescrita-com-diff → Fase 6 passos 3-4 + convenções. ✓
- Higiene baseline fora do crítico → `lentes.md` + Fase 3/4. ✓
- Proveniência → Task 1 + Fase 6 passo 7. ✓
- Arquitetura de arquivos (SKILL + 3 referências) → Tasks 1-4. ✓
- Calibragem por fase (tabela) → Task 3. ✓
- Mirror `.agents` (não estava no spec, mas é realidade do repo) → Task 6. ✓
- Catálogo → Task 5. ✓

**2. Placeholder scan:** Os `<...>` nos blocos são campos de template do formato de plano/relatório
(intencionais, fazem parte do conteúdo do arquivo), não lacunas do plano. Sem TBD/TODO. ✓

**3. Type consistency:** schema do candidato idêntico em `lentes.md`, `critico.md` e `SKILL.md`
(`id/lente/tipo/local/conteudo/antes/fonte`); enum `tipo: adicao|reescrita|link|verbete` consistente;
saída do crítico (`sobreviventes`/`descartados`) idêntica entre `critico.md` e a Fase 4/5. ✓
````
