---
name: seed-question
description: "Adiciona uma nova semente de pergunta ao backlog `03-Dominios/Inglês/Entrevistas/Database/Backlog de Perguntas.md`. Aciona com `/seed-question \"<pergunta>\"`, \"adiciona essa pergunta no backlog\", \"nova semente: ...\", \"registra essa pergunta pra processar depois\". Detecta próximo Q### disponível, gera card no fim de Pendentes com `category`, `phase`, `angle` e `inspiration`. Se metadados não forem fornecidos, ativa modo curador (pergunta o mínimo necessário antes de inserir)."
---

# Skill: seed-question

Adiciona uma nova semente ao `Backlog de Perguntas.md` sem expandir em Q-file completo. Útil pra capturar inspirações de social media, artigos, ou ideias durante estudo — antes de decidir investir nos 400-450 palavras de Standard Answer que `/process-question` exige.

## Quando usar

Ative quando o usuário:

- Invoca `/seed-question "<pergunta>"`
- Cola conteúdo (artigo, post, thread) e pede "adiciona isso como pergunta", "registra essa pergunta", "vira semente"
- Diz "nova semente: <tema>", "tenho mais uma pergunta pro backlog"
- Pede pra capturar pergunta sem expandir ainda

## Quando NÃO usar

| Situação | O que fazer |
|---|---|
| Usuário quer **expandir** uma semente em Q-file | Sugira `/process-question Q###` |
| Pergunta já existe no backlog (similaridade alta) | Aborte; mostre o Q### existente |
| Pergunta já existe como Q-file processada | Aborte; mostre o Q-file existente |
| Usuário quer adicionar **múltiplas** perguntas de uma vez | Processe em loop, uma de cada vez, confirmando cada card antes de inserir |

## Pré-requisito

Backlog precisa existir em `03-Dominios/Inglês/Entrevistas/Database/Backlog de Perguntas.md`. Se não existir, aborte com instrução de criar manualmente (esta skill **não** cria backlog novo).

## Fluxo de execução

### 1. Parse do input

Extrai a pergunta principal e metadados opcionais. Formatos:

- `/seed-question "How do you ...?"`
- `/seed-question "How do you ...?" --category=cultural-fit --phase=hiring-manager`
- Texto livre: "adiciona essa pergunta no backlog: How do you ...?"
- Texto longo (artigo + pergunta no meio) — extrai só a pergunta principal

Se o input tem múltiplas perguntas (ex.: artigo com 3 questions), pergunte qual é a principal antes de prosseguir.

### 2. Detectar próximo Q###

1. Lê o backlog.
2. Lê todos os Q-files já existentes em `03-Dominios/Inglês/Entrevistas/Database/Q*.md` (extrai `question_id` do frontmatter).
3. Coleta também `### Q###` em `## Pendentes` e `## Processadas` do backlog.
4. Próximo ID = `max(todos) + 1`, formatado como `Q0NN`.

### 3. Checar duplicata

Compare a pergunta nova (lowercase, sem pontuação) contra:

- `question:` de todas as sementes em Pendentes
- `title:` de todos Q-files (EN) processados

Se similaridade alta (overlap de 70%+ das palavras-chave técnicas), avise e mostre o conflito. Pergunte se quer prosseguir mesmo assim, fazer edição manual da existente, ou cancelar.

### 4. Inferir ou perguntar metadados

Campos obrigatórios em cada card:

- `category` — slug kebab-case
- `phase` — fase do funil
- `angle` — 1 linha sobre o que a pergunta testa
- `inspiration` — origem (wikilink GCA ou texto descritivo)
- `question` — a pergunta em si (EN preferencialmente, espelhando convenção do banco)

**Inferência automática:**

- **category**: olhe palavras-chave da pergunta. Mapeamento típico:
  - "design / architecture / scale / CDN / system" → `system-design` ou `architecture-decisions`
  - "salary / negotiat / offer / band" → `negotiation`
  - "tell me about a time / describe a situation" → `behavioral`
  - "team / disagree / culture / async" → `cultural-fit`
  - "incident / outage / triage / debug" → `incident-response`
  - "auth / threat / privacy / security" → `security-validation`
  - "AI / agent / TDD / workflow" → `ai-workflow`
  - "tell me about yourself / pitch / intro" → `pitch-icebreaker`
  - "BLUF / short answer / 30 seconds / hiring manager" → `bluf-executive-screening`
  - Slugs existentes no banco hoje: `pitch-icebreaker`, `bluf-executive-screening`, `behavioral`, `cultural-fit`, `negotiation`, `ai-workflow`, `architecture-decisions`, `incident-response`, `security-validation`, `system-design`.

