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

- [[Codex/00-Meta/guia/pipeline/index|Pipeline do Codex]]
- [[Domínios]]
