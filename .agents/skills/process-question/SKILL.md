---
name: process-question
description: "Expande uma semente de pergunta do backlog `03-Dominios/Inglês/Entrevistas/Database/Backlog de Perguntas.md` em dois Q-files completos (EN + PT) seguindo o template canônico (Q008-Q010). Aciona com `/process-question Q032`, \"processa a pergunta Q022\", \"expande a semente Q014\", \"transforma Q026 em Q-file\". Lê a inspiração GCA pra contexto de domínio, lê o dossiê do usuário (Roadmap.md) pra voz e posicionamento, gera draft sênior com anchor phrases, e move o card de Pendentes pra Processadas no backlog."
---

# Skill: process-question

Expande uma semente do backlog em **dois** Q-files completos (`QNNN - <title> - EN.md` e `QNNN - <pergunta> - PT.md`) seguindo o template canônico que Q008-Q010 estabeleceram.

## Quando usar

Ative quando o usuário:

- Invoca `/process-question Q###` (ex.: `/process-question Q032`)
- Pede "processa a pergunta Q022", "expande a semente Q014", "transforma Q026 em Q-file"
- Aponta uma seção `### Q###` do backlog e pede pra "fazer isso virar pergunta completa"

## Quando NÃO usar

| Situação | O que fazer |
|---|---|
| Usuário quer **adicionar** uma nova semente | Sugira `/seed-question` |
| Usuário quer **refinar uma Resposta Padrão já existente** | Sugira `/coaching` (modo socrático) |
| Q### já está em `## Processadas` | Aborte; mostre o link pro Q-file existente |
| Q### não existe no backlog | Aborte; liste os pendentes disponíveis |

## Pré-requisitos

Arquivos lidos para contexto (sempre, em paralelo):

1. **Backlog:** `03-Dominios/Inglês/Entrevistas/Database/Backlog de Perguntas.md` — pra extrair a semente
2. **Dossiê do usuário:** `03-Dominios/Inglês/GCA/Roadmap.md` — perfil, gargalos, alvo de cargo
3. **Inspiração GCA** (campo `inspiration:` da semente) — contexto de domínio. Pode ser uma Session, Community ou Mock Interview.
4. **Template de referência:** uma Q-file recente (ex.: `Q010 - How does Netflix...` ou `Q008 - How would you triage...`) — pra calibrar estrutura, voz e tom.

## Fluxo de execução

### 1. Parse do input

Extrai o `question_id` do input. Formatos suportados:

- `/process-question Q032`
- `/process-question q032` (case-insensitive)
- "processa a pergunta Q022"
- "expande a Q014"

Se o ID for ambíguo ou faltar, peça uma vez ao usuário.

### 2. Localizar a semente no backlog

1. Leia `Backlog de Perguntas.md`.
2. Busque seção `### Q### — ...` dentro de `## Pendentes`.
3. Se não encontrar em Pendentes mas encontrar em Processadas → aborte, mostre link pro Q-file existente.
4. Se não encontrar de jeito nenhum → aborte, liste os Q### disponíveis em Pendentes.

Extraia da seção: `category`, `phase`, `angle`, `inspiration`, `question`.

### 3. Carregar contexto em paralelo

Leia simultaneamente:

- O arquivo de inspiração apontado em `inspiration:` (resolva o wikilink pra caminho real)
- `03-Dominios/Inglês/GCA/Roadmap.md` (dossiê do usuário)
- Uma Q-file recente como template (ex.: Q010 ou Q008)

Se o arquivo de inspiração não for encontrado, prossiga com placeholder e avise o usuário no relatório final.

### 4. Decidir os slugs de arquivo

**Padrão de nomenclatura:**

- EN: `QNNN - <Short Title in English> - EN.md`
- PT: `QNNN - <Titulo curto em portugues sem acento> - PT.md`

Convenções (ver memory `feedback_vault_conventions.md`):

- Filename em ASCII (sem acentos, sem caracteres especiais).
- Hífen ` - ` como separador.
- Em-dash `—` só no título (frontmatter `title:`), não no nome de arquivo.
- Versão PT pode reformular a pergunta naturalmente em PT-BR (não tradução literal).

