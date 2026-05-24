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

- [[Codex/00-Meta/guia/pipeline/index|Pipeline do Codex]]
- [[Glosas]]
- [[Sendas]]