- **phase**: olhe a categoria + intent:
  - `initial-screening` (recruiter call), `technical-screen` (engineer deep dive), `hiring-manager`, `system-design`, `cultural-fit`, `negotiation`, `executive-round` (C-level)

- **angle**: gere uma frase descrevendo o vetor de teste. Ex.: "Trade-off articulation, ROI framing", "Strategic hiatus, recalibration", "Async governance, no heroism".

- **inspiration**: se o usuário forneceu (URL, citação, "vi num post do LinkedIn", "Session 07"), use. Se não, deixe placeholder `"externa"` ou pergunte.

**Confirmação ao usuário** (antes de inserir):

```
Próximo ID: Q###
Pergunta: <texto>
category: <slug>      [auto-inferida]
phase: <slug>         [auto-inferida]
angle: <frase>        [auto-gerada]
inspiration: <fonte>  [precisa de confirmação]

[c] confirmar e inserir
[e] editar metadados
[x] cancelar
```

Se o usuário pediu insert direto com flags explícitas (`--category=...`), pule a confirmação.

### 5. Inserir o card no backlog

Adicione no **fim** da seção `## Pendentes` (antes do `---` que separa de `## Processadas`):

```markdown
### Q### — <Short Title>

- **category:** <slug>
- **phase:** <slug>
- **angle:** <frase>
- **inspiration:** <texto ou wikilink>
- **question:** <pergunta completa>
```

**Short Title:** gere a partir da pergunta — 5-8 palavras, sem ponto final, sem aspas, sem "How do you / Tell me about". Ex.:
- "How do you handle code reviews async?" → "Async code review handling"
- "Tell me about a time you missed a deadline" → "Missed deadline accountability"

### 6. Atualizar frontmatter do backlog

- `updated: <hoje YYYY-MM-DD>`
- `total_seeds: +1`
- `pending: +1`

### 7. Reportar ao usuário

```
✅ Semente Q### adicionada ao backlog.

Pergunta: <texto>
Category: <slug> · Phase: <phase>

Backlog: <pending> pendentes, <processed> processadas.

Quando quiser expandir em Q-file completo: /process-question Q###
```

## Edge cases

| Caso | Comportamento |
|---|---|
| Input vazio (só `/seed-question` sem args) | Pergunte qual é a pergunta |
| Pergunta com >200 caracteres | Resumir pra Short Title; preservar pergunta completa em `question:` |
| Múltiplas perguntas no input | Pergunte qual é a principal; sugira rodar skill múltiplas vezes pras outras |
| Duplicata exata | Aborte; mostre o card existente |
| Duplicata similar (paráfrase) | Avise; mostre o card existente; pergunte se prossegue |
| Categoria nova (não no índice) | Aceite, mas sugira no relatório atualizar `index.md > ## Categorias iniciais` |
| Inspiração com wikilink quebrado | Aceite, mas avise — pode quebrar dataview |
| Backlog inexistente | Aborte com instrução pra criar a partir do template Q010-Q038 |
| Usuário forneceu pergunta em PT | Pergunte: "Quer registrar a pergunta principal em EN (convenção do banco) ou PT?" Se PT, registre PT mas avise que `/process-question` vai gerar título EN automaticamente |

## Convenções rígidas

- **Pergunta principal em EN no campo `question:`** — convenção do banco. PT vem na hora de processar.
- **Slugs em kebab-case lowercase** sempre.
- **Inserção sempre no fim de Pendentes** — não tente ordenar por categoria.
- **Frontmatter `updated:`, `total_seeds`, `pending` sempre bumpados** quando insere.
- **Não modifica `## Processadas`** — só Pendentes.
- **Confirmação antes de inserir** quando algum metadado foi inferido (não fornecido pelo usuário).

## Exemplo

```
Usuário: /seed-question "How would you design Twitter's home timeline?"

Skill:
1. Parse: pergunta = "How would you design Twitter's home timeline?"
2. Lê backlog → último Q### é Q038 → próximo é Q039.
3. Checa duplicata → nenhuma.
4. Infere:
   - category: system-design (palavras: "design", "timeline")
   - phase: system-design
   - angle: Fan-out trade-offs, hot-key handling, push vs pull architecture
   - inspiration: "externa" (não fornecido)
5. Apresenta confirmação ao usuário.
6. Usuário: "c"
7. Insere card no fim de Pendentes.
8. Bumpa updated: 2026-05-22, total_seeds: 29, pending: 28.
9. Reporta: "✅ Semente Q039 adicionada. /process-question Q039 quando quiser expandir."
```