### 5. Gerar Q###-EN.md

Estrutura **obrigatória** (replicar Q008-Q010):

```yaml
---
title: "QNNN - <Short Title> - EN"
created: <hoje YYYY-MM-DD>
updated: <hoje YYYY-MM-DD>
type: interview-question
status: seedling
question_id: QNNN
language: en
category: <slug da semente>
interview_phase: <slug da semente>
difficulty: hard
framework:
  - <1 a 2 frameworks: ex. reframe-the-problem, hypothesis-driven-triage, claims-prioritization>
tags:
  - inglês
  - entrevista
  - database
  - <tag específica do tema>
publish: false
related_language_note: "[[QNNN - <PT title> - PT]]"
source:
  - "<wikilink da inspiração, se for material GCA real>"
---
```

> Se `inspiration:` é literalmente uma seção GCA (ex.: `[[Session 04 - Resilience Architecture]]`), use no `source:`. Se for descritivo sem nota correspondente no vault, omita `source:` ao invés de criar wikilink quebrado.

Seções (ordem rígida, todas presentes):

1. `# QNNN - <Short Title> - EN`
2. `> [!question] Main question` — pergunta principal, 1 parágrafo
3. `## Standard Answer` com `> [!quote]-` (foldable) — voz primeira pessoa, ~400-450 palavras (2.5-3 min spoken)
4. `## Alternative Questions` — 3 a 5 reformulações que podem aparecer na real
5. `## Answer Strategy` com `> [!tip]` — meta-estratégia em 1-2 parágrafos curtos
6. `## What This Question Tests` — 4 a 6 bullets
7. `## Strong Answer Checklist` — 6 a 8 checkboxes `- [ ]`
8. `## Common Traps` com `> [!failure]` — 5 a 6 armadilhas comuns
9. `## Vocabulary / Phrases` — tabela com 5-6 frases-âncora + uso
10. `## Possible Follow-ups` — 3 a 5 follow-ups com formato `**Q?** → A.`
11. `## Delivery Notes` com `> [!info] Voice note tips` — duração, pausas, 3 anchor phrases, o que cortar se estiver longo
12. `## Related Notes` — wikilinks pro par PT + 1-2 Q-files vizinhas relevantes + source

#### Voz da Standard Answer

Critérios não-negociáveis:

- **Primeira pessoa**, voice-note style ("Okay, let me think through this out loud" / "Okay, let me walk through this the way I would in an interview")
- **2.5 a 3 minutos** falado (~400-450 palavras)
- **Abertura com reframe ou postura sênior** (ex.: "ruthless about priorities", "stabilize, not solve", "stopped streaming in real time")
- **Trade-off explícito nomeado** no meio ou fim
- **3 anchor phrases memoráveis** distribuídas no texto
- **Fechamento com meta-lição** (a coisa-grande que essa resposta sinaliza pro entrevistador)
- **Sem jargão exibicionista** — números em faixas ("around 95%", "about 30 seconds"), nunca precisão fake
- **Respeita o gargalo do usuário:** combate over-explaining (frases curtas, parágrafos curtos), velocidade controlada (estrutura previsível), técnica traduzida em impacto

Cale o "uhm/like" e jargão operacional. Texto pra ser **falado**, não lido.

### 6. Gerar Q###-PT.md

Mesma estrutura. Diferenças:

- `language: pt`
- Frontmatter `related_language_note:` aponta pro EN
- Pergunta principal e Resposta Padrão **adaptadas pra PT-BR**, não traduzidas literalmente. Mantém anchor phrases, mas traduzidas idiomaticamente (ex.: "ruthless about priorities" → "implacável com prioridades").
- Cabeçalhos em PT: `## Resposta padrão`, `## Perguntas alternativas`, `## Estratégia de resposta`, `## O que a pergunta testa`, `## Checklist de resposta forte`, `## Armadilhas comuns`, `## Vocabulário / Frases`, `## Possíveis follow-ups`, `## Notas de entrega`, `## Notas relacionadas`
- Callouts traduzidos: `> [!question] Pergunta principal`, `> [!info] Dicas pro voice note`
- Filename em ASCII sem acentos

