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
progress: in_progress | done | abandoned
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

- [[Codex/00-Meta/guia/pipeline/index|Pipeline do Codex]]
- [[Pergaminhos]]
- [[Domínios]]
- [[Sendas]]