### 7. Mover card pra Processadas

No `Backlog de Perguntas.md`:

1. Remova a seção `### Q### — ...` inteira de `## Pendentes`.
2. Adicione no fim de `## Processadas` uma linha:
   ```
   - [[QNNN - <Short Title> - EN]] · [[QNNN - <PT title> - PT]] · *<categoria>* · processada em <YYYY-MM-DD>
   ```
3. Atualize o frontmatter do backlog:
   - `updated: <hoje>`
   - `pending: <N-1>`
   - `processed: <N+1>`

### 8. Reportar ao usuário

Mensagem final compacta:

```
✅ Q### processada.

Arquivos criados:
- 03-Dominios/Inglês/Entrevistas/Database/QNNN - <title> - EN.md
- 03-Dominios/Inglês/Entrevistas/Database/QNNN - <pt title> - PT.md

Backlog: <pending> pendentes, <processed> processadas.

Próximos passos sugeridos:
- /coaching <arquivo EN> pra refinar a Standard Answer.
- /process-question <próxima> se quiser seguir em sequência.
```

## Edge cases

| Caso | Comportamento |
|---|---|
| ID não fornecido no input | Pergunte uma vez |
| Q### inexistente em Pendentes nem Processadas | Aborte; liste Q### disponíveis em Pendentes |
| Q### já em Processadas | Aborte; mostre link pro Q-file existente |
| Inspiração GCA referencia nota inexistente | Prossiga; gere sem `source:`; avise no relatório |
| Categoria nova (não está no `index.md`) | Use o slug do seed; sugira no relatório atualizar `index.md > ## Categorias iniciais` |
| Conflito de nome de arquivo (já existe Q-file com mesmo slug) | Aborte; peça novo título curto pro usuário |
| Usuário quer só EN ou só PT | Não suportado por default; este skill sempre cria o par. Se pedir explicitamente "só EN", crie EN e marque o card no backlog como "EN feito, PT pendente" (caso raro) |

## Convenções rígidas

- **Sempre cria o par EN + PT.** Banco é bilíngue por design.
- **Filename em ASCII** — sem acentos no nome de arquivo, sempre.
- **Frontmatter `title:` com em-dash** se o título original tinha; nome de arquivo com hífen ASCII.
- **`updated:` bumpado em todas as 3 mudanças** (Q-EN, Q-PT, backlog).
- **Voz primeira pessoa, 2.5-3 min** — não escreva resposta de 5 min por mais "completa" que pareça. Aderência ao tempo > completude.
- **3 anchor phrases obrigatórias** — testadas se você consegue listá-las no `Vocabulary / Phrases` e referenciá-las no `Delivery Notes`.
- **Trade-off explícito** — toda Standard Answer nomeia pelo menos um trade-off real, não pinta tudo positivo.
- **Não invente números precisos** — sempre faixas ("around 95%", "uns 30 segundos", "between 2 and 10 seconds").
- **Sem promessa de cobertura completa** — o `Delivery Notes` sempre diz o que cortar se estiver longo, e o `Possible Follow-ups` sempre nomeia o que não foi coberto na resposta principal.

## Exemplo

```
Usuário: /process-question Q032

Skill:
1. Lê Backlog → encontra Q032 em Pendentes (gap de saúde).
2. Lê Roadmap.md (dossiê: gap 2016-2020, hemodiálise, async, Manager of One).
3. Lê Session 04 - Resilience Architecture (inspiration).
4. Lê Q010 como template recente.
5. Gera Q032 - How do you reframe the 2016-2020 health gap as operational advantage - EN.md
   com anchor phrases: "strategic hiatus, not absence" / "the constraint forced the discipline" / "remote-async is not a workaround, it is the operating system".
6. Gera Q032 - Como reformular o gap de saude como vantagem operacional - PT.md mirroring.
7. Move card de Pendentes pra Processadas em Backlog de Perguntas.md.
8. Bumpa contadores: pending: 27, processed: 1.
9. Reporta sucesso + sugere próxima Q22 (negociação) ou Q26 (curveball C-level).
```
